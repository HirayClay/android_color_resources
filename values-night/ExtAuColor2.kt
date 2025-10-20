package com.vau.ui

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
 * 使用从XML文件中提取的实际颜色值
 */
private fun Int.getDefaultColor(): Int {
    return when (this) {
        // Text Colors
        R.color.text_brand_primary -> "#391004".toColorInt() // brand_900
        R.color.text_brand_secondary -> "#b1311d".toColorInt() // brand_700
        R.color.text_brand_secondary_hover -> "#8d291f".toColorInt() // brand_800
        R.color.text_brand_tertiary -> "#d54221".toColorInt() // brand_600
        R.color.text_brand_tertiary_alt -> "#d54221".toColorInt() // brand_600
        R.color.text_disabled -> "#717680".toColorInt() // gray_500
        R.color.text_editor_icon_fg -> "#a4a7ae".toColorInt() // gray_400
        R.color.text_editor_icon_fg_active -> "#717680".toColorInt() // gray_500
        R.color.text_error_primary -> "#d92d20".toColorInt() // error_600
        R.color.text_error_primary_hover -> "#b42318".toColorInt() // error_700
        R.color.text_inverse -> "#ffffff".toColorInt() // white
        R.color.text_placeholder -> "#717680".toColorInt() // gray_500
        R.color.text_placeholder_subtle -> "#d5d7da".toColorInt() // gray_300
        R.color.text_primary -> "#181d27".toColorInt() // gray_900
        R.color.text_primary_on_brand -> "#ffffff".toColorInt() // white
        R.color.text_quaternary -> "#717680".toColorInt() // gray_500
        R.color.text_quaternary_on_brand -> "#f0a881".toColorInt() // brand_300
        R.color.text_secondary -> "#414651".toColorInt() // gray_700
        R.color.text_secondary_hover -> "#252b37".toColorInt() // gray_800
        R.color.text_secondary_on_brand -> "#f6cbb2".toColorInt() // brand_200
        R.color.text_success_primary -> "#079455".toColorInt() // success_600
        R.color.text_tertiary -> "#535862".toColorInt() // gray_600
        R.color.text_tertiary_hover -> "#414651".toColorInt() // gray_700
        R.color.text_tertiary_on_brand -> "#f6cbb2".toColorInt() // brand_200
        R.color.text_warning_primary -> "#dc6803".toColorInt() // warning_600
        R.color.text_white -> "#ffffff".toColorInt() // white

        // Background Colors
        R.color.bg_active -> "#fafafa".toColorInt() // gray_50
        R.color.bg_brand_primary -> "#fdf5ef".toColorInt() // brand_50
        R.color.bg_brand_primary_alt -> "#fdf5ef".toColorInt() // brand_50
        R.color.bg_brand_secondary -> "#fbe7d9".toColorInt() // brand_100
        R.color.bg_brand_section -> "#8d291f".toColorInt() // brand_800
        R.color.bg_brand_section_subtle -> "#b1311d".toColorInt() // brand_700
        R.color.bg_brand_solid -> "#d54221".toColorInt() // brand_600
        R.color.bg_brand_solid_hover -> "#b1311d".toColorInt() // brand_700
        R.color.bg_disabled -> "#f5f5f5".toColorInt() // gray_100
        R.color.bg_disabled_subtle -> "#fafafa".toColorInt() // gray_50
        R.color.bg_error_primary -> "#fef3f2".toColorInt() // error_50
        R.color.bg_error_secondary -> "#fee4e2".toColorInt() // error_100
        R.color.bg_error_solid -> "#d92d20".toColorInt() // error_600
        R.color.bg_overlay -> "#0a0d12".toColorInt() // gray_950
        R.color.bg_primary -> "#181d27".toColorInt() // gray_900
        R.color.bg_primary_alt -> "#ffffff".toColorInt() // white
        R.color.bg_primary_hover -> "#fafafa".toColorInt() // gray_50
        R.color.bg_primary_solid -> "#0a0d12".toColorInt() // gray_950
        R.color.bg_quaternary -> "#e9eaeb".toColorInt() // gray_200
        R.color.bg_secondary -> "#fafafa".toColorInt() // gray_50
        R.color.bg_secondary_alt -> "#fafafa".toColorInt() // gray_50
        R.color.bg_secondary_hover -> "#f5f5f5".toColorInt() // gray_100
        R.color.bg_secondary_solid -> "#535862".toColorInt() // gray_600
        R.color.bg_secondary_subtle -> "#fdfdfd".toColorInt() // gray_25
        R.color.bg_success_primary -> "#ecfdf3".toColorInt() // success_50
        R.color.bg_success_secondary -> "#dcfae6".toColorInt() // success_100
        R.color.bg_success_solid -> "#079455".toColorInt() // success_600
        R.color.bg_tertiary -> "#f5f5f5".toColorInt() // gray_100
        R.color.bg_warning_primary -> "#fffaeb".toColorInt() // warning_50
        R.color.bg_warning_secondary -> "#fef0c7".toColorInt() // warning_100
        R.color.bg_warning_solid -> "#dc6803".toColorInt() // warning_600

        // Border Colors
        R.color.border_brand -> "#e35728".toColorInt() // brand_500
        R.color.border_brand_alt -> "#d54221".toColorInt() // brand_600
        R.color.border_disabled -> "#d5d7da".toColorInt() // gray_300
        R.color.border_disabled_subtle -> "#e9eaeb".toColorInt() // gray_200
        R.color.border_error -> "#f04438".toColorInt() // error_500
        R.color.border_error_subtle -> "#fda29b".toColorInt() // error_300
        R.color.border_inverse -> "#ffffff".toColorInt() // white
        R.color.border_primary -> "#181d27".toColorInt() // gray_900
        R.color.border_secondary -> "#e9eaeb".toColorInt() // gray_200
        R.color.border_tertiary -> "#f5f5f5".toColorInt() // gray_100

        // Foreground Colors
        R.color.fg_brand_primary -> "#d54221".toColorInt() // brand_600
        R.color.fg_brand_primary_alt -> "#d54221".toColorInt() // brand_600
        R.color.fg_brand_secondary -> "#e35728".toColorInt() // brand_500
        R.color.fg_brand_secondary_alt -> "#e35728".toColorInt() // brand_500
        R.color.fg_brand_secondary_hover -> "#d54221".toColorInt() // brand_600
        R.color.fg_disabled -> "#a4a7ae".toColorInt() // gray_400
        R.color.fg_disabled_subtle -> "#d5d7da".toColorInt() // gray_300
        R.color.fg_error_primary -> "#d92d20".toColorInt() // error_600
        R.color.fg_error_secondary -> "#f04438".toColorInt() // error_500
        R.color.fg_primary -> "#181d27".toColorInt() // gray_900
        R.color.fg_quaternary -> "#a4a7ae".toColorInt() // gray_400
        R.color.fg_quaternary_hover -> "#717680".toColorInt() // gray_500
        R.color.fg_secondary -> "#414651".toColorInt() // gray_700
        R.color.fg_secondary_hover -> "#252b37".toColorInt() // gray_800
        R.color.fg_success_primary -> "#079455".toColorInt() // success_600
        R.color.fg_success_secondary -> "#17b26a".toColorInt() // success_500
        R.color.fg_tertiary -> "#535862".toColorInt() // gray_600
        R.color.fg_tertiary_hover -> "#414651".toColorInt() // gray_700
        R.color.fg_warning_primary -> "#dc6803".toColorInt() // warning_600
        R.color.fg_warning_secondary -> "#f79009".toColorInt() // warning_500
        R.color.fg_white -> "#ffffff".toColorInt() // white

        // Button Colors
        R.color.button_destructive_primary_icon -> "#fda29b".toColorInt() // error_300
        R.color.button_destructive_primary_icon_hover -> "#fecdca".toColorInt() // error_200
        R.color.button_primary_icon -> "#f0a881".toColorInt() // brand_300
        R.color.button_primary_icon_hover -> "#f6cbb2".toColorInt() // brand_200

        // Icon Colors
        R.color.featured_icon_light_fg_brand -> "#d54221".toColorInt() // brand_600
        R.color.featured_icon_light_fg_error -> "#d92d20".toColorInt() // error_600
        R.color.featured_icon_light_fg_gray -> "#717680".toColorInt() // gray_500
        R.color.featured_icon_light_fg_success -> "#079455".toColorInt() // success_600
        R.color.featured_icon_light_fg_warning -> "#dc6803".toColorInt() // warning_600
        R.color.icon_fg_brand_on_brand -> "#f6cbb2".toColorInt() // brand_200

        // Utility Colors
        R.color.utility_blue_100 -> "#d1e9ff".toColorInt() // blue_100
        R.color.utility_blue_200 -> "#b2ddff".toColorInt() // blue_200
        R.color.utility_blue_300 -> "#84caff".toColorInt() // blue_300
        R.color.utility_blue_400 -> "#53b1fd".toColorInt() // blue_400
        R.color.utility_blue_50 -> "#eff8ff".toColorInt() // blue_50
        R.color.utility_blue_500 -> "#2e90fa".toColorInt() // blue_500
        R.color.utility_blue_600 -> "#1570ef".toColorInt() // blue_600
        R.color.utility_blue_700 -> "#175cd3".toColorInt() // blue_700
        R.color.utility_blue_dark_100 -> "#d1e0ff".toColorInt() // blue_dark_100
        R.color.utility_blue_dark_200 -> "#b2ccff".toColorInt() // blue_dark_200
        R.color.utility_blue_dark_300 -> "#84adff".toColorInt() // blue_dark_300
        R.color.utility_blue_dark_400 -> "#528bff".toColorInt() // blue_dark_400
        R.color.utility_blue_dark_50 -> "#eff4ff".toColorInt() // blue_dark_50
        R.color.utility_blue_dark_500 -> "#2970ff".toColorInt() // blue_dark_500
        R.color.utility_blue_dark_600 -> "#155eef".toColorInt() // blue_dark_600
        R.color.utility_blue_dark_700 -> "#004eeb".toColorInt() // blue_dark_700
        R.color.utility_blue_light_100 -> "#e0f2fe".toColorInt() // blue_light_100
        R.color.utility_blue_light_200 -> "#b9e6fe".toColorInt() // blue_light_200
        R.color.utility_blue_light_300 -> "#7cd4fd".toColorInt() // blue_light_300
        R.color.utility_blue_light_400 -> "#36bffa".toColorInt() // blue_light_400
        R.color.utility_blue_light_50 -> "#f0f9ff".toColorInt() // blue_light_50
        R.color.utility_blue_light_500 -> "#0ba5ec".toColorInt() // blue_light_500
        R.color.utility_blue_light_600 -> "#0086c9".toColorInt() // blue_light_600
        R.color.utility_blue_light_700 -> "#026aa2".toColorInt() // blue_light_700
        R.color.utility_brand_100 -> "#fbe7d9".toColorInt() // brand_100
        R.color.utility_brand_100_alt -> "#fbe7d9".toColorInt() // brand_100
        R.color.utility_brand_200 -> "#f6cbb2".toColorInt() // brand_200
        R.color.utility_brand_200_alt -> "#f6cbb2".toColorInt() // brand_200
        R.color.utility_brand_300 -> "#f0a881".toColorInt() // brand_300
        R.color.utility_brand_300_alt -> "#f0a881".toColorInt() // brand_300
        R.color.utility_brand_400 -> "#e97b4e".toColorInt() // brand_400
        R.color.utility_brand_400_alt -> "#e97b4e".toColorInt() // brand_400
        R.color.utility_brand_50 -> "#fdf5ef".toColorInt() // brand_50
        R.color.utility_brand_500 -> "#e35728".toColorInt() // brand_500
        R.color.utility_brand_500_alt -> "#e35728".toColorInt() // brand_500
        R.color.utility_brand_50_alt -> "#fdf5ef".toColorInt() // brand_50
        R.color.utility_brand_600 -> "#d54221".toColorInt() // brand_600
        R.color.utility_brand_600_alt -> "#d54221".toColorInt() // brand_600
        R.color.utility_brand_700 -> "#b1311d".toColorInt() // brand_700
        R.color.utility_brand_700_alt -> "#b1311d".toColorInt() // brand_700
        R.color.utility_brand_800 -> "#8d291f".toColorInt() // brand_800
        R.color.utility_brand_800_alt -> "#8d291f".toColorInt() // brand_800
        R.color.utility_brand_900 -> "#391004".toColorInt() // brand_900
        R.color.utility_brand_900_alt -> "#391004".toColorInt() // brand_900
        R.color.utility_error_100 -> "#fee4e2".toColorInt() // error_100
        R.color.utility_error_200 -> "#fecdca".toColorInt() // error_200
        R.color.utility_error_300 -> "#fda29b".toColorInt() // error_300
        R.color.utility_error_400 -> "#f97066".toColorInt() // error_400
        R.color.utility_error_50 -> "#fef3f2".toColorInt() // error_50
        R.color.utility_error_500 -> "#f04438".toColorInt() // error_500
        R.color.utility_error_600 -> "#d92d20".toColorInt() // error_600
        R.color.utility_error_700 -> "#b42318".toColorInt() // error_700
        R.color.utility_fuchsia_100 -> "#fbe8ff".toColorInt() // fuchsia_100
        R.color.utility_fuchsia_200 -> "#f6d0fe".toColorInt() // fuchsia_200
        R.color.utility_fuchsia_300 -> "#eeaafd".toColorInt() // fuchsia_300
        R.color.utility_fuchsia_400 -> "#e478fa".toColorInt() // fuchsia_400
        R.color.utility_fuchsia_50 -> "#fdf4ff".toColorInt() // fuchsia_50
        R.color.utility_fuchsia_500 -> "#d444f1".toColorInt() // fuchsia_500
        R.color.utility_fuchsia_600 -> "#ba24d5".toColorInt() // fuchsia_600
        R.color.utility_fuchsia_700 -> "#9f1ab1".toColorInt() // fuchsia_700
        R.color.utility_gray_100 -> "#f5f5f5".toColorInt() // gray_100
        R.color.utility_gray_200 -> "#e9eaeb".toColorInt() // gray_200
        R.color.utility_gray_300 -> "#d5d7da".toColorInt() // gray_300
        R.color.utility_gray_400 -> "#a4a7ae".toColorInt() // gray_400
        R.color.utility_gray_50 -> "#fafafa".toColorInt() // gray_50
        R.color.utility_gray_500 -> "#717680".toColorInt() // gray_500
        R.color.utility_gray_600 -> "#535862".toColorInt() // gray_600
        R.color.utility_gray_700 -> "#414651".toColorInt() // gray_700
        R.color.utility_gray_800 -> "#252b37".toColorInt() // gray_800
        R.color.utility_gray_900 -> "#181d27".toColorInt() // gray_900
        R.color.utility_gray_blue_100 -> "#eaecf5".toColorInt() // gray_blue_100
        R.color.utility_gray_blue_200 -> "#d5d9eb".toColorInt() // gray_blue_200
        R.color.utility_gray_blue_300 -> "#b3b8db".toColorInt() // gray_blue_300
        R.color.utility_gray_blue_400 -> "#717bbc".toColorInt() // gray_blue_400
        R.color.utility_gray_blue_50 -> "#f8f9fc".toColorInt() // gray_blue_50
        R.color.utility_gray_blue_500 -> "#4e5ba6".toColorInt() // gray_blue_500
        R.color.utility_gray_blue_600 -> "#3e4784".toColorInt() // gray_blue_600
        R.color.utility_gray_blue_700 -> "#363f72".toColorInt() // gray_blue_700
        R.color.utility_green_100 -> "#d3f8df".toColorInt() // green_100
        R.color.utility_green_200 -> "#aaf0c4".toColorInt() // green_200
        R.color.utility_green_300 -> "#73e2a3".toColorInt() // green_300
        R.color.utility_green_400 -> "#3ccb7f".toColorInt() // green_400
        R.color.utility_green_50 -> "#edfcf2".toColorInt() // green_50
        R.color.utility_green_500 -> "#16b364".toColorInt() // green_500
        R.color.utility_green_600 -> "#099250".toColorInt() // green_600
        R.color.utility_green_700 -> "#087443".toColorInt() // green_700
        R.color.utility_indigo_100 -> "#e0eaff".toColorInt() // indigo_100
        R.color.utility_indigo_200 -> "#c7d7fe".toColorInt() // indigo_200
        R.color.utility_indigo_300 -> "#a4bcfd".toColorInt() // indigo_300
        R.color.utility_indigo_400 -> "#8098f9".toColorInt() // indigo_400
        R.color.utility_indigo_50 -> "#eef4ff".toColorInt() // indigo_50
        R.color.utility_indigo_500 -> "#6172f3".toColorInt() // indigo_500
        R.color.utility_indigo_600 -> "#444ce7".toColorInt() // indigo_600
        R.color.utility_indigo_700 -> "#3538cd".toColorInt() // indigo_700
        R.color.utility_orange_100 -> "#fdead7".toColorInt() // orange_100
        R.color.utility_orange_200 -> "#f9dbaf".toColorInt() // orange_200
        R.color.utility_orange_300 -> "#f7b27a".toColorInt() // orange_300
        R.color.utility_orange_400 -> "#f38744".toColorInt() // orange_400
        R.color.utility_orange_50 -> "#fef6ee".toColorInt() // orange_50
        R.color.utility_orange_500 -> "#ef6820".toColorInt() // orange_500
        R.color.utility_orange_600 -> "#e04f16".toColorInt() // orange_600
        R.color.utility_orange_700 -> "#b93815".toColorInt() // orange_700
        R.color.utility_orange_dark_100 -> "#ffe6d5".toColorInt() // orange_dark_100
        R.color.utility_orange_dark_200 -> "#ffd6ae".toColorInt() // orange_dark_200
        R.color.utility_orange_dark_300 -> "#ff9c66".toColorInt() // orange_dark_300
        R.color.utility_orange_dark_400 -> "#ff692e".toColorInt() // orange_dark_400
        R.color.utility_orange_dark_50 -> "#fff4ed".toColorInt() // orange_dark_50
        R.color.utility_orange_dark_500 -> "#ff4405".toColorInt() // orange_dark_500
        R.color.utility_orange_dark_600 -> "#e62e05".toColorInt() // orange_dark_600
        R.color.utility_orange_dark_700 -> "#bc1b06".toColorInt() // orange_dark_700
        R.color.utility_pink_100 -> "#fce7f6".toColorInt() // pink_100
        R.color.utility_pink_200 -> "#fcceee".toColorInt() // pink_200
        R.color.utility_pink_300 -> "#faa7e0".toColorInt() // pink_300
        R.color.utility_pink_400 -> "#f670c7".toColorInt() // pink_400
        R.color.utility_pink_50 -> "#fdf2fa".toColorInt() // pink_50
        R.color.utility_pink_500 -> "#ee46bc".toColorInt() // pink_500
        R.color.utility_pink_600 -> "#dd2590".toColorInt() // pink_600
        R.color.utility_pink_700 -> "#c11574".toColorInt() // pink_700
        R.color.utility_purple_100 -> "#ebe9fe".toColorInt() // purple_100
        R.color.utility_purple_200 -> "#d9d6fe".toColorInt() // purple_200
        R.color.utility_purple_300 -> "#bdb4fe".toColorInt() // purple_300
        R.color.utility_purple_400 -> "#9b8afb".toColorInt() // purple_400
        R.color.utility_purple_50 -> "#f4f3ff".toColorInt() // purple_50
        R.color.utility_purple_500 -> "#7a5af8".toColorInt() // purple_500
        R.color.utility_purple_600 -> "#6938ef".toColorInt() // purple_600
        R.color.utility_purple_700 -> "#5925dc".toColorInt() // purple_700
        R.color.utility_success_100 -> "#dcfae6".toColorInt() // success_100
        R.color.utility_success_200 -> "#abefc6".toColorInt() // success_200
        R.color.utility_success_300 -> "#75e0a7".toColorInt() // success_300
        R.color.utility_success_400 -> "#47cd89".toColorInt() // success_400
        R.color.utility_success_50 -> "#ecfdf3".toColorInt() // success_50
        R.color.utility_success_500 -> "#17b26a".toColorInt() // success_500
        R.color.utility_success_600 -> "#079455".toColorInt() // success_600
        R.color.utility_success_700 -> "#067647".toColorInt() // success_700
        R.color.utility_warning_100 -> "#fef0c7".toColorInt() // warning_100
        R.color.utility_warning_200 -> "#fedf89".toColorInt() // warning_200
        R.color.utility_warning_300 -> "#fec84b".toColorInt() // warning_300
        R.color.utility_warning_400 -> "#fdb022".toColorInt() // warning_400
        R.color.utility_warning_50 -> "#fffaeb".toColorInt() // warning_50
        R.color.utility_warning_500 -> "#f79009".toColorInt() // warning_500
        R.color.utility_warning_600 -> "#dc6803".toColorInt() // warning_600
        R.color.utility_warning_700 -> "#b54708".toColorInt() // warning_700
        R.color.utility_yellow_100 -> "#fef7c3".toColorInt() // yellow_100
        R.color.utility_yellow_200 -> "#feee95".toColorInt() // yellow_200
        R.color.utility_yellow_300 -> "#fde272".toColorInt() // yellow_300
        R.color.utility_yellow_400 -> "#fac515".toColorInt() // yellow_400
        R.color.utility_yellow_50 -> "#fefbe8".toColorInt() // yellow_50
        R.color.utility_yellow_500 -> "#eaaa08".toColorInt() // yellow_500
        R.color.utility_yellow_600 -> "#ca8504".toColorInt() // yellow_600
        R.color.utility_yellow_700 -> "#a15c07".toColorInt() // yellow_700

        // Other Colors
        R.color.alpha_white_100 -> "#ffffff".toColorInt() // white
        R.color.app_store_badge_border -> "#a3a3a3".toColorInt() // gray_true_400
        R.color.avatar_styles_bg_neutral -> "#e5e5e5".toColorInt() // gray_true_200
        R.color.focus_ring -> "#e35728".toColorInt() // brand_500
        R.color.focus_ring_error -> "#f04438".toColorInt() // error_500
        R.color.footer_button_fg -> "#f6cbb2".toColorInt() // brand_200
        R.color.footer_button_fg_hover -> "#ffffff".toColorInt() // white
        R.color.screen_mockup_border -> "#181d27".toColorInt() // gray_900
        R.color.slider_handle_bg -> "#ffffff".toColorInt() // white
        R.color.slider_handle_border -> "#d54221".toColorInt() // brand_600
        R.color.toggle_border -> "#d5d7da".toColorInt() // gray_300
        R.color.toggle_button_fg_disabled -> "#fafafa".toColorInt() // gray_50
        R.color.toggle_slim_border_pressed -> "#d54221".toColorInt() // brand_600
        R.color.toggle_slim_border_pressed_hover -> "#b1311d".toColorInt() // brand_700
        R.color.tooltip_supporting_text -> "#d5d7da".toColorInt() // gray_300
        // 默认颜色
        else -> "#000000".toColorInt() // black
    }
}