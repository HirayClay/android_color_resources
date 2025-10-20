#!/usr/bin/env python3
"""
Android Font XML Generator
Generate Android font family XML files from font files in static directory
"""

import os
from typing import Dict, List
from pathlib import Path

class FontWeightMapper:
    """Map font weights to Android font weight values"""
    
    WEIGHT_MAP = {
        'thin': 100,
        'extralight': 200,
        'light': 300,
        'regular': 400,
        'medium': 500,
        'semibold': 600,
        'bold': 700,
        'extrabold': 800,
        'black': 900
    }
    
    @classmethod
    def get_weight(cls, weight_name: str) -> int:
        """Get Android font weight from weight name"""
        return cls.WEIGHT_MAP.get(weight_name.lower(), 400)

class FontFile:
    """Represents a font file with its properties"""
    
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.filename = os.path.basename(filepath)
        self.name, self.extension = os.path.splitext(self.filename)
        self.is_italic = 'italic' in self.name.lower()
        self.weight_name = self._extract_weight_name()
        self.weight_value = FontWeightMapper.get_weight(self.weight_name)
        self.font_family = self._extract_font_family()
    
    def _extract_weight_name(self) -> str:
        """Extract weight name from filename"""
        name = self.name.lower()
        
        # Remove italic suffix if present
        if 'italic' in name:
            name = name.replace('italic', '')
        
        # Extract weight from filename (intertight_weight)
        parts = name.split('_')
        if len(parts) >= 2:
            weight_part = parts[1]
            # Map weight part to weight name
            for weight_name in FontWeightMapper.WEIGHT_MAP.keys():
                if weight_name == weight_part:
                    return weight_name
        
        return 'regular'  # default
    
    def _extract_font_family(self) -> str:
        """Extract font family name from filename"""
        name = self.name.lower()
        
        # Extract family from filename (intertight_weight)
        parts = name.split('_')
        if parts:
            family = parts[0]
            # Remove dashes and capitalize
            return family.replace('-', '').title()
        
        return 'InterTight'
    
    def __str__(self):
        return f"{self.filename} - Family: {self.font_family}, Weight: {self.weight_name}({self.weight_value}), Italic: {self.is_italic}"

class AndroidFontGenerator:
    """Generate Android font XML files"""
    
    def __init__(self, static_dir: str = "static", output_dir: str = "font", output_dir_v26: str = "font-v26"):
        self.static_dir = Path(static_dir)
        self.output_dir = Path(output_dir)
        self.output_dir_v26 = Path(output_dir_v26)
        self.font_files: List[FontFile] = []
        
        # Create output directories if they don't exist
        self.output_dir.mkdir(exist_ok=True)
        self.output_dir_v26.mkdir(exist_ok=True)
    
    def scan_font_files(self):
        """Scan static directory for font files"""
        print(f"Scanning font files in {self.static_dir}...")
        
        font_extensions = {'.ttf', '.otf'}
        
        for file_path in self.static_dir.iterdir():
            if file_path.suffix.lower() in font_extensions:
                font_file = FontFile(str(file_path))
                self.font_files.append(font_file)
                print(f"Found: {font_file}")
        
        print(f"Total font files found: {len(self.font_files)}")
    
    def group_by_family(self) -> Dict[str, List[FontFile]]:
        """Group font files by font family"""
        families = {}
        
        for font_file in self.font_files:
            family = font_file.font_family
            if family not in families:
                families[family] = []
            families[family].append(font_file)
        
        return families

    def create_font_v26_family_xml(self, family_name: str, font_files: List[FontFile]) -> str:
        """Create Android font family XML string"""
        
        # Sort font files by weight and italic style
        font_files.sort(key=lambda f: (f.weight_value, f.is_italic))
        
        xml_lines = [
            '<?xml version="1.0" encoding="utf-8"?>',
            '<font-family xmlns:app="http://schemas.android.com/apk/res-auto">',
        ]
        
        # Add font elements
        for font_file in font_files:
            style = 'italic' if font_file.is_italic else 'normal'
            font_path = f"@font/{font_file.filename}"
            
            xml_lines.append(f'    <font')
            xml_lines.append(f'        app:fontStyle="{style}"')
            xml_lines.append(f'        app:fontWeight="{font_file.weight_value}"')
            xml_lines.append(f'        app:font="{font_path}" />')
        
        xml_lines.append('</font-family>')
        
        return '\n'.join(xml_lines)
        
    def create_font_family_xml(self, family_name: str, font_files: List[FontFile]) -> str:
        """Create Android font family XML string"""
        
        # Sort font files by weight and italic style
        font_files.sort(key=lambda f: (f.weight_value, f.is_italic))
        
        xml_lines = [
            '<?xml version="1.0" encoding="utf-8"?>',
            '<font-family xmlns:android="http://schemas.android.com/apk/res/android">',
        ]
        
        # Add font elements
        for font_file in font_files:
            style = 'italic' if font_file.is_italic else 'normal'
            font_path = f"@font/{font_file.filename}"
            
            xml_lines.append(f'    <font')
            xml_lines.append(f'        android:fontStyle="{style}"')
            xml_lines.append(f'        android:fontWeight="{font_file.weight_value}"')
            xml_lines.append(f'        android:font="{font_path}" />')
        
        xml_lines.append('</font-family>')
        
        return '\n'.join(xml_lines)
    
    
    def create_predefined_xml(self) -> str:
        """Create predefined font styles XML string"""
        
        families = self.group_by_family()
        
        xml_lines = [
            '<?xml version="1.0" encoding="utf-8"?>',
            '<resources>'
        ]
        
        for family_name, font_files in families.items():
            # Create array resource for font family
            xml_lines.append(f'    <array name="{family_name.lower()}_font_weights">')
            
            # Add weight values
            weights = sorted(set(f.weight_value for f in font_files))
            for weight in weights:
                xml_lines.append(f'        <item>{weight}</item>')
            
            xml_lines.append('    </array>')
            
            # Create string resource for font family name
            xml_lines.append(f'    <string name="{family_name.lower()}_font_family">{family_name}</string>')
        
        xml_lines.append('</resources>')
        
        return '\n'.join(xml_lines)
    
    def create_predefined_xml_v26(self) -> str:
        """Create predefined font styles XML string for API 26+"""
        
        families = self.group_by_family()
        
        xml_lines = [
            '<?xml version="1.0" encoding="utf-8"?>',
            '<resources>'
        ]
        
        for family_name, font_files in families.items():
            # Create array resource for font family with v26 features
            xml_lines.append(f'    <array name="{family_name.lower()}_font_weights_v26">')
            
            # Add weight values with variation settings
            weights = sorted(set(f.weight_value for f in font_files))
            for weight in weights:
                xml_lines.append(f'        <item>{weight}</item>')
            
            xml_lines.append('    </array>')
            
            # Create string resource for font family name
            xml_lines.append(f'    <string name="{family_name.lower()}_font_family_v26">{family_name}</string>')
            
            # Add font variation settings resource
            xml_lines.append(f'    <array name="{family_name.lower()}_variation_settings">')
            for weight in weights:
                variation_setting = f"'wght' {weight}"
                xml_lines.append(f'        <item>{variation_setting}</item>')
            xml_lines.append('    </array>')
        
        xml_lines.append('</resources>')
        
        return '\n'.join(xml_lines)
    
    def generate_xml_files(self):
        """Generate all XML files"""
        print("Generating Android font XML files...")
        
        # Group by family
        families = self.group_by_family()
        
        # Generate font family XML files
        for family_name, font_files in families.items():
            xml_content = self.create_font_family_xml(family_name, font_files)

            # Write to file
            output_file = self.output_dir / f"{family_name.lower()}_font_family.xml"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(xml_content)
            print(f"Generated: {output_file}")
        
        # Generate predefined styles XML
        predefined_xml = self.create_predefined_xml()
        predefined_file = self.output_dir / "font_predefined.xml"
        with open(predefined_file, 'w', encoding='utf-8') as f:
            f.write(predefined_xml)
        print(f"Generated: {predefined_file}")
        
        # Generate README
        self._generate_readme(families)
    
    def generate_xml_files_v26(self):
        """Generate all XML files for API 26+"""
        print("Generating Android font XML files for API 26+...")
        
        # Group by family
        families = self.group_by_family()
        
        # Generate font family XML files for v26
        for family_name, font_files in families.items():
            xml_content = self.create_font_v26_family_xml(family_name, font_files)
            
            # Write to font-v26 directory
            output_file = self.output_dir_v26 / f"{family_name.lower()}_font_family.xml"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(xml_content)
            print(f"Generated v26: {output_file}")
        
        # Generate predefined styles XML for v26
        predefined_xml = self.create_predefined_xml_v26()
        predefined_file = self.output_dir_v26 / "font_predefined.xml"
        with open(predefined_file, 'w', encoding='utf-8') as f:
            f.write(predefined_xml)
        print(f"Generated v26: {predefined_file}")
        
        # Generate README for v26
        self._generate_readme_v26(families)
    
    def _generate_readme(self, families: Dict[str, List[FontFile]]):
        """Generate README file with usage instructions"""
        readme_content = """# Android Font Files

This directory contains Android font XML files generated from the static font files.

## Font Families

"""
        
        for family_name, font_files in families.items():
            readme_content += f"### {family_name}\n\n"
            readme_content += "**Available weights:**\n\n"
            
            # Group by weight
            weight_groups = {}
            for font_file in font_files:
                if font_file.weight_value not in weight_groups:
                    weight_groups[font_file.weight_value] = []
                weight_groups[font_file.weight_value].append(font_file)
            
            for weight in sorted(weight_groups.keys()):
                fonts = weight_groups[weight]
                for font_file in fonts:
                    style = "Italic" if font_file.is_italic else "Regular"
                    readme_content += f"- **{font_file.weight_name.title()} {style}** (weight: {weight})\n"
            
            readme_content += "\n**Usage in XML:**\n"
            readme_content += f"```xml\n<TextView\n"
            readme_content += f"    android:fontFamily=\"@font/{family_name.lower()}_font_family\"\n"
            readme_content += f"    android:textStyle=\"normal\"\n"
            readme_content += f"    android:fontWeight=\"400\" />\n```\n\n"
            
            readme_content += "**Usage in Kotlin/Java:**\n"
            readme_content += f"```kotlin\n"
            readme_content += f"val typeface = ResourcesCompat.getFont(context, R.font.{family_name.lower()}_font_family)\n"
            readme_content += f"textView.typeface = typeface\n```\n\n"
            readme_content += "---\n\n"
        
        readme_content += """## Font Files

The following font files are referenced by the XML files:

"""
        
        for font_file in self.font_files:
            readme_content += f"- `{font_file.filename}` - {font_file.font_family} {font_file.weight_name.title()} {'Italic' if font_file.is_italic else 'Regular'}\n"
        
        # Write README
        readme_file = self.output_dir / "README.md"
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print(f"Generated: {readme_file}")
    
    def _generate_readme_v26(self, families: Dict[str, List[FontFile]]):
        """Generate README file with usage instructions for API 26+"""
        readme_content = """# Android Font Files (API 26+)

This directory contains Android font XML files generated for API 26+ with variable font support.

## Font Families

"""
        
        for family_name, font_files in families.items():
            readme_content += f"### {family_name}\n\n"
            readme_content += "**Available weights:**\n\n"
            
            # Group by weight
            weight_groups = {}
            for font_file in font_files:
                if font_file.weight_value not in weight_groups:
                    weight_groups[font_file.weight_value] = []
                weight_groups[font_file.weight_value].append(font_file)
            
            for weight in sorted(weight_groups.keys()):
                fonts = weight_groups[weight]
                for font_file in fonts:
                    style = "Italic" if font_file.is_italic else "Regular"
                    readme_content += f"- **{font_file.weight_name.title()} {style}** (weight: {weight})\n"
            
            readme_content += "\n**Usage in XML (API 26+):**\n"
            readme_content += f"```xml\n<TextView\n"
            readme_content += f"    android:fontFamily=\"@font/{family_name.lower()}_font_family\"\n"
            readme_content += f"    android:textStyle=\"normal\"\n"
            readme_content += f"    android:fontWeight=\"400\"\n"
            # readme_content += f"    android:fontVariationSettings=\"'wght' 400\" />\n```\n\n"
            
            readme_content += "**Usage in Kotlin/Java (API 26+):**\n"
            readme_content += f"```kotlin\n"
            readme_content += f"val typeface = ResourcesCompat.getFont(context, R.font.{family_name.lower()}_font_family)\n"
            readme_content += f"textView.typeface = typeface\n"
            readme_content += f"// For API 26+, you can also use font variation settings\n"
            # readme_content += f"textView.setFontVariationSettings(\"'wght' 600\")\n```\n\n"
            readme_content += "---\n\n"
        
        readme_content += """## Font Files\n\nThe following font files are referenced by the XML files:\n\n"""
        
        for font_file in self.font_files:
            readme_content += f"- `{font_file.filename}` - {font_file.font_family} {font_file.weight_name.title()} {'Italic' if font_file.is_italic else 'Regular'}\n"
        
        readme_content += "\n## API 26+ Features\n\n"
        readme_content += "- **Font Variation Settings**: Support for variable fonts with `android:fontVariationSettings`\n"
        readme_content += "- **TTC Index**: Support for TrueType Collections with `android:ttcIndex`\n"
        readme_content += "- **Enhanced Font Weight**: Better support for custom font weights\n"
        
        # Write README
        readme_file = self.output_dir_v26 / "README.md"
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print(f"Generated v26: {readme_file}")
    
    def run(self):
        """Run the font generation process"""
        print("Android Font XML Generator")
        print("=" * 40)
        
        # Scan for font files
        self.scan_font_files()
        
        if not self.font_files:
            print("No font files found!")
            return
        
        # Generate XML files for regular version
        self.generate_xml_files()
        
        # Generate XML files for API 26+ version
        self.generate_xml_files_v26()
        
        print("\nFont XML generation completed!")
        print(f"Regular output directory: {self.output_dir}")
        print(f"API 26+ output directory: {self.output_dir_v26}")

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate Android font XML files')
    parser.add_argument('--static-dir', default='static', 
                       help='Directory containing font files (default: static)')
    parser.add_argument('--output-dir', default='font', 
                       help='Output directory for XML files (default: font)')
    parser.add_argument('--output-dir-v26', default='font-v26', 
                       help='Output directory for API 26+ XML files (default: font-v26)')
    
    args = parser.parse_args()
    
    # Create generator and run
    generator = AndroidFontGenerator(args.static_dir, args.output_dir, args.output_dir_v26)
    generator.run()

if __name__ == '__main__':
    main()