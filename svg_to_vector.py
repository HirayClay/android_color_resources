#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SVG to Android Vector Drawable Converter
将SVG文件转换为Android Vector Drawable格式
"""

import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path
import argparse
from typing import Dict, List, Optional, Tuple


class SvgToVectorConverter:
    """SVG转Android Vector Drawable转换器"""
    
    def __init__(self):
        # SVG命名空间
        self.svg_ns = {
            '': 'http://www.w3.org/2000/svg',
            'svg': 'http://www.w3.org/2000/svg'
        }
        
        # 支持的SVG元素到Vector Drawable的映射
        self.element_mapping = {
            'path': 'path',
            'rect': 'path',
            'circle': 'path',
            'ellipse': 'path',
            'line': 'path',
            'polyline': 'path',
            'polygon': 'path'
        }
    
    def parse_svg_viewbox(self, svg_root: ET.Element) -> Tuple[float, float, float, float]:
        """解析SVG的viewBox属性"""
        viewbox = svg_root.get('viewBox')
        if viewbox:
            values = [float(x) for x in viewbox.split()]
            return tuple(values)
        
        # 如果没有viewBox，尝试从width和height获取
        width = svg_root.get('width', '24')
        height = svg_root.get('height', '24')
        
        # 移除单位
        width = re.sub(r'[^\d.-]', '', str(width))
        height = re.sub(r'[^\d.-]', '', str(height))
        
        try:
            w = float(width) if width else 24
            h = float(height) if height else 24
            return (0, 0, w, h)
        except ValueError:
            return (0, 0, 24, 24)
    
    def convert_color(self, color: str) -> str:
        """转换颜色格式"""
        if not color or color == 'none':
            return '#00000000'  # 透明
        
        if color.startswith('#'):
            # 确保颜色是8位格式 (#AARRGGBB)
            if len(color) == 4:  # #RGB
                color = '#' + ''.join([c*2 for c in color[1:]])
            if len(color) == 7:  # #RRGGBB
                color = '#FF' + color[1:]  # 添加Alpha通道
            return color
        
        # 处理命名颜色
        named_colors = {
            'black': '#FF000000',
            'white': '#FFFFFFFF',
            'red': '#FFFF0000',
            'green': '#FF00FF00',
            'blue': '#FF0000FF',
            'transparent': '#00000000'
        }
        
        return named_colors.get(color.lower(), '#FF000000')
    
    def rect_to_path(self, element: ET.Element) -> str:
        """将rect元素转换为path数据"""
        x = float(element.get('x', 0))
        y = float(element.get('y', 0))
        width = float(element.get('width', 0))
        height = float(element.get('height', 0))
        rx = float(element.get('rx', 0))
        ry = float(element.get('ry', 0))
        
        if rx == 0 and ry == 0:
            # 普通矩形
            return f"M{x},{y} L{x+width},{y} L{x+width},{y+height} L{x},{y+height} Z"
        else:
            # 圆角矩形
            if ry == 0:
                ry = rx
            if rx == 0:
                rx = ry
            
            return (f"M{x+rx},{y} "
                   f"L{x+width-rx},{y} "
                   f"Q{x+width},{y} {x+width},{y+ry} "
                   f"L{x+width},{y+height-ry} "
                   f"Q{x+width},{y+height} {x+width-rx},{y+height} "
                   f"L{x+rx},{y+height} "
                   f"Q{x},{y+height} {x},{y+height-ry} "
                   f"L{x},{y+ry} "
                   f"Q{x},{y} {x+rx},{y} Z")
    
    def circle_to_path(self, element: ET.Element) -> str:
        """将circle元素转换为path数据"""
        cx = float(element.get('cx', 0))
        cy = float(element.get('cy', 0))
        r = float(element.get('r', 0))
        
        # 使用贝塞尔曲线绘制圆
        return (f"M{cx-r},{cy} "
               f"C{cx-r},{cy-0.552*r} {cx-0.552*r},{cy-r} {cx},{cy-r} "
               f"C{cx+0.552*r},{cy-r} {cx+r},{cy-0.552*r} {cx+r},{cy} "
               f"C{cx+r},{cy+0.552*r} {cx+0.552*r},{cy+r} {cx},{cy+r} "
               f"C{cx-0.552*r},{cy+r} {cx-r},{cy+0.552*r} {cx-r},{cy} Z")
    
    def ellipse_to_path(self, element: ET.Element) -> str:
        """将ellipse元素转换为path数据"""
        cx = float(element.get('cx', 0))
        cy = float(element.get('cy', 0))
        rx = float(element.get('rx', 0))
        ry = float(element.get('ry', 0))
        
        # 使用贝塞尔曲线绘制椭圆
        return (f"M{cx-rx},{cy} "
               f"C{cx-rx},{cy-0.552*ry} {cx-0.552*rx},{cy-ry} {cx},{cy-ry} "
               f"C{cx+0.552*rx},{cy-ry} {cx+rx},{cy-0.552*ry} {cx+rx},{cy} "
               f"C{cx+rx},{cy+0.552*ry} {cx+0.552*rx},{cy+ry} {cx},{cy+ry} "
               f"C{cx-0.552*rx},{cy+ry} {cx-rx},{cy+0.552*ry} {cx-rx},{cy} Z")
    
    def line_to_path(self, element: ET.Element) -> str:
        """将line元素转换为path数据"""
        x1 = float(element.get('x1', 0))
        y1 = float(element.get('y1', 0))
        x2 = float(element.get('x2', 0))
        y2 = float(element.get('y2', 0))
        
        return f"M{x1},{y1} L{x2},{y2}"
    
    def polyline_to_path(self, element: ET.Element) -> str:
        """将polyline元素转换为path数据"""
        points = element.get('points', '')
        if not points:
            return ""
        
        # 解析点坐标
        coords = re.findall(r'[\d.-]+', points)
        if len(coords) < 4:
            return ""
        
        path_data = f"M{coords[0]},{coords[1]}"
        for i in range(2, len(coords), 2):
            if i + 1 < len(coords):
                path_data += f" L{coords[i]},{coords[i+1]}"
        
        return path_data
    
    def polygon_to_path(self, element: ET.Element) -> str:
        """将polygon元素转换为path数据"""
        path_data = self.polyline_to_path(element)
        if path_data:
            path_data += " Z"
        return path_data
    
    def element_to_path_data(self, element: ET.Element) -> str:
        """将SVG元素转换为path数据"""
        tag = element.tag.split('}')[-1] if '}' in element.tag else element.tag
        
        if tag == 'path':
            return element.get('d', '')
        elif tag == 'rect':
            return self.rect_to_path(element)
        elif tag == 'circle':
            return self.circle_to_path(element)
        elif tag == 'ellipse':
            return self.ellipse_to_path(element)
        elif tag == 'line':
            return self.line_to_path(element)
        elif tag == 'polyline':
            return self.polyline_to_path(element)
        elif tag == 'polygon':
            return self.polygon_to_path(element)
        
        return ""
    
    def process_svg_element(self, element: ET.Element, group_element: ET.Element):
        """处理SVG元素并添加到group中"""
        tag = element.tag.split('}')[-1] if '}' in element.tag else element.tag
        
        if tag in self.element_mapping:
            # 转换为path元素
            path_data = self.element_to_path_data(element)
            if path_data:
                path_elem = ET.SubElement(group_element, 'path')
                path_elem.set('android:pathData', path_data)
                
                # 处理颜色属性
                fill = element.get('fill')
                stroke = element.get('stroke')
                stroke_width = element.get('stroke-width')
                
                if fill and fill != 'none':
                    path_elem.set('android:fillColor', self.convert_color(fill))
                
                if stroke and stroke != 'none':
                    path_elem.set('android:strokeColor', self.convert_color(stroke))
                    if stroke_width:
                        path_elem.set('android:strokeWidth', stroke_width)
        
        elif tag == 'g':
            # 处理group元素
            group = ET.SubElement(group_element, 'group')
            
            # 处理transform属性
            transform = element.get('transform')
            if transform:
                # 简单处理translate transform
                translate_match = re.search(r'translate\(([^)]+)\)', transform)
                if translate_match:
                    coords = translate_match.group(1).split(',')
                    if len(coords) >= 2:
                        group.set('android:translateX', coords[0].strip())
                        group.set('android:translateY', coords[1].strip())
            
            # 递归处理子元素
            for child in element:
                self.process_svg_element(child, group)
        
        else:
            # 递归处理其他容器元素
            for child in element:
                self.process_svg_element(child, group_element)
    
    def convert_svg_to_vector(self, svg_file_path: str, output_dir: str) -> bool:
        """将SVG文件转换为Android Vector Drawable"""
        try:
            # 解析SVG文件
            tree = ET.parse(svg_file_path)
            root = tree.getroot()
            
            # 获取文件名（不含扩展名）
            svg_filename = Path(svg_file_path).stem
            
            # 解析viewBox
            min_x, min_y, width, height = self.parse_svg_viewbox(root)
            
            # 创建Vector Drawable根元素
            vector = ET.Element('vector')
            vector.set('xmlns:android', 'http://schemas.android.com/apk/res/android')
            vector.set('android:width', f'{int(width)}dp')
            vector.set('android:height', f'{int(height)}dp')
            vector.set('android:viewportWidth', str(width))
            vector.set('android:viewportHeight', str(height))
            
            # 处理SVG元素
            for element in root:
                self.process_svg_element(element, vector)
            
            # 如果没有子元素，可能需要直接处理root的子元素
            if len(vector) == 0:
                # 查找所有绘制元素
                for element in root.iter():
                    tag = element.tag.split('}')[-1] if '}' in element.tag else element.tag
                    if tag in self.element_mapping:
                        self.process_svg_element(element, vector)
            
            # 生成XML内容
            xml_content = self.format_xml(vector)
            
            # 保存文件
            output_file = os.path.join(output_dir, f'{svg_filename}.xml')
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(xml_content)
            
            print(f"✓ 已转换: {svg_filename}.svg -> {svg_filename}.xml")
            return True
            
        except Exception as e:
            print(f"✗ 转换失败 {svg_file_path}: {str(e)}")
            return False
    
    def format_xml(self, element: ET.Element) -> str:
        """格式化XML输出"""
        # 使用ET生成基础XML
        rough_string = ET.tostring(element, encoding='unicode')
        
        # 手动格式化以获得更好的缩进
        lines = []
        lines.append('<?xml version="1.0" encoding="utf-8"?>')
        
        def format_element(elem, indent=0):
            """递归格式化元素"""
            indent_str = '    ' * indent
            
            # 开始标签
            attrs = []
            for key, value in elem.attrib.items():
                attrs.append(f'{key}="{value}"')
            
            if attrs:
                if len(attrs) == 1:
                    tag_line = f'{indent_str}<{elem.tag} {attrs[0]}'
                else:
                    tag_line = f'{indent_str}<{elem.tag}'
                    for attr in attrs:
                        tag_line += f'\n{indent_str}    {attr}'
            else:
                tag_line = f'{indent_str}<{elem.tag}'
            
            # 检查是否有子元素
            if len(elem) > 0:
                lines.append(tag_line + '>')
                for child in elem:
                    format_element(child, indent + 1)
                lines.append(f'{indent_str}</{elem.tag}>')
            else:
                lines.append(tag_line + ' />')
        
        format_element(element)
        return '\n'.join(lines)
    
    def convert_directory(self, svg_dir: str, output_dir: str) -> None:
        """转换目录下的所有SVG文件"""
        svg_path = Path(svg_dir)
        output_path = Path(output_dir)
        
        # 创建输出目录
        output_path.mkdir(parents=True, exist_ok=True)
        
        # 查找所有SVG文件
        svg_files = list(svg_path.glob('*.svg'))
        
        if not svg_files:
            print(f"在目录 {svg_dir} 中未找到SVG文件")
            return
        
        print(f"找到 {len(svg_files)} 个SVG文件")
        print(f"输出目录: {output_dir}")
        print("-" * 50)
        
        success_count = 0
        for svg_file in svg_files:
            if self.convert_svg_to_vector(str(svg_file), output_dir):
                success_count += 1
        
        print("-" * 50)
        print(f"转换完成: {success_count}/{len(svg_files)} 个文件成功转换")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='SVG to Android Vector Drawable Converter')
    parser.add_argument('--input', '-i', default='svgs', 
                       help='SVG文件输入目录 (默认: svgs)')
    parser.add_argument('--output', '-o', default='vectors', 
                       help='Vector Drawable输出目录 (默认: vectors)')
    
    args = parser.parse_args()
    
    # 获取当前脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 构建完整路径
    input_dir = os.path.join(script_dir, args.input)
    output_dir = os.path.join(script_dir, args.output)
    
    print("SVG to Android Vector Drawable Converter")
    print("=" * 50)
    print(f"输入目录: {input_dir}")
    print(f"输出目录: {output_dir}")
    print()
    
    # 检查输入目录是否存在
    if not os.path.exists(input_dir):
        print(f"错误: 输入目录 '{input_dir}' 不存在")
        print(f"请确保在项目根目录下创建 '{args.input}' 文件夹并放入SVG文件")
        return
    
    # 创建转换器并执行转换
    converter = SvgToVectorConverter()
    converter.convert_directory(input_dir, output_dir)


if __name__ == '__main__':
    main()