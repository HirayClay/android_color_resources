#!/usr/bin/env python3
"""
Font File Renamer for Android
Rename font files to follow Android naming conventions
"""

import os
import shutil
from pathlib import Path
from typing import Dict, List

class FontFileRenamer:
    """Rename font files to follow Android naming conventions"""
    
    # Android font weight mapping
    WEIGHT_MAP = {
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
    
    def __init__(self, static_dir: str = "static"):
        self.static_dir = Path(static_dir)
        self.renamed_files: Dict[str, str] = {}
    
    def parse_font_filename(self, filename: str) -> Dict[str, str]:
        """Parse font filename to extract components"""
        name = filename.replace('.ttf', '').replace('.otf', '')
        
        # Default values
        family = "intertight"
        weight = "regular"
        style = "normal"
        
        # Parse weight - check for exact matches first
        name_lower = name.lower()
        
        if 'extrabold' in name_lower:
            weight = "extrabold"
        elif 'semibold' in name_lower:
            weight = "semibold"
        elif 'extralight' in name_lower:
            weight = "extralight"
        elif 'black' in name_lower:
            weight = "black"
        elif 'bold' in name_lower:
            weight = "bold"
        elif 'medium' in name_lower:
            weight = "medium"
        elif 'light' in name_lower:
            weight = "light"
        elif 'thin' in name_lower:
            weight = "thin"
        elif 'regular' in name_lower or name_lower == 'intertight':
            weight = "regular"
        
        # Parse style
        if 'italic' in name_lower:
            style = "italic"
        
        # Special case for Italic without weight (regular italic)
        if name_lower == 'intertight-italic':
            weight = "regular"
            style = "italic"
        
        return {
            'family': family,
            'weight': weight,
            'style': style,
            'weight_value': self.WEIGHT_MAP[weight]
        }
    
    def generate_android_filename(self, components: Dict[str, str]) -> str:
        """Generate Android-style filename"""
        family = components['family']
        weight_value = components['weight_value']
        style = components['style']
        
        # Android naming convention: family_weight_style.ttf
        if style == "italic":
            return f"{family}_{weight_value}_italic.ttf"
        else:
            return f"{family}_{weight_value}.ttf"
    
    def rename_font_files(self, dry_run: bool = False):
        """Rename all font files"""
        print("Renaming font files to Android naming conventions...")
        print("=" * 50)
        
        font_extensions = {'.ttf', '.otf'}
        
        for file_path in self.static_dir.iterdir():
            if file_path.suffix.lower() in font_extensions:
                old_name = file_path.name
                components = self.parse_font_filename(old_name)
                new_name = self.generate_android_filename(components)
                
                if old_name != new_name:
                    old_path = self.static_dir / old_name
                    new_path = self.static_dir / new_name
                    
                    print(f"Renaming:")
                    print(f"  From: {old_name}")
                    print(f"  To:   {new_name}")
                    print(f"  Info: {components['family'].title()} {components['weight']} {components['style']} (weight: {components['weight_value']})")
                    print()
                    
                    if not dry_run:
                        shutil.move(old_path, new_path)
                    
                    self.renamed_files[old_name] = new_name
                else:
                    print(f"Already correct: {old_name}")
                    print()
        
        print(f"Total files renamed: {len(self.renamed_files)}")
    
    def create_rename_mapping(self) -> str:
        """Create a mapping of old to new filenames"""
        mapping_content = "# Font File Rename Mapping\n\n"
        mapping_content += "This file shows the mapping from original filenames to Android-style filenames.\n\n"
        mapping_content += "## Rename Mapping\n\n"
        
        for old_name, new_name in self.renamed_files.items():
            mapping_content += f"- `{old_name}` → `{new_name}`\n"
        
        return mapping_content
    
    def run(self, dry_run: bool = False):
        """Run the renaming process"""
        print("Android Font File Renamer")
        print("=" * 30)
        
        if dry_run:
            print("DRY RUN MODE - No files will be actually renamed")
            print()
        
        # Rename files
        self.rename_font_files(dry_run)
        
        # Create mapping file
        if self.renamed_files:
            mapping_content = self.create_rename_mapping()
            mapping_file = self.static_dir / "rename_mapping.md"
            
            if not dry_run:
                with open(mapping_file, 'w', encoding='utf-8') as f:
                    f.write(mapping_content)
                print(f"Rename mapping saved to: {mapping_file}")
        
        if not dry_run:
            print("\nFont file renaming completed!")
        else:
            print("\nDry run completed. Use --execute to actually rename files.")

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Rename font files to Android naming conventions')
    parser.add_argument('--static-dir', default='static', 
                       help='Directory containing font files (default: static)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be renamed without actually renaming')
    parser.add_argument('--execute', action='store_true',
                       help='Actually rename the files (use with caution)')
    
    args = parser.parse_args()
    
    # Create renamer and run
    renamer = FontFileRenamer(args.static_dir)
    renamer.run(dry_run=not args.execute)

if __name__ == '__main__':
    main()