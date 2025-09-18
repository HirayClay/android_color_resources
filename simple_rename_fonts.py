#!/usr/bin/env python3
"""
Simple Font File Renamer
Convert font filenames to lowercase and replace dashes with underscores
"""

import os
import shutil
from pathlib import Path

class SimpleFontRenamer:
    """Simple font file renamer for Android conventions"""
    
    def __init__(self, static_dir: str = "static"):
        self.static_dir = Path(static_dir)
        self.renamed_files: dict = {}
    
    def rename_font_files(self):
        """Rename font files to lowercase with underscores"""
        print("Converting font filenames to lowercase with underscores...")
        print("=" * 50)
        
        font_extensions = {'.ttf', '.otf'}
        
        for file_path in self.static_dir.iterdir():
            if file_path.suffix.lower() in font_extensions:
                old_name = file_path.name
                
                # Simple conversion: lowercase and replace dashes with underscores
                new_name = old_name.lower().replace('-', '_')
                
                if old_name != new_name:
                    old_path = self.static_dir / old_name
                    new_path = self.static_dir / new_name
                    
                    print(f"Renaming:")
                    print(f"  From: {old_name}")
                    print(f"  To:   {new_name}")
                    print()
                    
                    shutil.move(old_path, new_path)
                    
                    self.renamed_files[old_name] = new_name
                else:
                    print(f"Already correct: {old_name}")
                    print()
        
        print(f"Total files renamed: {len(self.renamed_files)}")
    
    def run(self):
        """Run the renaming process"""
        print("Simple Font File Renamer")
        print("=" * 30)
        print()
        
        # Rename files
        self.rename_font_files()
        
        print("\nFont file renaming completed!")

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Convert font filenames to lowercase with underscores')
    parser.add_argument('--static-dir', default='static', 
                       help='Directory containing font files (default: static)')
    
    args = parser.parse_args()
    
    # Create renamer and run
    renamer = SimpleFontRenamer(args.static_dir)
    renamer.run()

if __name__ == '__main__':
    main()