#!/usr/bin/env python3
"""
解析设计令牌JSON文件，生成Android平台日夜间模式的颜色XML文件
"""

import json
import os
import re
from typing import Dict, Any, List, Tuple, Optional, Union, Set


def load_json_file(file_path: str) -> Dict[str, Any]:
    """加载JSON文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def is_color_node(node: Dict[str, Any]) -> bool:
    """判断是否为颜色节点"""
    return node.get('type') == 'color' and 'value' in node


def is_light_mode(node_name: str) -> bool:
    """判断是否为日间模式节点"""
    return 'light mode' in node_name.lower()


def should_include_in_light(node_name: str) -> bool:
    """判断是否应该包含在日间模式XML中"""
    return 'light mode' in node_name.lower() or 'light mode' not in node_name.lower()


def should_include_in_dark(node_name: str) -> bool:
    """判断是否应该包含在夜间模式XML中"""
    return 'dark mode' in node_name.lower() or 'light mode' not in node_name.lower()


def extract_color_value(value: str) -> str:
    """提取颜色值，去掉透明度"""
    if len(value) == 9:  # #RRGGBBAA格式
        return value[:7]
    return value


def format_xml_name(name_parts: List[str], existing_names: Optional[Set[str]] = None) -> str:
    """格式化XML名称，将路径转换为下划线分隔的小写名称
    
    Args:
        name_parts: 路径部分列表
        existing_names: 已存在的名称集合，用于检测冲突
    
    Returns:
        格式化后的XML名称
    """
    # 清理名称，移除特殊字符和空格
    cleaned_parts = []
    bracket_content = None
    
    for part in name_parts:
        # 提取括号内的数字（如果存在）
        bracket_match = re.search(r'\(([^)]+)\)', part)
        if bracket_match:
            extracted_content = bracket_match.group(1).strip()
            # 检查括号内是否是纯数字
            if extracted_content.isdigit():
                # 保留数字信息，稍后判断是否需要使用
                bracket_content = extracted_content
            # 移除括号整体
            part_without_bracket = re.sub(r'\s*\([^)]*\)', '', part)
        else:
            part_without_bracket = part
        
        # 替换空格和特殊字符为下划线
        part_clean = re.sub(r'[^a-zA-Z0-9]', '_', part_without_bracket)
        # 移除连续的下划线
        part_clean = re.sub(r'_+', '_', part_clean)
        # 移除开头和结尾的下划线
        part_clean = part_clean.strip('_')
        
        if part_clean:
            cleaned_parts.append(part_clean.lower())

    # 移除 'colors' 前缀（如果存在）
    if cleaned_parts and cleaned_parts[0] == 'colors':
        cleaned_parts = cleaned_parts[1:]
    
    # 移除 'base' 前缀（如果存在）
    if cleaned_parts and cleaned_parts[0] == 'base':
        cleaned_parts = cleaned_parts[1:]
    
    # 移除 'component colors' 前缀（如果存在）
    if cleaned_parts and cleaned_parts[0] == 'component':
        cleaned_parts = cleaned_parts[1:]
    if len(cleaned_parts) > 1 and cleaned_parts[0] == 'colors':
        cleaned_parts = cleaned_parts[1:]
    
    # 只有节点名是纯数字的时候保留父节点的名称
    if len(cleaned_parts) > 1 and cleaned_parts[-1].isdigit():
        color_name = f"{cleaned_parts[-2]}_{cleaned_parts[-1]}"
        return color_name
    
    # 否则只使用最后一个节点名
    if len(cleaned_parts) > 1:
        base_name = cleaned_parts[-1]
    else:
        base_name = '_'.join(cleaned_parts)
    
    # 检查是否需要添加括号内的数字（只有在名称冲突时才添加）
    if bracket_content and existing_names is not None:
        # 如果基础名称已经存在，则添加括号内的数字以避免冲突
        if base_name in existing_names:
            return f"{base_name}_{bracket_content}"
    
    return base_name


def extract_content_between_spacing_and_bracket(input_string: str) -> str:
    """
    提取字符串中spacing字符前一个点号到最后一个左括号之间的内容
    并将spacing后面的第一个点号替换成下划线，移除其他点号
    
    例如: "primitives.mode 1.spacing.0 (0px)" -> "spacing_0"
    例如: "primitives.mode 1.spacing.large.value (24px)" -> "spacing_largevalue"
    
    Args:
        input_string (str): 输入字符串
    
    Returns:
        str: 提取的内容，如果找不到则返回空字符串
    """
    # 找到最后一个左括号的位置
    last_bracket_pos = input_string.rfind('(')
    if last_bracket_pos == -1:
        return ""
    
    # 找到spacing字符的位置
    spacing_pos = input_string.find('spacing')
    if spacing_pos == -1:
        return ""
    
    # 找到spacing前一个点号的位置
    # 从spacing位置向前查找点号
    dot_before_spacing_pos = -1
    for i in range(spacing_pos - 1, -1, -1):
        if input_string[i] == '.':
            dot_before_spacing_pos = i + 1  # 从点号后面一位开始
            break
    
    if dot_before_spacing_pos == -1:
        return ""
    
    # 提取内容 (从点号后一位到最后一个左括号前)
    content = input_string[dot_before_spacing_pos:last_bracket_pos].strip()
    
    # 将spacing后面的第一个点号替换成下划线，移除其他点号
    spacing_index = content.find('spacing')
    if spacing_index != -1:
        # 找到spacing后面的内容
        after_spacing = content[spacing_index + len('spacing'):]
        # 如果spacing后面有内容
        if after_spacing:
            # 找到第一个点号
            first_dot_pos = after_spacing.find('.')
            if first_dot_pos != -1:
                # 将第一个点号替换成下划线，移除其他点号
                before_first_dot = after_spacing[:first_dot_pos]
                after_first_dot = after_spacing[first_dot_pos + 1:].replace('.', '')
                processed_after_spacing = before_first_dot + '_' + after_first_dot
            else:
                # 没有点号，保持原样
                processed_after_spacing = after_spacing
            
            content = 'spacing' + processed_after_spacing
    
    return content


def format_spacing_name(name_parts: List[str]) -> str:
    """格式化spacing尺寸名称，采用节点属性+父节点名"""
    if not name_parts:
        return "unknown"
    
    # 获取最后一个节点名
    last_part = name_parts[-1]
    
    # 如果节点名有空格，使用空格前的名字
    if ' ' in last_part:
        node_name = last_part.split(' ')[0]
    else:
        node_name = last_part
    
    # 清理节点名，移除特殊字符
    node_name = re.sub(r'[^a-zA-Z0-9]', '', node_name)
    
    # 如果有父节点，使用父节点名
    if len(name_parts) > 1:
        parent_part = name_parts[-2]
        # 清理父节点名
        parent_part = re.sub(r'[^a-zA-Z0-9]', '', parent_part)
        return f"{parent_part}_{node_name}"
    
    return node_name


def is_dimension_node(node: Dict[str, Any]) -> bool:
    """判断是否为尺寸节点"""
    return node.get('type') == 'dimension' and 'value' in node


def traverse_primitive_colors(data: Dict[str, Any], path: List[str],
                              light_colors: Dict[str, str],
                              dark_colors: Dict[str, str]) -> None:
    """遍历primitives模块中的颜色"""
    for key, value in data.items():
        current_path = path + [key]

        if isinstance(value, dict):
            if is_color_node(value):
                # 这是一个颜色节点
                color_value = extract_color_value(value['value'])
                xml_name = format_xml_name(current_path)

                # 根据路径判断是否包含light/dark mode
                path_str = ' '.join(current_path).lower()

                # 特殊处理 gray 颜色
                if 'gray' in path_str:
                    if 'light mode' in path_str:
                        light_colors[xml_name] = color_value
                    elif 'dark mode' in path_str:
                        dark_colors[xml_name] = color_value
                    else:
                        # 如果没有明确指定模式，同时添加到两个集合
                        light_colors[xml_name] = color_value
                        dark_colors[xml_name] = color_value
                else:
                    # 其他颜色按原来的逻辑处理
                    if should_include_in_light(path_str):
                        light_colors[xml_name] = color_value

                    if should_include_in_dark(path_str):
                        dark_colors[xml_name] = color_value
            else:
                # 继续递归
                traverse_primitive_colors(value, current_path, light_colors, dark_colors)


def traverse_spacing_dimensions(data: Dict[str, Any], path: List[str],
                               dimensions: List[Tuple[str, int]]) -> None:
    """遍历primitives模块中的spacing尺寸，保持节点访问顺序"""
    for key, value in data.items():
        current_path = path + [key]

        if isinstance(value, dict):
            if is_dimension_node(value):
                # 这是一个尺寸节点
                dimension_value = value['value']
                xml_name = format_spacing_name(current_path)
                dimensions.append((xml_name, dimension_value))
            else:
                # 继续递归
                traverse_spacing_dimensions(value, current_path, dimensions)


def generate_android_xml(colors: Dict[str, Union[str, Tuple[str, str]]], output_path: str, file_name: str) -> None:
    """生成Android XML文件
    
    Args:
        colors: 颜色字典，值可以是字符串（颜色值或引用）或元组（颜色值，注释）
    """
    xml_content = '<?xml version="1.0" encoding="utf-8"?>\n'
    xml_content += '<resources>\n'

    # 按名称排序
    for name in sorted(colors.keys()):
        color_data = colors[name]
        
        # 检查是否包含注释（跨模式引用的情况）
        if isinstance(color_data, tuple):
            color_value, comment = color_data
            xml_content += f'    <color name="{name}">{color_value}</color>{comment}\n'
        else:
            xml_content += f'    <color name="{name}">{color_data}</color>\n'

    xml_content += '</resources>'

    # 确保输出目录存在
    os.makedirs(output_path, exist_ok=True)

    # 写入文件
    file_path = os.path.join(output_path, file_name)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(xml_content)

    print(f"Generated: {file_path}")


def generate_dimens_xml(dimensions: Dict[str, int], output_path: str, file_name: str) -> None:
    """生成Android dimens.xml文件"""
    xml_content = '<?xml version="1.0" encoding="utf-8"?>\n'
    xml_content += '<resources>\n'

    # 按名称排序
    for name in sorted(dimensions.keys()):
        xml_content += f'    <dimen name="{name}">{dimensions[name]}dp</dimen>\n'

    xml_content += '</resources>'

    # 确保输出目录存在
    os.makedirs(output_path, exist_ok=True)

    # 写入文件
    file_path = os.path.join(output_path, file_name)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(xml_content)

    print(f"Generated: {file_path}")


def generate_ordered_dimens_xml(dimensions: List[Tuple[str, int]], output_path: str, file_name: str) -> None:
    """生成Android dimens.xml文件，保持节点访问顺序"""
    xml_content = '<?xml version="1.0" encoding="utf-8"?>\n'
    xml_content += '<resources>\n'

    # 按照节点访问顺序生成，不排序
    for name, value in dimensions:
        xml_content += f'    <dimen name="{name}">{value}dp</dimen>\n'

    xml_content += '</resources>'

    # 确保输出目录存在
    os.makedirs(output_path, exist_ok=True)

    # 写入文件
    file_path = os.path.join(output_path, file_name)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(xml_content)

    print(f"Generated: {file_path}")


def generate_ordered_semantic_dimens_xml(dimensions: List[Tuple[str, str]], output_path: str, file_name: str) -> None:
    """生成Android语义dimens.xml文件，保持节点访问顺序"""
    xml_content = '<?xml version="1.0" encoding="utf-8"?>\n'
    xml_content += '<resources>\n'

    # 按照节点访问顺序生成，不排序
    for name, reference in dimensions:
        xml_content += f'    <dimen name="{name}">@dimen/{reference}</dimen>\n'

    xml_content += '</resources>'

    # 确保输出目录存在
    os.makedirs(output_path, exist_ok=True)

    # 写入文件
    file_path = os.path.join(output_path, file_name)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(xml_content)

    print(f"Generated: {file_path}")


def generate_semantic_dimens_xml(dimensions: Dict[str, int], output_path: str, file_name: str) -> None:
    """生成Android dimens.xml文件"""
    xml_content = '<?xml version="1.0" encoding="utf-8"?>\n'
    xml_content += '<resources>\n'

    # 按名称排序
    for name in sorted(dimensions.keys()):
        xml_content += f'    <dimen name="{name}">@dimen/{dimensions[name]}</dimen>\n'

    xml_content += '</resources>'

    # 确保输出目录存在
    os.makedirs(output_path, exist_ok=True)

    # 写入文件
    file_path = os.path.join(output_path, file_name)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(xml_content)

    print(f"Generated: {file_path}")


def process_primitives(data: Dict[str, Any]) -> Tuple[Dict[str, str], Dict[str, str]]:
    """处理primitives模块，提取颜色"""
    light_colors = {}
    dark_colors = {}
    
    print("Extracting primitive colors...")
    traverse_primitive_colors(data['primitives'], [], light_colors, dark_colors)
    
    return light_colors, dark_colors


def process_spacing_dimensions(data: Dict[str, Any]) -> List[Tuple[str, int]]:
    """处理primitives模块中的spacing尺寸"""
    dimensions = []
    
    print("Extracting spacing dimensions...")
    if 'primitives' in data and 'spacing' in data['primitives']:
        traverse_spacing_dimensions(data['primitives']['spacing'], ['spacing'], dimensions)
    else:
        print("Warning: 'spacing' not found in primitives")
    
    return dimensions


def generate_xml_files(light_colors: Dict[str, str], dark_colors: Dict[str, str], 
                      output_dir: str) -> None:
    """生成Android XML文件"""
    print("Generating Android XML files...")
    generate_android_xml(light_colors, os.path.join(output_dir, "values"), "primitive_color.xml")  # type: ignore
    generate_android_xml(dark_colors, os.path.join(output_dir, "values-night"), "primitive_color.xml")  # type: ignore


def resolve_color_reference(reference: str, primitive_color_map: Dict[str, str]) -> Optional[str]:
    """解析颜色引用，从primitive color map中查找对应的颜色值"""
    # 去除开头和结尾的花括号
    if reference.startswith('{') and reference.endswith('}'):
        reference = reference[1:-1]
    
    # 去掉light mode或dark mode
    reference = re.sub(r'\s*\(light mode\)', '', reference)
    reference = re.sub(r'\s*\(dark mode\)', '', reference)
    
    # 以点号分割路径
    path_parts = reference.split('.')
    
    # 移除 'colors' 和 'base' 前缀
    filtered_parts = []
    for part in path_parts:
        if part not in ['colors', 'base']:
            filtered_parts.append(part)
    
    # 如果只剩一个部分，直接使用
    if len(filtered_parts) == 1:
        color_name = filtered_parts[0]
    else:
        # 否则使用最后两部分（处理类似 blue_dark_50 的情况）
        color_name = '_'.join(filtered_parts[-2:])
    
    if color_name and color_name in primitive_color_map:
        return primitive_color_map[color_name]
    
    print(f"Warning: Could not find color for reference '{reference}' -> '{color_name}'")
    return None


def resolve_color_reference_to_name(reference: str, primitive_color_map: Dict[str, str]) -> Tuple[Optional[str], Optional[str]]:
    """解析颜色引用,返回primitive color的名称和模式信息
    
    Returns:
        Tuple[Optional[str], Optional[str]]: (颜色名称, 模式信息) 或 (None, None)
        模式信息可以是 'light mode', 'dark mode' 或 None
    """
    # 去除开头和结尾的花括号
    if reference.startswith('{') and reference.endswith('}'):
        reference = reference[1:-1]
    
    # 处理直接的颜色值(以#开头)
    if reference.startswith('#'):
        return None, None
    
    # 如果引用以 "primitives." 开头,直接解析
    if reference.startswith('primitives.'):
        color_name = resolve_primitives_reference(reference, primitive_color_map)
        # 提取模式信息
        mode_info = extract_mode_from_reference(reference)
        return color_name, mode_info
    
    # 如果引用以 "1. color modes" 开头,需要特殊处理
    elif reference.startswith('1. color modes'):
        # 这种情况引用的是semantic color,我们需要找到它最终的primitive引用
        # 但由于我们的设计,这里应该返回None,让semantic color直接引用primitive
        return None, None
    
    # 其他情况,尝试解析
    else:
        color_name = resolve_primitives_reference(reference, primitive_color_map)
        mode_info = extract_mode_from_reference(reference)
        return color_name, mode_info


def extract_mode_from_reference(reference: str) -> Optional[str]:
    """从引用中提取模式信息
    
    Returns:
        'light mode', 'dark mode' 或 None
    """
    if '(light mode)' in reference.lower():
        return 'light mode'
    elif '(dark mode)' in reference.lower():
        return 'dark mode'
    else:
        return None


def resolve_primitives_reference(reference: str, primitive_color_map: Dict[str, str]) -> Optional[str]:
    """解析primitives引用"""
    # 去掉light mode或dark mode后缀(在括号中的)
    reference = re.sub(r'\s*\(light mode\)', '', reference)
    reference = re.sub(r'\s*\(dark mode\)', '', reference)
    
    # 以点号分割路径
    path_parts = reference.split('.')
    
    # 移除 'primitives', 'colors' 等前缀，但保留 'base'
    filtered_parts = []
    skip_keywords = ['primitives', 'colors', 'light mode', 'dark mode']
    
    for part in path_parts:
        # 跳过需要移除的关键字
        if part in skip_keywords:
            continue
        # 替换空格为下划线（但要在判断后）
        cleaned_part = part.replace(' ', '_')
        if cleaned_part and cleaned_part not in [kw.replace(' ', '_') for kw in skip_keywords]:
            filtered_parts.append(cleaned_part)
    
    # 特殊处理 base 下的颜色（white, black, transparent）
    # 检查是否是 base.white, base.black, base.transparent 这样的结构
    if len(filtered_parts) == 2 and filtered_parts[0] == 'base':
        color_name = filtered_parts[1]
        if color_name in primitive_color_map:
            return color_name
        else:
            print(f"Warning: Base color '{color_name}' not found in primitive_color_map")
    
    # 处理基础颜色（white, black, transparent等）- 兼容没有base前缀的情况
    # 如果最后一个部分是基础颜色，直接使用它
    if filtered_parts and filtered_parts[-1] in ['white', 'black', 'transparent']:
        color_name = filtered_parts[-1]
        if color_name in primitive_color_map:
            return color_name
    
    # 处理只有一个部分的情况
    if len(filtered_parts) == 1:
        color_name = filtered_parts[0]
        if color_name in primitive_color_map:
            return color_name
    
    # 处理颜色名称（如 gray.900, brand.600）
    if len(filtered_parts) >= 2:
        # 最后两部分通常是颜色名和数字（如 brand.600）
        color_name = f"{filtered_parts[-2]}_{filtered_parts[-1]}"
        
        # 检查是否存在
        if color_name in primitive_color_map:
            return color_name
        
        # 如果不存在，尝试其他组合
        # 例如：blue_dark.600 -> blue_dark_600
        if len(filtered_parts) >= 3:
            color_name = f"{filtered_parts[-3]}_{filtered_parts[-2]}_{filtered_parts[-1]}"
            if color_name in primitive_color_map:
                return color_name
    
    # 如果还是找不到，尝试从原始引用中提取
    for i, part in enumerate(filtered_parts):
        if part.isdigit() and i > 0:
            color_name = f"{filtered_parts[i-1]}_{part}"
            if color_name in primitive_color_map:
                return color_name
    
    print(f"Warning: Could not find color name for reference '{reference}'")
    return None  # type: ignore


def get_node_value(json, nodeRef):#
    paths = nodeRef.split(".")[2:]
    v = json.get('1. color modes')
    for path in paths:
        v = v.get(path)
    return v['value']

def traverse_radius_nodes(data: Dict[str, Any], radius_values: Dict[str, str]) -> None:
    """遍历半径节点"""
    for key, value in data.items():
        if isinstance(value, dict) and 'value' in value and value.get('type') == 'dimension':
            # 这是一个半径节点
            radius_value = value['value']
            xml_name = format_xml_name([key])
            radius_values[xml_name] = f"{radius_value}dp"
        elif isinstance(value, dict):
            # 继续递归
            traverse_radius_nodes(value, radius_values)

def generate_radius_xml(radius_values: Dict[str, str], output_dir: str) -> None:
    """生成radius_dimens.xml文件"""
    xml_content = '<?xml version="1.0" encoding="utf-8"?>\n'
    xml_content += '<resources>\n'
    
    for name, value in radius_values.items():
        xml_content += f'    <dimen name="{name}">{value}</dimen>\n'
    
    xml_content += '</resources>'
    
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'radius_dimens.xml')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    print(f"Generated radius_dimens.xml with {len(radius_values)} radius values")

def collect_base_names(data: Dict[str, Any], path: List[str], base_names: Dict[str, int]) -> None:
    """收集所有基础名称（不带括号数字），统计在同一模式下的出现次数"""
    for key, value in data.items():
        current_path = path + [key]
        
        if isinstance(value, dict):
            if 'value' in value and isinstance(value['value'], str):
                # 这是一个颜色节点，计算其基础名称
                # 使用 existing_names=None 来获取不带括号数字的基础名称
                base_name = format_xml_name(current_path, existing_names=None)
                
                # 根据路径判断是light mode还是dark mode，分别统计
                path_str = ' '.join(current_path).lower()
                if 'light mode' in path_str:
                    key_name = f"light:{base_name}"
                elif 'dark mode' in path_str:
                    key_name = f"dark:{base_name}"
                else:
                    key_name = f"unknown:{base_name}"
                
                base_names[key_name] = base_names.get(key_name, 0) + 1
            else:
                # 继续递归
                collect_base_names(value, current_path, base_names)


def traverse_semantic_colors(full_data:Dict[str,Any], data: Dict[str, Any], path: List[str],
                             light_semantic: Dict[str, Union[str, Tuple[str, str]]],
                             dark_semantic: Dict[str, Union[str, Tuple[str, str]]],
                             primitive_color_map: Dict[str, str],
                             light_primitive_map: Dict[str, str],
                             dark_primitive_map: Dict[str, str],
                             existing_names: Optional[Set[str]] = None,
                             light_added_names: Optional[Set[str]] = None,
                             dark_added_names: Optional[Set[str]] = None) -> None:
    """遍历语义颜色节点
    
    Args:
        full_data: 完整的JSON数据
        data: 当前需要遍历的数据
        path: 当前路径
        light_semantic: 日间模式语义颜色字典
        dark_semantic: 夜间模式语义颜色字典
        primitive_color_map: 基础颜色映射（合并的）
        light_primitive_map: 日间模式基础颜色映射
        dark_primitive_map: 夜间模式基础颜色映射
        existing_names: 冲突的基础名称集合
        light_added_names: 日间模式已添加的名称
        dark_added_names: 夜间模式已添加的名称
    """
    if light_added_names is None:
        light_added_names = set()
    if dark_added_names is None:
        dark_added_names = set()
    
    for key, value in data.items():
        current_path = path + [key]
        
        if isinstance(value, dict):
            if 'value' in value and isinstance(value['value'], str):
                # 这是一个颜色节点
                reference = value['value']
                
                # 根据路径判断是light mode还是dark mode
                path_str = ' '.join(current_path).lower()
                is_light_mode = 'light mode' in path_str
                is_dark_mode = 'dark mode' in path_str
                
                # 选择对应模式的 added_names
                current_added_names = light_added_names if is_light_mode else (dark_added_names if is_dark_mode else set())
                
                # 判断是直接的颜色值还是引用
                if reference.startswith('#'):
                    # 直接的颜色值，提取并去掉透明度（如果是8位）
                    color_value = extract_color_value(reference)
                    xml_name = format_xml_name(current_path, current_added_names)
                    
                    if is_light_mode:
                        light_semantic[xml_name] = color_value
                        light_added_names.add(xml_name)
                    elif is_dark_mode:
                        dark_semantic[xml_name] = color_value
                        dark_added_names.add(xml_name)
                else:
                    # 这是一个颜色引用
                    if reference.startswith('{1. color modes'): #说明引用的是color modes下的节点，找到这个节点读取其value属性。
                        reference = get_node_value(full_data, reference[1:-1])
                    primitive_color_name, ref_mode = resolve_color_reference_to_name(reference, primitive_color_map)
                    
                    if primitive_color_name:
                        xml_name = format_xml_name(current_path, current_added_names)
                        
                        # 检查是否存在跨模式引用
                        current_mode = 'light mode' if is_light_mode else 'dark mode'
                        is_cross_mode = ref_mode and ref_mode != current_mode
                        
                        if is_cross_mode:
                            # 跨模式引用：使用直接颜色值而非引用
                            # 从对应模式的primitive map中获取颜色值
                            target_map = dark_primitive_map if ref_mode == 'dark mode' else light_primitive_map
                            if primitive_color_name in target_map:
                                color_value = target_map[primitive_color_name]
                                comment = f"  <!-- {primitive_color_name} ({ref_mode}) -->"
                                
                                if is_light_mode:
                                    light_semantic[xml_name] = (color_value, comment)
                                    light_added_names.add(xml_name)
                                elif is_dark_mode:
                                    dark_semantic[xml_name] = (color_value, comment)
                                    dark_added_names.add(xml_name)
                            else:
                                print(f"Warning: Cross-mode color '{primitive_color_name}' not found in {ref_mode} primitive map")
                        else:
                            # 同模式引用：使用@color引用
                            color_reference = f"@color/{primitive_color_name}"
                            
                            if is_light_mode:
                                light_semantic[xml_name] = color_reference
                                light_added_names.add(xml_name)
                            elif is_dark_mode:
                                dark_semantic[xml_name] = color_reference
                                dark_added_names.add(xml_name)
            else:
                # 继续递归
                traverse_semantic_colors(full_data, value, current_path, light_semantic,
                                         dark_semantic, primitive_color_map, light_primitive_map,
                                         dark_primitive_map, existing_names, 
                                         light_added_names, dark_added_names)


def process_color_modes(data: Dict[str, Any], primitive_color_map: Dict[str, str],
                       light_primitive_map: Dict[str, str],
                       dark_primitive_map: Dict[str, str]) -> Tuple[Dict[str, Union[str, Tuple[str, str]]], Dict[str, Union[str, Tuple[str, str]]]]:
    """处理color modes节点，提取语义颜色"""
    light_semantic = {}
    dark_semantic = {}
    
    # 检查可能的color modes键名
    color_modes_key = None
    for key in data.keys():
        if 'color modes' in key.lower():
            color_modes_key = key
            break
    
    if color_modes_key is None:
        print("Warning: 'color modes' not found in JSON")
        return light_semantic, dark_semantic
    
    print("Processing semantic colors...")
    
    # 第一步：收集所有基础名称，统计在同一模式下的出现次数
    base_names = {}
    collect_base_names(data[color_modes_key], [], base_names)
    
    # 找出每个模式下出现多次的名称（需要解决冲突）
    conflicting_names = set()
    for key_name, count in base_names.items():
        if count > 1:
            # 提取基础名称（去掉 light: 或 dark: 前缀）
            if ':' in key_name:
                base_name = key_name.split(':', 1)[1]
                conflicting_names.add(base_name)
                # 调试输出
                # print(f"Conflict detected: {key_name} (count: {count}) -> {base_name}")
    
    # 第二步：遍历并生成颜色，传入冲突名称集合和分离的primitive maps
    traverse_semantic_colors(data, data[color_modes_key], [], light_semantic,
                           dark_semantic, primitive_color_map, light_primitive_map,
                           dark_primitive_map, conflicting_names)
    
    return light_semantic, dark_semantic


def generate_semantic_xml_files(light_semantic: Dict[str, Union[str, Tuple[str, str]]], 
                               dark_semantic: Dict[str, Union[str, Tuple[str, str]]], 
                               output_dir: str) -> None:
    """生成语义颜色XML文件"""
    print("Generating semantic color XML files...")
    generate_android_xml(light_semantic, os.path.join(output_dir, "values"), "semantic_color.xml")
    generate_android_xml(dark_semantic, os.path.join(output_dir, "values-night"), "semantic_color.xml")


def print_summary(light_colors: Dict[str, str], dark_colors: Dict[str, str],
                  light_semantic: Dict[str, Union[str, Tuple[str, str]]], 
                  dark_semantic: Dict[str, Union[str, Tuple[str, str]]],
                  output_dir: str) -> None:
    """打印处理结果摘要"""
    print(f"\nSummary:")
    print(f"Light mode primitive colors: {len(light_colors)}")
    print(f"Dark mode primitive colors: {len(dark_colors)}")
    print(f"Light mode semantic colors: {len(light_semantic)}")
    print(f"Dark mode semantic colors: {len(dark_semantic)}")
    print(f"Output directory: {output_dir}")


def process_semantic_spacing(data:Dict[str,Any]):
    semantic_dimens = []
    spacing_node = data['3. spacing']
    for k,v in spacing_node.items():
        spacing_name = k
        reference_name = extract_content_between_spacing_and_bracket(v['value'][1:-1])
        semantic_dimens.append((str.replace(spacing_name,"-","_"), reference_name))

    return semantic_dimens

def main():
    # JSON文件路径
    json_file = "design-tokens.tokens(1).json"

    # 输出目录 - 使用当前目录
    output_dir = "."

    # 加载JSON文件
    print("Loading JSON file...")
    try:
        data = load_json_file(json_file)
    except FileNotFoundError:
        print(f"Error: File not found: {json_file}")
        return
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return

    # 检查是否有primitives模块
    if 'primitives' not in data:
        print("Error: 'primitives' module not found in JSON")
        return

    # 处理primitives模块
    light_colors, dark_colors = process_primitives(data)
    
    # 创建primitive color map，合并light和dark模式的所有颜色
    primitive_color_map = {}
    primitive_color_map.update(light_colors)
    primitive_color_map.update(dark_colors)
    
        
    # 处理color modes模块（语义颜色），传入分离的light和dark primitive maps
    light_semantic, dark_semantic = process_color_modes(data, primitive_color_map,
                                                       light_colors, dark_colors)
    
    # 处理spacing尺寸
    dimensions = process_spacing_dimensions(data)
    semantic_dimensions = process_semantic_spacing(data)
    # 处理渐变
    gradients = process_gradients(data)
    # 处理半径
    radius_values = process_radius_data(data)
    # 处理typography
    typography_styles = process_typography_data(data)
    # 处理font sizes
    text_sizes = process_font_sizes(data)

    # 生成XML文件
    generate_xml_files(light_colors, dark_colors, output_dir)
    generate_semantic_xml_files(light_semantic, dark_semantic, output_dir)
    generate_ordered_dimens_xml(dimensions, os.path.join(output_dir, "values"), "dimens.xml")
    generate_ordered_semantic_dimens_xml(semantic_dimensions,os.path.join(output_dir,"values"),"semantic_dimens.xml")
    generate_gradient_xml_files(gradients, output_dir)
    generate_radius_xml(radius_values, os.path.join(output_dir, "values"))
    generate_typography_xml_files(typography_styles, output_dir)
    generate_text_dimens_xml(text_sizes, output_dir)
    
    # 打印摘要
    print_summary(light_colors, dark_colors, light_semantic, dark_semantic, output_dir)
    print(f"Spacing dimensions: {len(dimensions)}")
    print(f"Gradients: {len(gradients)}")
    print(f"Radius values: {len(radius_values)}")
    print(f"Typography styles: {len(typography_styles)}")


def is_gradient_node(node: Dict[str, Any]) -> bool:
    """判断是否为渐变节点"""
    return node.get('type') == 'custom-gradient' and 'value' in node


def format_gradient_name(parent_name: str, node_name: str) -> str:
    """格式化渐变名称，按照命名规则处理"""
    # 处理类似 '600 -> 500 (90deg)' 的情况
    if ' -> ' in node_name and '(' in node_name:
        # 提取箭头前后的数字
        parts = node_name.split(' -> ')
        if len(parts) == 2:
            start_num = parts[0].strip()
            end_part = parts[1].split('(')[0].strip()  # 去掉度数部分
            return f"{parent_name}_{start_num}_{end_part}"
    
    # 其他情况直接拼接
    # 清理名称，移除特殊字符
    parent_clean = re.sub(r'[^a-zA-Z0-9]', '_', parent_name)
    node_clean = re.sub(r'[^a-zA-Z0-9]', '_', node_name)
    
    # 移除连续的下划线
    parent_clean = re.sub(r'_+', '_', parent_clean).strip('_')
    node_clean = re.sub(r'_+', '_', node_clean).strip('_')
    
    return f"{parent_clean}_{node_clean}"


def generate_android_gradient_xml(gradient_name: str, rotation: float, start_color: str, end_color: str) -> str:
    """生成单个Android渐变XML内容"""
    # 确保颜色值格式正确
    if not start_color.startswith('#'):
        start_color = f"#{start_color}"
    if not end_color.startswith('#'):
        end_color = f"#{end_color}"
    
    # 处理8位颜色值（包含透明度）
    if len(start_color) == 9:
        start_color = start_color[:7]  # 去掉透明度
    if len(end_color) == 9:
        end_color = end_color[:7]  # 去掉透明度
    
    xml_content = f'''<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android"
    android:shape="rectangle">
    <gradient
        android:type="linear"
        android:angle="{int(rotation)}"
        android:startColor="{start_color}"
        android:endColor="{end_color}" />
</shape>'''
    
    return xml_content


def traverse_gradient_nodes(data: Dict[str, Any], path: List[str], gradients: Dict[str, Dict[str, Any]]) -> None:
    """遍历渐变节点"""
    for key, value in data.items():
        current_path = path + [key]
        
        if isinstance(value, dict):
            if is_gradient_node(value):
                # 这是一个渐变节点
                gradient_value = value['value']
                rotation = gradient_value.get('rotation', 0)
                stops = gradient_value.get('stops', [])
                
                # 确保有两个停止点
                if len(stops) >= 2:
                    start_color = stops[0]['color']
                    end_color = stops[1]['color']
                    
                    # 生成XML名称
                    if len(current_path) >= 2:
                        parent_name = current_path[-2]  # 父节点名
                        node_name = current_path[-1]    # 当前节点名
                        xml_name = format_gradient_name(parent_name, node_name)
                    else:
                        xml_name = format_gradient_name('gradient', current_path[-1])
                    
                    gradients[xml_name] = {
                        'rotation': rotation,
                        'start_color': start_color,
                        'end_color': end_color
                    }
                    
                    print(f"Found gradient: {xml_name} - {start_color} -> {end_color} ({rotation}°)")
            else:
                # 继续递归
                traverse_gradient_nodes(value, current_path, gradients)


def process_gradients(data: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """处理gradient模块，提取渐变"""
    gradients = {}
    
    if 'gradient' not in data:
        print("Warning: 'gradient' module not found in JSON")
        return gradients
    
    print("Extracting gradients...")
    traverse_gradient_nodes(data['gradient'], [], gradients)
    
    return gradients


def process_radius_data(data: Dict[str, Any]) -> Dict[str, str]:
    """处理radius模块，提取半径值"""
    radius_values = {}
    
    # 检查可能的radius键名
    radius_key = None
    for key in data.keys():
        if 'radius' in key.lower() and key.startswith('2.'):
            radius_key = key
            break
    
    if radius_key is None:
        print("Warning: '2. radius' not found in JSON")
        return radius_values
    
    print("Extracting radius values...")
    traverse_radius_nodes(data[radius_key], radius_values)
    
    return radius_values


def generate_gradient_xml_files(gradients: Dict[str, Dict[str, Any]], output_dir: str) -> None:
    """生成渐变XML文件"""
    gradient_dir = os.path.join(output_dir, "gradients")
    os.makedirs(gradient_dir, exist_ok=True)
    
    print(f"Generating gradient XML files in {gradient_dir}...")
    
    for gradient_name, gradient_data in gradients.items():
        xml_content = generate_android_gradient_xml(
            gradient_name,
            gradient_data['rotation'],
            gradient_data['start_color'],
            gradient_data['end_color']
        )
        
        file_path = os.path.join(gradient_dir, f"{gradient_name}.xml")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(xml_content)
        
        print(f"Generated: {file_path}")


def is_typography_node(node: Dict[str, Any]) -> bool:
    """判断是否为typography节点"""
    return node.get('type') == 'custom-typography' and 'value' in node


def format_typography_name(node_name: str) -> str:
    """格式化typography节点名称，将类似"display 2xl（72）"转换为"display_2xl" """
    # 去掉括号内的内容
    import re
    name = re.sub(r'\s*（[^）]*）', '', node_name)
    name = re.sub(r'\s*\([^)]*\)', '', name)
    
    # 将空格替换为下划线
    name = name.replace(' ', '_')
    
    # 移除特殊字符，只保留字母、数字和下划线
    name = re.sub(r'[^a-zA-Z0-9_]', '_', name)
    
    # 移除连续的下划线
    name = re.sub(r'_+', '_', name)
    
    # 移除开头和结尾的下划线
    name = name.strip('_')
    
    return name.lower()


def extract_typography_value(node_name: str, value_dict: Dict[str, Any]) -> Dict[str, str]:
    """提取typography值，从节点名中提取字体大小"""
    result = {}
    
    # 从节点名中提取字体大小
    import re
    # 匹配括号内的数字，支持中文和英文括号
    size_match = re.search(r'[（(](\d+)[）)]', node_name)
    if size_match:
        size_value = size_match.group(1)
        result['text_size'] = f"{size_value}sp"
    
    # 从value中提取其他属性
    typography_value = value_dict.get('value', {})
    
    # 提取字体粗细
    if 'fontWeight' in typography_value:
        font_weight = typography_value['fontWeight']
        if isinstance(font_weight, str):
            # 将字符串形式的字体粗细转换为数值
            weight_map = {
                'thin': '100',
                'extralight': '200',
                'light': '300',
                'regular': '400',
                'medium': '500',
                'semibold': '600',
                'bold': '700',
                'extrabold': '800',
                'black': '900'
            }
            result['text_weight'] = weight_map.get(font_weight.lower(), '400')
        elif isinstance(font_weight, (int, float)):
            result['text_weight'] = str(int(font_weight))
    
    # 提取行高
    if 'lineHeight' in typography_value:
        line_height = typography_value['lineHeight']
        if isinstance(line_height, dict) and 'value' in line_height:
            line_height_value = line_height['value']
            if isinstance(line_height_value, str):
                # 处理行高值
                if line_height_value.endswith('%'):
                    # 如果是百分比，转换为小数
                    percentage = float(line_height_value.rstrip('%'))
                    result['line_height_multiplier'] = f"{percentage / 100:.2f}"
                else:
                    result['line_height'] = f"{line_height_value}sp"
            elif isinstance(line_height_value, (int, float)):
                result['line_height'] = f"{line_height_value}sp"
        elif isinstance(line_height, str) and line_height.endswith('%'):
            # 处理直接字符串形式的百分比
            percentage = float(line_height.rstrip('%'))
            result['line_height_multiplier'] = f"{percentage / 100:.2f}"
    
    # 提取字母间距
    if 'letterSpacing' in typography_value:
        letter_spacing = typography_value['letterSpacing']
        if isinstance(letter_spacing, dict) and 'value' in letter_spacing:
            spacing_value = letter_spacing['value']
            if isinstance(spacing_value, str):
                result['letter_spacing'] = spacing_value
            elif isinstance(spacing_value, (int, float)):
                result['letter_spacing'] = f"{spacing_value}sp"
        elif isinstance(letter_spacing, (int, float)):
            result['letter_spacing'] = f"{letter_spacing}sp"
    
    return result


def traverse_typography_nodes(data: Dict[str, Any], 
                              typography_styles: Dict[str, Dict[str, str]]) -> None:
    """遍历typography节点下的直接子节点"""
    for key, value in data.items():
        xml_name = format_typography_name(key)
        typography_values = extract_typography_value(key, value)

        if typography_values:
            typography_styles[xml_name] = typography_values
            print(f"Found typography style: {xml_name} - {typography_values}")


def process_typography_data(data: Dict[str, Any]) -> Dict[str, Dict[str, str]]:
    """处理typography模块，提取字体样式"""
    typography_styles = {}
    
    # 精确匹配"typography"节点
    if 'typography' not in data:
        print("Warning: 'typography' not found in JSON")
        return typography_styles
    
    print("Extracting typography styles...")
    traverse_typography_nodes(data['typography'], typography_styles)
    
    return typography_styles


def generate_typography_xml_files(typography_styles: Dict[str, Dict[str, str]], output_dir: str) -> None:
    """生成typography XML文件"""
    if not typography_styles:
        print("No typography styles found, skipping XML generation")
        return

    # 生成text styles XML
    text_styles_content = '<?xml version="1.0" encoding="utf-8"?>\n'
    text_styles_content += '<resources>\n'

    for style_name, style_values in sorted(typography_styles.items()):
        text_styles_content += f'    <style name="{style_name}">\n'

        if 'text_size' in style_values:
            text_styles_content += f'        <item name="android:textSize">{style_values["text_size"]}</item>\n'

        if 'text_weight' in style_values:
            text_styles_content += f'        <item name="android:textStyle">{style_values["text_weight"]}</item>\n'

        if 'line_height' in style_values:
            text_styles_content += f'        <item name="android:lineHeight">{style_values["line_height"]}</item>\n'

        if 'line_height_multiplier' in style_values:
            text_styles_content += f'        <item name="android:lineHeightMultiplier">{style_values["line_height_multiplier"]}</item>\n'

        if 'letter_spacing' in style_values:
            text_styles_content += f'        <item name="android:letterSpacing">{style_values["letter_spacing"]}</item>\n'

        text_styles_content += '    </style>\n'

    text_styles_content += '</resources>'

    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 写入text styles文件
    text_styles_path = os.path.join(output_dir, "values", "text_styles.xml")
    with open(text_styles_path, 'w', encoding='utf-8') as f:
        f.write(text_styles_content)

    print(f"Generated: {text_styles_path}")

    # 生成dimens文件用于字体大小
    dimens_content = '<?xml version="1.0" encoding="utf-8"?>\n'
    dimens_content += '<resources>\n'

    for style_name, style_values in sorted(typography_styles.items()):
        if 'text_size' in style_values:
            # 提取数值部分，去掉sp单位
            size_value = style_values['text_size']
            if size_value.endswith('sp'):
                size_name = f"{style_name}"
                dimens_content += f'    <dimen name="{size_name}">{size_value}</dimen>\n'

    dimens_content += '</resources>'

    dimens_path = os.path.join(output_dir, "values", "text_sizes.xml")
    with open(dimens_path, 'w', encoding='utf-8') as f:
        f.write(dimens_content)

    print(f"Generated: {dimens_path}")

    # 生成README文件
    readme_content = """# Typography Styles

This directory contains Android typography style files generated from design tokens.

## Generated Files

- `values/text_styles.xml` - Text style definitions with all typography properties
- `values/text_sizes.xml` - Text size dimensions for easy reference

## Usage

### In XML:

```xml
<TextView
    style="@style/display_2xl"
    android:text="Sample Text" />
```

### In Kotlin/Java:

```kotlin
textView.setTextAppearance(context, R.style.display_2xl)
```

## Available Styles

"""

    for style_name, style_values in sorted(typography_styles.items()):
        readme_content += f"### {style_name}\n\n"
        readme_content += "**Properties:**\n"

        if 'text_size' in style_values:
            readme_content += f"- Text Size: {style_values['text_size']}\n"

        if 'text_weight' in style_values:
            readme_content += f"- Font Weight: {style_values['text_weight']}\n"

        if 'line_height' in style_values:
            readme_content += f"- Line Height: {style_values['line_height']}\n"

        if 'line_height_multiplier' in style_values:
            readme_content += f"- Line Height Multiplier: {style_values['line_height_multiplier']}\n"

        if 'letter_spacing' in style_values:
            readme_content += f"- Letter Spacing: {style_values['letter_spacing']}\n"

        readme_content += "\n"

    readme_path = os.path.join(output_dir, "typography_readme.md")
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)

    print(f"Generated: {readme_path}")


def traverse_font_size_nodes(font_size_data: Dict[str, Any], text_sizes: Dict[str, int]) -> None:
    """遍历font size节点，提取文字大小"""
    for key, value in font_size_data.items():
        if isinstance(value, dict) and value.get('type') == 'dimension' and 'value' in value:
            # 这是一个字体大小节点
            size_value = value['value']

            # 从节点名中提取text-后面的内容作为名称
            if key.startswith('text-'):
                xml_name = key[5:]  # 去掉'text-'前缀
            else:
                xml_name = key

            # 清理名称，将连字符替换为下划线
            xml_name = xml_name.replace('-', '_')

            text_sizes[xml_name] = size_value
            print(f"Found font size: {xml_name} = {size_value}sp")


def process_font_sizes(data: Dict[str, Any]) -> Dict[str, int]:
    """处理font size节点，提取文字大小"""
    text_sizes = {}

    # 查找"6. typography"节点
    typography_key = None
    for key in data.keys():
        if key == '6. typography':
            typography_key = key
            break

    if typography_key is None:
        print("Warning: '6. typography' not found in JSON")
        return text_sizes

    # 查找"font size"节点
    typography_data = data[typography_key]
    if 'font size' not in typography_data:
        print("Warning: 'font size' not found in typography")
        return text_sizes

    print("Extracting font sizes...")
    traverse_font_size_nodes(typography_data['font size'], text_sizes)

    return text_sizes


def generate_text_dimens_xml(text_sizes: Dict[str, int], output_dir: str) -> None:
    """生成text_dimens.xml文件，包含所有文字大小"""
    xml_content = '<?xml version="1.0" encoding="utf-8"?>\n'
    xml_content += '<resources>\n'

    # 按名称排序
    for name in sorted(text_sizes.keys()):
        xml_content += f'    <dimen name="{name}">{text_sizes[name]}sp</dimen>\n'

    xml_content += '</resources>'

    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 写入文件
    file_path = os.path.join(output_dir, "values", "text_dimens.xml")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(xml_content)

    print(f"Generated: {file_path}")


if __name__ == "__main__":
    main()