#!/usr/bin/env python3
"""
解析生成的日夜间模式语义色文件，生成基于Theme的颜色属性系统
用于支持通过Theme切换实现的日夜模式
"""

import xml.etree.ElementTree as ET
import os
from typing import Dict, List, Tuple
import re


def to_camel_case(snake_str: str) -> str:
    """将下划线命名转换为驼峰命名
    
    Args:
        snake_str: 下划线分隔的字符串，如 'border_primary'
        
    Returns:
        驼峰命名的字符串，如 'borderPrimary'
    """
    components = snake_str.split('_')
    # 第一个单词小写，其他单词首字母大写
    return components[0] + ''.join(x.title() for x in components[1:])


def parse_color_xml(file_path: str) -> Dict[str, str]:
    """解析颜色XML文件，返回颜色名称和值的映射
    
    Args:
        file_path: XML文件路径
        
    Returns:
        字典，键为颜色名称，值为颜色值或引用
    """
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    colors = {}
    for color in root.findall('color'):
        name = color.get('name')
        value = color.text.strip() if color.text else ''
        if name and value:
            colors[name] = value
    
    return colors


def resolve_color_value(color_ref: str, primitive_colors: Dict[str, str]) -> str:
    """解析颜色引用，获取最终的颜色值
    
    Args:
        color_ref: 颜色引用或直接颜色值
        primitive_colors: 原子颜色映射表
        
    Returns:
        解析后的颜色值
    """
    if color_ref.startswith('#'):
        # 直接的颜色值
        return color_ref
    elif color_ref.startswith('@color/'):
        # @color/ 引用
        color_name = color_ref[7:]  # 去掉 @color/
        if color_name in primitive_colors:
            # 递归解析，以防引用链
            return resolve_color_value(primitive_colors[color_name], primitive_colors)
        else:
            return color_ref  # 找不到，返回原引用
    else:
        return color_ref


def generate_attrs_xml(color_names: List[str], output_path: str) -> None:
    """生成颜色属性定义文件（attrs.xml）
    
    Args:
        color_names: 颜色名称列表
        output_path: 输出文件路径
    """
    xml_content = '<?xml version="1.0" encoding="utf-8"?>\n'
    xml_content += '<resources>\n'
    xml_content += '    <!-- Semantic Color Attributes -->\n'
    
    # 按字母顺序排序
    sorted_names = sorted(color_names)
    
    for name in sorted_names:
        # 转换为驼峰命名
        attr_name = to_camel_case(name)
        xml_content += f'    <attr name="{attr_name}" format="color" />\n'
    
    xml_content += '</resources>'
    
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
    
    # 写入文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    
    print(f"Generated: {output_path}")
    print(f"  - Total attributes: {len(sorted_names)}")


def generate_theme_style(colors: Dict[str, str], 
                        parent_theme: str, theme_name: str,
                        light_colors: Dict[str, str],
                        dark_colors: Dict[str, str],
                        light_primitive_colors: Dict[str, str],
                        dark_primitive_colors: Dict[str, str],
                        is_dark_mode: bool = False) -> str:
    """生成单个主题的XML内容
    
    Args:
        colors: 颜色字典（名称 -> 值）
        parent_theme: 父主题名称
        theme_name: 当前主题名称
        light_colors: 日间模式颜色字典
        dark_colors: 夜间模式颜色字典
        light_primitive_colors: 日间模式原子颜色映射
        dark_primitive_colors: 夜间模式原子颜色映射
        is_dark_mode: 是否为夜间模式
        
    Returns:
        主题的XML字符串
    """
    xml_content = f'    <!-- {theme_name} - Semantic Color Theme -->\n'
    xml_content += f'    <style name="{theme_name}" parent="{parent_theme}">\n'
    
    # 按字母顺序排序
    sorted_items = sorted(colors.items())
    
    for name, value in sorted_items:
        # 转换为驼峰命名
        attr_name = to_camel_case(name)
        
        # 获取当前值（可能是引用或直接值）
        current_value = value
        
        # 判断是否为 @color/ 引用
        if value.startswith('@color/'):
            # 解析日夜间模式的实际颜色值
            light_actual_value = resolve_color_value(light_colors.get(name, value), light_primitive_colors)
            dark_actual_value = resolve_color_value(dark_colors.get(name, value), dark_primitive_colors)
            
            # 比较两个模式下的实际颜色值是否相同
            if light_actual_value == dark_actual_value and not light_actual_value.startswith('@color/'):
                # 值相同且已解析为具体颜色值，使用 @color/ 引用
                xml_content += f'        <item name="{attr_name}">{value}</item>\n'
            else:
                # 值不同，使用当前模式的实际颜色值
                resolved_value = resolve_color_value(value, dark_primitive_colors if is_dark_mode else light_primitive_colors)
                xml_content += f'        <item name="{attr_name}">{resolved_value}</item>\n'
        else:
            # 直接的颜色值，检查是否需要对比
            # 获取对应模式下的值
            if is_dark_mode:
                light_value_for_name = light_colors.get(name, '')
                light_actual = resolve_color_value(light_value_for_name, light_primitive_colors)
                dark_actual = resolve_color_value(value, dark_primitive_colors)
            else:
                dark_value_for_name = dark_colors.get(name, '')
                light_actual = resolve_color_value(value, light_primitive_colors)
                dark_actual = resolve_color_value(dark_value_for_name, dark_primitive_colors)
            
            # 直接使用当前值（已经是颜色值）
            xml_content += f'        <item name="{attr_name}">{value}</item>\n'
    
    xml_content += '    </style>\n'
    
    return xml_content


def generate_combined_theme_xml(light_colors: Dict[str, str],
                               dark_colors: Dict[str, str],
                               output_path: str,
                               light_theme_name: str,
                               dark_theme_name: str,
                               light_parent_theme: str,
                               dark_parent_theme: str,
                               light_primitive_colors: Dict[str, str],
                               dark_primitive_colors: Dict[str, str]) -> None:
    """生成合并的主题XML文件，包含日间和夜间两个主题
    
    Args:
        light_colors: 日间颜色字典
        dark_colors: 夜间颜色字典
        output_path: 输出文件路径
        light_theme_name: 日间主题名称
        dark_theme_name: 夜间主题名称
        light_parent_theme: 日间父主题名称
        dark_parent_theme: 夜间父主题名称
        light_primitive_colors: 日间模式原子颜色映射
        dark_primitive_colors: 夜间模式原子颜色映射
    """
    xml_content = '<?xml version="1.0" encoding="utf-8"?>\n'
    xml_content += '<resources>\n'
    xml_content += '\n'
    
    # 生成日间主题
    xml_content += generate_theme_style(
        light_colors, light_parent_theme, light_theme_name,
        light_colors, dark_colors,
        light_primitive_colors, dark_primitive_colors, is_dark_mode=False
    )
    
    xml_content += '\n'
    
    # 生成夜间主题
    xml_content += generate_theme_style(
        dark_colors, dark_parent_theme, dark_theme_name,
        light_colors, dark_colors,
        light_primitive_colors, dark_primitive_colors, is_dark_mode=True
    )
    
    xml_content += '</resources>'
    
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
    
    # 写入文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    
    print(f"Generated: {output_path}")
    print(f"  - Light theme: {light_theme_name} (parent: {light_parent_theme})")
    print(f"  - Dark theme: {dark_theme_name} (parent: {dark_parent_theme})")
    print(f"  - Total color items per theme: {len(light_colors)}")


def extract_comment(color_element) -> str:
    """从XML元素中提取注释（如果存在）"""
    # 这个函数主要用于处理行内注释，但ET不直接支持
    # 我们将在后续版本中改进
    return ""


def clean_color_value(value: str) -> str:
    """清理颜色值，移除注释
    
    Args:
        value: 原始颜色值（可能包含注释）
        
    Returns:
        清理后的颜色值
    """
    # 移除行内注释
    if '<!--' in value:
        value = value[:value.index('<!--')].strip()
    
    return value


def main():
    # 配置
    light_color_file = "values/semantic_color.xml"
    dark_color_file = "values-night/semantic_color.xml"
    
    # 原子颜色文件路径
    light_primitive_file = "values/primitive_color.xml"
    dark_primitive_file = "values-night/primitive_color.xml"
    
    output_dir = "values"
    attrs_file = os.path.join(output_dir, "semantic_color_attrs.xml")
    theme_file = os.path.join(output_dir, "themes.xml")  # 合并到一个文件
    
    # 检查输入文件是否存在
    if not os.path.exists(light_color_file):
        print(f"Error: Light mode color file not found: {light_color_file}")
        return
    
    if not os.path.exists(dark_color_file):
        print(f"Error: Dark mode color file not found: {dark_color_file}")
        return
    
    print("Parsing semantic color files...")
    
    # 解析日间和夜间模式的颜色文件
    light_colors = parse_color_xml(light_color_file)
    dark_colors = parse_color_xml(dark_color_file)
    
    print(f"Light mode colors: {len(light_colors)}")
    print(f"Dark mode colors: {len(dark_colors)}")
    
    # 解析原子颜色文件
    print("\nParsing primitive color files...")
    light_primitive_colors = {}
    dark_primitive_colors = {}
    
    if os.path.exists(light_primitive_file):
        light_primitive_colors = parse_color_xml(light_primitive_file)
        print(f"Light mode primitive colors: {len(light_primitive_colors)}")
    else:
        print(f"Warning: Light mode primitive color file not found: {light_primitive_file}")
    
    if os.path.exists(dark_primitive_file):
        dark_primitive_colors = parse_color_xml(dark_primitive_file)
        print(f"Dark mode primitive colors: {len(dark_primitive_colors)}")
    else:
        print(f"Warning: Dark mode primitive color file not found: {dark_primitive_file}")
    
    # 获取所有颜色名称（使用日间模式的名称作为基准）
    color_names = list(light_colors.keys())
    
    # 验证夜间模式是否包含所有颜色
    missing_in_dark = set(light_colors.keys()) - set(dark_colors.keys())
    if missing_in_dark:
        print(f"\nWarning: {len(missing_in_dark)} colors missing in dark mode:")
        for name in sorted(missing_in_dark):
            print(f"  - {name}")
    
    # 生成属性定义文件
    print("\nGenerating attribute definitions...")
    generate_attrs_xml(color_names, attrs_file)
    
    # 生成合并的主题文件（包含日间和夜间两个主题）
    print("\nGenerating combined theme file...")
    generate_combined_theme_xml(
        light_colors=light_colors,
        dark_colors=dark_colors,
        output_path=theme_file,
        light_theme_name="AUIAppTheme",
        dark_theme_name="TintAUIAppTheme",
        light_parent_theme="Theme.MaterialComponents.DayNight.NoActionBar.Bridge",
        dark_parent_theme="Theme.MaterialComponents.DayNight.NoActionBar.Bridge",
        light_primitive_colors=light_primitive_colors,
        dark_primitive_colors=dark_primitive_colors
    )
    
    print("\n" + "="*60)
    print("Generation completed successfully!")
    print("="*60)
    print("\nGenerated files:")
    print(f"  1. Attributes: {attrs_file}")
    print(f"  2. Themes: {theme_file}")
    print("\nTheme names:")
    print("  - Light theme: AppLightTheme (parent: AppTheme)")
    print("  - Dark theme: AppDarkTheme (parent: TintAppTheme)")
    print("\nUsage:")
    print("  1. 在你的应用主题中继承这些主题")
    print("  2. 在代码中使用 ?attr/颜色属性名 来引用颜色")
    print(f"     例如: ?attr/{to_camel_case('border_primary')}")
    print("\nExample:")
    print("  <style name=\"MyAppTheme.Light\" parent=\"AppLightTheme\">")
    print("      <!-- 你的其他主题属性 -->")
    print("  </style>")
    print("\n  <style name=\"MyAppTheme.Dark\" parent=\"AppDarkTheme\">")
    print("      <!-- 你的其他主题属性 -->")
    print("  </style>")


if __name__ == '__main__':
    main()
