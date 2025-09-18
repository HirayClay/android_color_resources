# Typography Styles

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

### display_2xl

**Properties:**
- Text Size: 72sp

### display_lg

**Properties:**
- Text Size: 48sp

### display_md

**Properties:**
- Text Size: 36sp

### display_sm

**Properties:**
- Text Size: 30sp

### display_xl

**Properties:**
- Text Size: 60sp

### display_xs

**Properties:**
- Text Size: 24sp

### text_2xs

**Properties:**
- Text Size: 11sp

### text_3xs

**Properties:**
- Text Size: 10sp

### text_lg

**Properties:**
- Text Size: 18sp

### text_md

**Properties:**
- Text Size: 16sp

### text_sm

**Properties:**
- Text Size: 14sp

### text_xl

**Properties:**
- Text Size: 20sp

### text_xs

**Properties:**
- Text Size: 12sp

