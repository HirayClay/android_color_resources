#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import re
import os

def read_semantic_colors(day_file_path, night_file_path):
    """读取日间和夜间的semantic_color.xml文件，获取颜色映射关系"""
    # 读取日间模式
    day_tree = ET.parse(day_file_path)
    day_root = day_tree.getroot()
    
    day_semantic_colors = {}
    for color in day_root.findall('color'):
        name = color.get('name')
        value = color.text
        if value and value.startswith('@color/'):
            # 提取引用的primitive颜色名
            primitive_name = value.replace('@color/', '')
            day_semantic_colors[name] = primitive_name
        else:
            # 直接颜色值
            day_semantic_colors[name] = value
    
    # 读取夜间模式
    night_tree = ET.parse(night_file_path)
    night_root = night_tree.getroot()
    
    night_semantic_colors = {}
    for color in night_root.findall('color'):
        name = color.get('name')
        value = color.text
        if value and value.startswith('@color/'):
            # 提取引用的primitive颜色名
            primitive_name = value.replace('@color/', '')
            night_semantic_colors[name] = primitive_name
        else:
            # 直接颜色值
            night_semantic_colors[name] = value
    
    return day_semantic_colors, night_semantic_colors

def read_primitive_colors(primitive_file_path):
    """读取primitive_color.xml文件，获取具体颜色值"""
    tree = ET.parse(primitive_file_path)
    root = tree.getroot()
    
    primitive_colors = {}
    for color in root.findall('color'):
        name = color.get('name')
        value = color.text
        if value:
            primitive_colors[name] = value
    
    return primitive_colors

def get_final_color_value(day_semantic_colors, night_semantic_colors, primitive_colors_day, primitive_colors_night, semantic_name):
    """获取语义颜色的最终颜色值（同时返回日间和夜间模式的值）"""
    # 获取日间模式的映射
    day_primitive_name = day_semantic_colors.get(semantic_name)
    if not day_primitive_name:
        return "#000000", "#000000"  # 默认黑色
    
    # 获取夜间模式的映射（如果不存在则使用日间的）
    night_primitive_name = night_semantic_colors.get(semantic_name, day_primitive_name)
    
    # 如果直接存储的是颜色值
    if day_primitive_name.startswith('#'):
        day_color = day_primitive_name
    else:
        day_color = primitive_colors_day.get(day_primitive_name, "#000000")
    
    if night_primitive_name.startswith('#'):
        night_color = night_primitive_name
    else:
        night_color = primitive_colors_night.get(night_primitive_name, "#000000")
    
    return day_color, night_color, day_primitive_name, night_primitive_name

def generate_kt_content(day_semantic_colors, night_semantic_colors, primitive_colors_day, primitive_colors_night):
    """生成ExtAuColor.kt文件内容"""
    
    # 文件头部
    header = '''package com.vau.ui

import android.content.res.Configuration
import android.graphics.Color
import androidx.core.content.ContextCompat
import androidx.core.graphics.toColorInt

/**
 * 安全的颜色获取扩展函数
 * 在预览模式下会提供默认颜色，避免预览失败
 */
fun Int.asColor(): Int {
    return try {
        val ctx = AUIInitializer.getContext()
        ContextCompat.getColor(ctx, this)
    } catch (e: Exception) {
        // 在预览模式或Context未初始化时提供默认颜色
        getDefaultColor()
    }
}

/**
 * 根据资源ID提供默认颜色
 * 使用从XML文件中提取的实际颜色值，支持日间和夜间模式
 */
private fun Int.getDefaultColor(isDay: Boolean = true): Int {
    return when (this) {'''
    
    # 生成颜色映射部分
    color_mappings = []
    
    # 按类别分组处理颜色
    categories = {
        'text': [],
        'bg': [],
        'border': [],
        'fg': [],
        'button': [],
        'icon': [],
        'utility': [],
        'other': []
    }
    
    # 将颜色按类别分组
    for semantic_name in sorted(day_semantic_colors.keys()):
        day_color, night_color, day_primitive_name, night_primitive_name = get_final_color_value(
            day_semantic_colors, night_semantic_colors, primitive_colors_day, primitive_colors_night, semantic_name)
        
        # R.color.xxx -> xxx
        r_color_name = f"R.color.{semantic_name}"
        
        # 生成注释信息
        if day_primitive_name == night_primitive_name:
            comment_info = day_primitive_name
        else:
            comment_info = f"{day_primitive_name} -> {night_primitive_name}"
        
        if semantic_name.startswith('text_'):
            categories['text'].append((r_color_name, day_color, night_color, comment_info, semantic_name))
        elif semantic_name.startswith('bg_'):
            categories['bg'].append((r_color_name, day_color, night_color, comment_info, semantic_name))
        elif semantic_name.startswith('border_'):
            categories['border'].append((r_color_name, day_color, night_color, comment_info, semantic_name))
        elif semantic_name.startswith('fg_'):
            categories['fg'].append((r_color_name, day_color, night_color, comment_info, semantic_name))
        elif semantic_name.startswith('button_'):
            categories['button'].append((r_color_name, day_color, night_color, comment_info, semantic_name))
        elif 'icon' in semantic_name:
            categories['icon'].append((r_color_name, day_color, night_color, comment_info, semantic_name))
        elif semantic_name.startswith('utility_'):
            categories['utility'].append((r_color_name, day_color, night_color, comment_info, semantic_name))
        else:
            categories['other'].append((r_color_name, day_color, night_color, comment_info, semantic_name))
    
    # 生成分类注释和映射
    for category_name, colors in categories.items():
        if colors:
            if category_name == 'text':
                color_mappings.append("        // Text Colors")
            elif category_name == 'bg':
                color_mappings.append("        // Background Colors") 
            elif category_name == 'border':
                color_mappings.append("        // Border Colors")
            elif category_name == 'fg':
                color_mappings.append("        // Foreground Colors")
            elif category_name == 'button':
                color_mappings.append("        // Button Colors")
            elif category_name == 'icon':
                color_mappings.append("        // Icon Colors")
            elif category_name == 'utility':
                color_mappings.append("        // Utility Colors")
            elif category_name == 'other':
                color_mappings.append("        // Other Colors")
            
            for r_color_name, day_color, night_color, comment_info, semantic_name in colors:
                # 如果日夜间颜色值相同，直接使用颜色值；否则生成判断逻辑
                if day_color == night_color:
                    color_mappings.append(f'        {r_color_name} -> "{day_color}".toColorInt() // {comment_info}')
                else:
                    color_mappings.append(f'        {r_color_name} -> if (isDay) "{day_color}".toColorInt() else "{night_color}".toColorInt() // {comment_info}')
            
            color_mappings.append("")  # 添加空行分隔
    
    # 文件尾部
    footer = '''        // 默认颜色
        else -> "#000000".toColorInt() // black
    }
}'''
    
    # 组合完整内容
    full_content = header + "\n" + "\n".join(color_mappings) + footer
    
    return full_content

def main():
    """主函数"""
    # 文件路径
    semantic_file_day = "/Users/bjsttlp312/android_color_resources/values/semantic_color.xml"
    semantic_file_night = "/Users/bjsttlp312/android_color_resources/values-night/semantic_color.xml"
    primitive_file_day = "/Users/bjsttlp312/android_color_resources/values/primitive_color.xml"
    primitive_file_night = "/Users/bjsttlp312/android_color_resources/values-night/primitive_color.xml"
    output_file = "/Users/bjsttlp312/android_color_resources/AuColor.kt"
    
    # 检查文件是否存在
    if not os.path.exists(semantic_file_day):
        print(f"错误: 文件不存在 {semantic_file_day}")
        return
        
    if not os.path.exists(semantic_file_night):
        print(f"错误: 文件不存在 {semantic_file_night}")
        return
    
    if not os.path.exists(primitive_file_day):
        print(f"错误: 文件不存在 {primitive_file_day}")
        return
        
    if not os.path.exists(primitive_file_night):
        print(f"错误: 文件不存在 {primitive_file_night}")
        return
    
    try:
        # 读取XML文件
        print("正在读取日间和夜间模式的semantic_color.xml...")
        day_semantic_colors, night_semantic_colors = read_semantic_colors(semantic_file_day, semantic_file_night)
        print(f"读取到 {len(day_semantic_colors)} 个日间语义颜色和 {len(night_semantic_colors)} 个夜间语义颜色")
        
        print("正在读取日间模式primitive_color.xml...")
        primitive_colors_day = read_primitive_colors(primitive_file_day)
        print(f"读取到 {len(primitive_colors_day)} 个日间基础颜色")
        
        print("正在读取夜间模式primitive_color.xml...")
        primitive_colors_night = read_primitive_colors(primitive_file_night)
        print(f"读取到 {len(primitive_colors_night)} 个夜间基础颜色")
        
        # 生成Kotlin代码
        print("正在生成AuColor.kt内容...")
        kt_content = generate_kt_content(day_semantic_colors, night_semantic_colors, primitive_colors_day, primitive_colors_night)
        
        # 写入文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(kt_content)
        
        print(f"成功生成 AuColor.kt")
        print(f"生成的文件包含 {len(day_semantic_colors)} 个颜色映射")
        
    except Exception as e:
        print(f"生成过程中发生错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()