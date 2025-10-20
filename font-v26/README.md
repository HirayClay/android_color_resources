# Android Font Files (API 26+)

This directory contains Android font XML files generated for API 26+ with variable font support.

## Font Families

### Intertight

**Available weights:**

- **Thin Regular** (weight: 100)
- **Thin Italic** (weight: 100)
- **Extralight Regular** (weight: 200)
- **Extralight Italic** (weight: 200)
- **Light Regular** (weight: 300)
- **Light Italic** (weight: 300)
- **Regular Regular** (weight: 400)
- **Regular Italic** (weight: 400)
- **Medium Regular** (weight: 500)
- **Medium Italic** (weight: 500)
- **Semibold Regular** (weight: 600)
- **Semibold Italic** (weight: 600)
- **Bold Regular** (weight: 700)
- **Bold Italic** (weight: 700)
- **Extrabold Regular** (weight: 800)
- **Extrabold Italic** (weight: 800)
- **Black Regular** (weight: 900)
- **Black Italic** (weight: 900)

**Usage in XML (API 26+):**
```xml
<TextView
    android:fontFamily="@font/intertight_font_family"
    android:textStyle="normal"
    android:fontWeight="400"
**Usage in Kotlin/Java (API 26+):**
```kotlin
val typeface = ResourcesCompat.getFont(context, R.font.intertight_font_family)
textView.typeface = typeface
// For API 26+, you can also use font variation settings
---

## Font Files

The following font files are referenced by the XML files:

- `intertight_light.ttf` - Intertight Light Regular
- `intertight_extrabold.ttf` - Intertight Extrabold Regular
- `intertight_lightitalic.ttf` - Intertight Light Italic
- `intertight_semibolditalic.ttf` - Intertight Semibold Italic
- `intertight_extralightitalic.ttf` - Intertight Extralight Italic
- `intertight_blackitalic.ttf` - Intertight Black Italic
- `intertight_regular.ttf` - Intertight Regular Regular
- `intertight_bolditalic.ttf` - Intertight Bold Italic
- `intertight_thinitalic.ttf` - Intertight Thin Italic
- `intertight_extralight.ttf` - Intertight Extralight Regular
- `intertight_medium.ttf` - Intertight Medium Regular
- `intertight_thin.ttf` - Intertight Thin Regular
- `intertight_italic.ttf` - Intertight Regular Italic
- `intertight_bold.ttf` - Intertight Bold Regular
- `intertight_semibold.ttf` - Intertight Semibold Regular
- `intertight_mediumitalic.ttf` - Intertight Medium Italic
- `intertight_extrabolditalic.ttf` - Intertight Extrabold Italic
- `intertight_black.ttf` - Intertight Black Regular

## API 26+ Features

- **Font Variation Settings**: Support for variable fonts with `android:fontVariationSettings`
- **TTC Index**: Support for TrueType Collections with `android:ttcIndex`
- **Enhanced Font Weight**: Better support for custom font weights
