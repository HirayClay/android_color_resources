package com.vau.ui

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
    return when (this) {
        // Text Colors
        R.color.text_brand_primary -> if (isDay) "#391004".toColorInt() else "#f7f7f7".toColorInt() // brand_900 -> gray_50
        R.color.text_brand_secondary -> if (isDay) "#b1311d".toColorInt() else "#cecfd2".toColorInt() // brand_700 -> gray_300
        R.color.text_brand_secondary_hover -> if (isDay) "#8d291f".toColorInt() else "#ececed".toColorInt() // brand_800 -> gray_200
        R.color.text_brand_tertiary -> if (isDay) "#d54221".toColorInt() else "#94979c".toColorInt() // brand_600 -> gray_400
        R.color.text_brand_tertiary_alt -> if (isDay) "#d54221".toColorInt() else "#f7f7f7".toColorInt() // brand_600 -> gray_50
        R.color.text_disabled -> if (isDay) "#717680".toColorInt() else "#85888e".toColorInt() // gray_500
        R.color.text_editor_icon_fg -> if (isDay) "#a4a7ae".toColorInt() else "#94979c".toColorInt() // gray_400
        R.color.text_editor_icon_fg_active -> if (isDay) "#717680".toColorInt() else "#ffffff".toColorInt() // gray_500 -> white
        R.color.text_error_primary -> if (isDay) "#d92d20".toColorInt() else "#f97066".toColorInt() // error_600 -> error_400
        R.color.text_error_primary_hover -> if (isDay) "#b42318".toColorInt() else "#fda29b".toColorInt() // error_700 -> error_300
        R.color.text_inverse -> if (isDay) "#ffffff".toColorInt() else "#000000".toColorInt() // white -> black
        R.color.text_placeholder -> if (isDay) "#717680".toColorInt() else "#85888e".toColorInt() // gray_500
        R.color.text_placeholder_subtle -> if (isDay) "#d5d7da".toColorInt() else "#373a41".toColorInt() // gray_300 -> gray_700
        R.color.text_primary -> if (isDay) "#181d27".toColorInt() else "#f7f7f7".toColorInt() // gray_900 -> gray_50
        R.color.text_primary_on_brand -> if (isDay) "#ffffff".toColorInt() else "#f7f7f7".toColorInt() // white -> gray_50
        R.color.text_quaternary -> if (isDay) "#717680".toColorInt() else "#94979c".toColorInt() // gray_500 -> gray_400
        R.color.text_quaternary_on_brand -> if (isDay) "#f0a881".toColorInt() else "#94979c".toColorInt() // brand_300 -> gray_400
        R.color.text_secondary -> if (isDay) "#414651".toColorInt() else "#cecfd2".toColorInt() // gray_700 -> gray_300
        R.color.text_secondary_hover -> if (isDay) "#252b37".toColorInt() else "#ececed".toColorInt() // gray_800 -> gray_200
        R.color.text_secondary_on_brand -> if (isDay) "#f6cbb2".toColorInt() else "#cecfd2".toColorInt() // brand_200 -> gray_300
        R.color.text_success_primary -> if (isDay) "#079455".toColorInt() else "#47cd89".toColorInt() // success_600 -> success_400
        R.color.text_tertiary -> if (isDay) "#535862".toColorInt() else "#94979c".toColorInt() // gray_600 -> gray_400
        R.color.text_tertiary_hover -> if (isDay) "#414651".toColorInt() else "#cecfd2".toColorInt() // gray_700 -> gray_300
        R.color.text_tertiary_on_brand -> if (isDay) "#f6cbb2".toColorInt() else "#94979c".toColorInt() // brand_200 -> gray_400
        R.color.text_warning_primary -> if (isDay) "#dc6803".toColorInt() else "#fdb022".toColorInt() // warning_600 -> warning_400
        R.color.text_white -> "#ffffff".toColorInt() // white

        // Background Colors
        R.color.bg_active -> if (isDay) "#fafafa".toColorInt() else "#26272b".toColorInt() // gray_50 -> gray_iron_800
        R.color.bg_brand_primary -> if (isDay) "#fdf5ef".toColorInt() else "#e35728".toColorInt() // brand_50 -> brand_500
        R.color.bg_brand_primary_alt -> if (isDay) "#fdf5ef".toColorInt() else "#1a1a1e".toColorInt() // brand_50 -> gray_iron_900
        R.color.bg_brand_secondary -> if (isDay) "#fbe7d9".toColorInt() else "#d54221".toColorInt() // brand_100 -> brand_600
        R.color.bg_brand_section -> if (isDay) "#8d291f".toColorInt() else "#1a1a1e".toColorInt() // brand_800 -> gray_iron_900
        R.color.bg_brand_section_subtle -> if (isDay) "#b1311d".toColorInt() else "#131316".toColorInt() // brand_700 -> gray_iron_950
        R.color.bg_brand_solid -> "#d54221".toColorInt() // brand_600
        R.color.bg_brand_solid_hover -> if (isDay) "#b1311d".toColorInt() else "#e35728".toColorInt() // brand_700 -> brand_500
        R.color.bg_disabled -> if (isDay) "#f5f5f5".toColorInt() else "#26272b".toColorInt() // gray_100 -> gray_iron_800
        R.color.bg_disabled_subtle -> if (isDay) "#fafafa".toColorInt() else "#1a1a1e".toColorInt() // gray_50 -> gray_iron_900
        R.color.bg_error_primary -> if (isDay) "#fef3f2".toColorInt() else "#55160c".toColorInt() // error_50 -> error_950
        R.color.bg_error_secondary -> if (isDay) "#fee4e2".toColorInt() else "#d92d20".toColorInt() // error_100 -> error_600
        R.color.bg_error_solid -> "#d92d20".toColorInt() // error_600
        R.color.bg_overlay -> if (isDay) "#0a0d12".toColorInt() else "#26272b".toColorInt() // gray_950 -> gray_iron_800
        R.color.bg_primary -> if (isDay) "#ffffff".toColorInt() else "#131316".toColorInt() // white -> gray_iron_950
        R.color.bg_primary_900 -> if (isDay) "#181d27".toColorInt() else "#fafafa".toColorInt() // gray_900 -> gray_iron_50
        R.color.bg_primary_alt -> if (isDay) "#ffffff".toColorInt() else "#1a1a1e".toColorInt() // white -> gray_iron_900
        R.color.bg_primary_hover -> if (isDay) "#fafafa".toColorInt() else "#26272b".toColorInt() // gray_50 -> gray_iron_800
        R.color.bg_primary_solid -> if (isDay) "#0a0d12".toColorInt() else "#1a1a1e".toColorInt() // gray_950 -> gray_iron_900
        R.color.bg_quaternary -> if (isDay) "#e9eaeb".toColorInt() else "#3f3f46".toColorInt() // gray_200 -> gray_iron_700
        R.color.bg_secondary -> if (isDay) "#fafafa".toColorInt() else "#1a1a1e".toColorInt() // gray_50 -> gray_iron_900
        R.color.bg_secondary_alt -> if (isDay) "#fafafa".toColorInt() else "#131316".toColorInt() // gray_50 -> gray_iron_950
        R.color.bg_secondary_hover -> if (isDay) "#f5f5f5".toColorInt() else "#26272b".toColorInt() // gray_100 -> gray_iron_800
        R.color.bg_secondary_solid -> if (isDay) "#535862".toColorInt() else "#51525c".toColorInt() // gray_600 -> gray_iron_600
        R.color.bg_secondary_subtle -> if (isDay) "#fdfdfd".toColorInt() else "#1a1a1e".toColorInt() // gray_25 -> gray_iron_900
        R.color.bg_success_primary -> if (isDay) "#ecfdf3".toColorInt() else "#053321".toColorInt() // success_50 -> success_950
        R.color.bg_success_secondary -> if (isDay) "#dcfae6".toColorInt() else "#079455".toColorInt() // success_100 -> success_600
        R.color.bg_success_solid -> "#079455".toColorInt() // success_600
        R.color.bg_tertiary -> if (isDay) "#f5f5f5".toColorInt() else "#26272b".toColorInt() // gray_100 -> gray_iron_800
        R.color.bg_warning_primary -> if (isDay) "#fffaeb".toColorInt() else "#4e1d09".toColorInt() // warning_50 -> warning_950
        R.color.bg_warning_secondary -> if (isDay) "#fef0c7".toColorInt() else "#dc6803".toColorInt() // warning_100 -> warning_600
        R.color.bg_warning_solid -> "#dc6803".toColorInt() // warning_600

        // Border Colors
        R.color.border_brand -> if (isDay) "#e35728".toColorInt() else "#e97b4e".toColorInt() // brand_500 -> brand_400
        R.color.border_brand_alt -> if (isDay) "#d54221".toColorInt() else "#373a41".toColorInt() // brand_600 -> gray_700
        R.color.border_disabled -> if (isDay) "#d5d7da".toColorInt() else "#3f3f46".toColorInt() // gray_300 -> gray_iron_700
        R.color.border_disabled_subtle -> if (isDay) "#e9eaeb".toColorInt() else "#26272b".toColorInt() // gray_200 -> gray_iron_800
        R.color.border_error -> if (isDay) "#f04438".toColorInt() else "#f97066".toColorInt() // error_500 -> error_400
        R.color.border_error_subtle -> if (isDay) "#fda29b".toColorInt() else "#f04438".toColorInt() // error_300 -> error_500
        R.color.border_inverse -> if (isDay) "#ffffff".toColorInt() else "#000000".toColorInt() // white -> black
        R.color.border_primary -> if (isDay) "#d5d7da".toColorInt() else "#3f3f46".toColorInt() // gray_300 -> gray_iron_700
        R.color.border_primary_900 -> if (isDay) "#181d27".toColorInt() else "#fafafa".toColorInt() // gray_900 -> gray_iron_50
        R.color.border_secondary -> if (isDay) "#e9eaeb".toColorInt() else "#26272b".toColorInt() // gray_200 -> gray_iron_800
        R.color.border_secondary_alt -> if (isDay) "#000000".toColorInt() else "#3f3f46".toColorInt() // #000000 -> gray_iron_700
        R.color.border_tertiary -> if (isDay) "#f5f5f5".toColorInt() else "#26272b".toColorInt() // gray_100 -> gray_iron_800

        // Foreground Colors
        R.color.fg_brand_primary -> if (isDay) "#d54221".toColorInt() else "#e35728".toColorInt() // brand_600 -> brand_500
        R.color.fg_brand_primary_alt -> if (isDay) "#d54221".toColorInt() else "#cecfd2".toColorInt() // brand_600 -> gray_300
        R.color.fg_brand_secondary -> "#e35728".toColorInt() // brand_500
        R.color.fg_brand_secondary_alt -> if (isDay) "#e35728".toColorInt() else "#61656c".toColorInt() // brand_500 -> gray_600
        R.color.fg_brand_secondary_hover -> if (isDay) "#d54221".toColorInt() else "#85888e".toColorInt() // brand_600 -> gray_500
        R.color.fg_disabled -> if (isDay) "#a4a7ae".toColorInt() else "#85888e".toColorInt() // gray_400 -> gray_500
        R.color.fg_disabled_subtle -> if (isDay) "#d5d7da".toColorInt() else "#61656c".toColorInt() // gray_300 -> gray_600
        R.color.fg_error_primary -> if (isDay) "#d92d20".toColorInt() else "#f04438".toColorInt() // error_600 -> error_500
        R.color.fg_error_secondary -> if (isDay) "#f04438".toColorInt() else "#f97066".toColorInt() // error_500 -> error_400
        R.color.fg_primary -> if (isDay) "#181d27".toColorInt() else "#ffffff".toColorInt() // gray_900 -> white
        R.color.fg_quaternary -> if (isDay) "#a4a7ae".toColorInt() else "#61656c".toColorInt() // gray_400 -> gray_600
        R.color.fg_quaternary_hover -> if (isDay) "#717680".toColorInt() else "#85888e".toColorInt() // gray_500
        R.color.fg_secondary -> if (isDay) "#414651".toColorInt() else "#cecfd2".toColorInt() // gray_700 -> gray_300
        R.color.fg_secondary_hover -> if (isDay) "#252b37".toColorInt() else "#ececed".toColorInt() // gray_800 -> gray_200
        R.color.fg_success_primary -> if (isDay) "#079455".toColorInt() else "#17b26a".toColorInt() // success_600 -> success_500
        R.color.fg_success_secondary -> if (isDay) "#17b26a".toColorInt() else "#47cd89".toColorInt() // success_500 -> success_400
        R.color.fg_tertiary -> if (isDay) "#535862".toColorInt() else "#94979c".toColorInt() // gray_600 -> gray_400
        R.color.fg_tertiary_hover -> if (isDay) "#414651".toColorInt() else "#cecfd2".toColorInt() // gray_700 -> gray_300
        R.color.fg_warning_primary -> if (isDay) "#dc6803".toColorInt() else "#f79009".toColorInt() // warning_600 -> warning_500
        R.color.fg_warning_secondary -> if (isDay) "#f79009".toColorInt() else "#fdb022".toColorInt() // warning_500 -> warning_400
        R.color.fg_white -> "#ffffff".toColorInt() // white

        // Button Colors
        R.color.button_destructive_primary_icon -> "#fda29b".toColorInt() // error_300
        R.color.button_destructive_primary_icon_hover -> "#fecdca".toColorInt() // error_200
        R.color.button_primary_icon -> "#f0a881".toColorInt() // brand_300
        R.color.button_primary_icon_hover -> "#f6cbb2".toColorInt() // brand_200

        // Icon Colors
        R.color.featured_icon_light_fg_brand -> if (isDay) "#d54221".toColorInt() else "#f6cbb2".toColorInt() // brand_600 -> brand_200
        R.color.featured_icon_light_fg_error -> if (isDay) "#d92d20".toColorInt() else "#fecdca".toColorInt() // error_600 -> error_200
        R.color.featured_icon_light_fg_gray -> if (isDay) "#717680".toColorInt() else "#ececed".toColorInt() // gray_500 -> gray_200
        R.color.featured_icon_light_fg_success -> if (isDay) "#079455".toColorInt() else "#abefc6".toColorInt() // success_600 -> success_200
        R.color.featured_icon_light_fg_warning -> if (isDay) "#dc6803".toColorInt() else "#fedf89".toColorInt() // warning_600 -> warning_200
        R.color.icon_fg_brand_on_brand -> if (isDay) "#f6cbb2".toColorInt() else "#94979c".toColorInt() // brand_200 -> gray_400

        // Utility Colors
        R.color.utility_blue_100 -> if (isDay) "#d1e9ff".toColorInt() else "#194185".toColorInt() // blue_100 -> blue_900
        R.color.utility_blue_200 -> if (isDay) "#b2ddff".toColorInt() else "#1849a9".toColorInt() // blue_200 -> blue_800
        R.color.utility_blue_300 -> if (isDay) "#84caff".toColorInt() else "#175cd3".toColorInt() // blue_300 -> blue_700
        R.color.utility_blue_400 -> if (isDay) "#53b1fd".toColorInt() else "#1570ef".toColorInt() // blue_400 -> blue_600
        R.color.utility_blue_50 -> if (isDay) "#eff8ff".toColorInt() else "#102a56".toColorInt() // blue_50 -> blue_950
        R.color.utility_blue_500 -> "#2e90fa".toColorInt() // blue_500
        R.color.utility_blue_600 -> if (isDay) "#1570ef".toColorInt() else "#53b1fd".toColorInt() // blue_600 -> blue_400
        R.color.utility_blue_700 -> if (isDay) "#175cd3".toColorInt() else "#84caff".toColorInt() // blue_700 -> blue_300
        R.color.utility_blue_dark_100 -> if (isDay) "#d1e0ff".toColorInt() else "#00359e".toColorInt() // blue_dark_100 -> blue_dark_900
        R.color.utility_blue_dark_200 -> if (isDay) "#b2ccff".toColorInt() else "#0040c1".toColorInt() // blue_dark_200 -> blue_dark_800
        R.color.utility_blue_dark_300 -> if (isDay) "#84adff".toColorInt() else "#004eeb".toColorInt() // blue_dark_300 -> blue_dark_700
        R.color.utility_blue_dark_400 -> if (isDay) "#528bff".toColorInt() else "#155eef".toColorInt() // blue_dark_400 -> blue_dark_600
        R.color.utility_blue_dark_50 -> if (isDay) "#eff4ff".toColorInt() else "#002266".toColorInt() // blue_dark_50 -> blue_dark_950
        R.color.utility_blue_dark_500 -> "#2970ff".toColorInt() // blue_dark_500
        R.color.utility_blue_dark_600 -> if (isDay) "#155eef".toColorInt() else "#528bff".toColorInt() // blue_dark_600 -> blue_dark_400
        R.color.utility_blue_dark_700 -> if (isDay) "#004eeb".toColorInt() else "#84adff".toColorInt() // blue_dark_700 -> blue_dark_300
        R.color.utility_blue_light_100 -> if (isDay) "#e0f2fe".toColorInt() else "#0b4a6f".toColorInt() // blue_light_100 -> blue_light_900
        R.color.utility_blue_light_200 -> if (isDay) "#b9e6fe".toColorInt() else "#065986".toColorInt() // blue_light_200 -> blue_light_800
        R.color.utility_blue_light_300 -> if (isDay) "#7cd4fd".toColorInt() else "#026aa2".toColorInt() // blue_light_300 -> blue_light_700
        R.color.utility_blue_light_400 -> if (isDay) "#36bffa".toColorInt() else "#0086c9".toColorInt() // blue_light_400 -> blue_light_600
        R.color.utility_blue_light_50 -> if (isDay) "#f0f9ff".toColorInt() else "#062c41".toColorInt() // blue_light_50 -> blue_light_950
        R.color.utility_blue_light_500 -> "#0ba5ec".toColorInt() // blue_light_500
        R.color.utility_blue_light_600 -> if (isDay) "#0086c9".toColorInt() else "#36bffa".toColorInt() // blue_light_600 -> blue_light_400
        R.color.utility_blue_light_700 -> if (isDay) "#026aa2".toColorInt() else "#7cd4fd".toColorInt() // blue_light_700 -> blue_light_300
        R.color.utility_brand_100 -> if (isDay) "#fbe7d9".toColorInt() else "#391004".toColorInt() // brand_100 -> brand_900
        R.color.utility_brand_100_alt -> if (isDay) "#fbe7d9".toColorInt() else "#22262f".toColorInt() // brand_100 -> gray_800
        R.color.utility_brand_200 -> if (isDay) "#f6cbb2".toColorInt() else "#8d291f".toColorInt() // brand_200 -> brand_800
        R.color.utility_brand_200_alt -> if (isDay) "#f6cbb2".toColorInt() else "#373a41".toColorInt() // brand_200 -> gray_700
        R.color.utility_brand_300 -> if (isDay) "#f0a881".toColorInt() else "#b1311d".toColorInt() // brand_300 -> brand_700
        R.color.utility_brand_300_alt -> if (isDay) "#f0a881".toColorInt() else "#373a41".toColorInt() // brand_300 -> gray_700
        R.color.utility_brand_400 -> if (isDay) "#e97b4e".toColorInt() else "#d54221".toColorInt() // brand_400 -> brand_600
        R.color.utility_brand_400_alt -> if (isDay) "#e97b4e".toColorInt() else "#61656c".toColorInt() // brand_400 -> gray_600
        R.color.utility_brand_50 -> if (isDay) "#fdf5ef".toColorInt() else "#290902".toColorInt() // brand_50 -> brand_950
        R.color.utility_brand_500 -> "#e35728".toColorInt() // brand_500
        R.color.utility_brand_500_alt -> if (isDay) "#e35728".toColorInt() else "#85888e".toColorInt() // brand_500 -> gray_500
        R.color.utility_brand_50_alt -> if (isDay) "#fdf5ef".toColorInt() else "#13161b".toColorInt() // brand_50 -> gray_900
        R.color.utility_brand_600 -> if (isDay) "#d54221".toColorInt() else "#e97b4e".toColorInt() // brand_600 -> brand_400
        R.color.utility_brand_600_alt -> if (isDay) "#d54221".toColorInt() else "#94979c".toColorInt() // brand_600 -> gray_400
        R.color.utility_brand_700 -> if (isDay) "#b1311d".toColorInt() else "#f0a881".toColorInt() // brand_700 -> brand_300
        R.color.utility_brand_700_alt -> if (isDay) "#b1311d".toColorInt() else "#cecfd2".toColorInt() // brand_700 -> gray_300
        R.color.utility_brand_800 -> if (isDay) "#8d291f".toColorInt() else "#f6cbb2".toColorInt() // brand_800 -> brand_200
        R.color.utility_brand_800_alt -> if (isDay) "#8d291f".toColorInt() else "#ececed".toColorInt() // brand_800 -> gray_200
        R.color.utility_brand_900 -> if (isDay) "#391004".toColorInt() else "#fbe7d9".toColorInt() // brand_900 -> brand_100
        R.color.utility_brand_900_alt -> if (isDay) "#391004".toColorInt() else "#f0f0f1".toColorInt() // brand_900 -> gray_100
        R.color.utility_error_100 -> if (isDay) "#fee4e2".toColorInt() else "#7a271a".toColorInt() // error_100 -> error_900
        R.color.utility_error_200 -> if (isDay) "#fecdca".toColorInt() else "#912018".toColorInt() // error_200 -> error_800
        R.color.utility_error_300 -> if (isDay) "#fda29b".toColorInt() else "#b42318".toColorInt() // error_300 -> error_700
        R.color.utility_error_400 -> if (isDay) "#f97066".toColorInt() else "#d92d20".toColorInt() // error_400 -> error_600
        R.color.utility_error_50 -> if (isDay) "#fef3f2".toColorInt() else "#55160c".toColorInt() // error_50 -> error_950
        R.color.utility_error_500 -> "#f04438".toColorInt() // error_500
        R.color.utility_error_600 -> if (isDay) "#d92d20".toColorInt() else "#f97066".toColorInt() // error_600 -> error_400
        R.color.utility_error_700 -> if (isDay) "#b42318".toColorInt() else "#fda29b".toColorInt() // error_700 -> error_300
        R.color.utility_fuchsia_100 -> if (isDay) "#fbe8ff".toColorInt() else "#6f1877".toColorInt() // fuchsia_100 -> fuchsia_900
        R.color.utility_fuchsia_200 -> if (isDay) "#f6d0fe".toColorInt() else "#821890".toColorInt() // fuchsia_200 -> fuchsia_800
        R.color.utility_fuchsia_300 -> if (isDay) "#eeaafd".toColorInt() else "#9f1ab1".toColorInt() // fuchsia_300 -> fuchsia_700
        R.color.utility_fuchsia_400 -> if (isDay) "#e478fa".toColorInt() else "#ba24d5".toColorInt() // fuchsia_400 -> fuchsia_600
        R.color.utility_fuchsia_50 -> if (isDay) "#fdf4ff".toColorInt() else "#47104c".toColorInt() // fuchsia_50 -> fuchsia_950
        R.color.utility_fuchsia_500 -> "#d444f1".toColorInt() // fuchsia_500
        R.color.utility_fuchsia_600 -> if (isDay) "#ba24d5".toColorInt() else "#e478fa".toColorInt() // fuchsia_600 -> fuchsia_400
        R.color.utility_fuchsia_700 -> if (isDay) "#9f1ab1".toColorInt() else "#eeaafd".toColorInt() // fuchsia_700 -> fuchsia_300
        R.color.utility_gray_100 -> if (isDay) "#f5f5f5".toColorInt() else "#22262f".toColorInt() // gray_100 -> gray_800
        R.color.utility_gray_200 -> if (isDay) "#e9eaeb".toColorInt() else "#373a41".toColorInt() // gray_200 -> gray_700
        R.color.utility_gray_300 -> if (isDay) "#d5d7da".toColorInt() else "#373a41".toColorInt() // gray_300 -> gray_700
        R.color.utility_gray_400 -> if (isDay) "#a4a7ae".toColorInt() else "#61656c".toColorInt() // gray_400 -> gray_600
        R.color.utility_gray_50 -> if (isDay) "#fafafa".toColorInt() else "#13161b".toColorInt() // gray_50 -> gray_900
        R.color.utility_gray_500 -> if (isDay) "#717680".toColorInt() else "#85888e".toColorInt() // gray_500
        R.color.utility_gray_600 -> if (isDay) "#535862".toColorInt() else "#94979c".toColorInt() // gray_600 -> gray_400
        R.color.utility_gray_700 -> if (isDay) "#414651".toColorInt() else "#cecfd2".toColorInt() // gray_700 -> gray_300
        R.color.utility_gray_800 -> if (isDay) "#252b37".toColorInt() else "#ececed".toColorInt() // gray_800 -> gray_200
        R.color.utility_gray_900 -> if (isDay) "#181d27".toColorInt() else "#f0f0f1".toColorInt() // gray_900 -> gray_100
        R.color.utility_gray_blue_100 -> if (isDay) "#eaecf5".toColorInt() else "#101323".toColorInt() // gray_blue_100 -> gray_blue_900
        R.color.utility_gray_blue_200 -> if (isDay) "#d5d9eb".toColorInt() else "#293056".toColorInt() // gray_blue_200 -> gray_blue_800
        R.color.utility_gray_blue_300 -> if (isDay) "#b3b8db".toColorInt() else "#363f72".toColorInt() // gray_blue_300 -> gray_blue_700
        R.color.utility_gray_blue_400 -> if (isDay) "#717bbc".toColorInt() else "#3e4784".toColorInt() // gray_blue_400 -> gray_blue_600
        R.color.utility_gray_blue_50 -> if (isDay) "#f8f9fc".toColorInt() else "#0d0f1c".toColorInt() // gray_blue_50 -> gray_blue_950
        R.color.utility_gray_blue_500 -> "#4e5ba6".toColorInt() // gray_blue_500
        R.color.utility_gray_blue_600 -> if (isDay) "#3e4784".toColorInt() else "#717bbc".toColorInt() // gray_blue_600 -> gray_blue_400
        R.color.utility_gray_blue_700 -> if (isDay) "#363f72".toColorInt() else "#b3b8db".toColorInt() // gray_blue_700 -> gray_blue_300
        R.color.utility_green_100 -> if (isDay) "#d3f8df".toColorInt() else "#084c2e".toColorInt() // green_100 -> green_900
        R.color.utility_green_200 -> if (isDay) "#aaf0c4".toColorInt() else "#095c37".toColorInt() // green_200 -> green_800
        R.color.utility_green_300 -> if (isDay) "#73e2a3".toColorInt() else "#087443".toColorInt() // green_300 -> green_700
        R.color.utility_green_400 -> if (isDay) "#3ccb7f".toColorInt() else "#099250".toColorInt() // green_400 -> green_600
        R.color.utility_green_50 -> if (isDay) "#edfcf2".toColorInt() else "#052e1c".toColorInt() // green_50 -> green_950
        R.color.utility_green_500 -> "#16b364".toColorInt() // green_500
        R.color.utility_green_600 -> if (isDay) "#099250".toColorInt() else "#3ccb7f".toColorInt() // green_600 -> green_400
        R.color.utility_green_700 -> if (isDay) "#087443".toColorInt() else "#73e2a3".toColorInt() // green_700 -> green_300
        R.color.utility_indigo_100 -> if (isDay) "#e0eaff".toColorInt() else "#2d3282".toColorInt() // indigo_100 -> indigo_900
        R.color.utility_indigo_200 -> if (isDay) "#c7d7fe".toColorInt() else "#2d31a6".toColorInt() // indigo_200 -> indigo_800
        R.color.utility_indigo_300 -> if (isDay) "#a4bcfd".toColorInt() else "#3538cd".toColorInt() // indigo_300 -> indigo_700
        R.color.utility_indigo_400 -> if (isDay) "#8098f9".toColorInt() else "#444ce7".toColorInt() // indigo_400 -> indigo_600
        R.color.utility_indigo_50 -> if (isDay) "#eef4ff".toColorInt() else "#1f235b".toColorInt() // indigo_50 -> indigo_950
        R.color.utility_indigo_500 -> "#6172f3".toColorInt() // indigo_500
        R.color.utility_indigo_600 -> if (isDay) "#444ce7".toColorInt() else "#8098f9".toColorInt() // indigo_600 -> indigo_400
        R.color.utility_indigo_700 -> if (isDay) "#3538cd".toColorInt() else "#a4bcfd".toColorInt() // indigo_700 -> indigo_300
        R.color.utility_orange_100 -> if (isDay) "#fdead7".toColorInt() else "#772917".toColorInt() // orange_100 -> orange_900
        R.color.utility_orange_200 -> if (isDay) "#f9dbaf".toColorInt() else "#932f19".toColorInt() // orange_200 -> orange_800
        R.color.utility_orange_300 -> if (isDay) "#f7b27a".toColorInt() else "#b93815".toColorInt() // orange_300 -> orange_700
        R.color.utility_orange_400 -> if (isDay) "#f38744".toColorInt() else "#e04f16".toColorInt() // orange_400 -> orange_600
        R.color.utility_orange_50 -> if (isDay) "#fef6ee".toColorInt() else "#511c10".toColorInt() // orange_50 -> orange_950
        R.color.utility_orange_500 -> "#ef6820".toColorInt() // orange_500
        R.color.utility_orange_600 -> if (isDay) "#e04f16".toColorInt() else "#f38744".toColorInt() // orange_600 -> orange_400
        R.color.utility_orange_700 -> if (isDay) "#b93815".toColorInt() else "#f7b27a".toColorInt() // orange_700 -> orange_300
        R.color.utility_orange_dark_100 -> if (isDay) "#ffe6d5".toColorInt() else "#771a0d".toColorInt() // orange_dark_100 -> orange_dark_900
        R.color.utility_orange_dark_200 -> if (isDay) "#ffd6ae".toColorInt() else "#97180c".toColorInt() // orange_dark_200 -> orange_dark_800
        R.color.utility_orange_dark_300 -> if (isDay) "#ff9c66".toColorInt() else "#bc1b06".toColorInt() // orange_dark_300 -> orange_dark_700
        R.color.utility_orange_dark_400 -> if (isDay) "#ff692e".toColorInt() else "#e62e05".toColorInt() // orange_dark_400 -> orange_dark_600
        R.color.utility_orange_dark_50 -> if (isDay) "#fff4ed".toColorInt() else "#57130a".toColorInt() // orange_dark_50 -> orange_dark_950
        R.color.utility_orange_dark_500 -> "#ff4405".toColorInt() // orange_dark_500
        R.color.utility_orange_dark_600 -> if (isDay) "#e62e05".toColorInt() else "#ff692e".toColorInt() // orange_dark_600 -> orange_dark_400
        R.color.utility_orange_dark_700 -> if (isDay) "#bc1b06".toColorInt() else "#ff9c66".toColorInt() // orange_dark_700 -> orange_dark_300
        R.color.utility_pink_100 -> if (isDay) "#fce7f6".toColorInt() else "#851651".toColorInt() // pink_100 -> pink_900
        R.color.utility_pink_200 -> if (isDay) "#fcceee".toColorInt() else "#9e165f".toColorInt() // pink_200 -> pink_800
        R.color.utility_pink_300 -> if (isDay) "#faa7e0".toColorInt() else "#c11574".toColorInt() // pink_300 -> pink_700
        R.color.utility_pink_400 -> if (isDay) "#f670c7".toColorInt() else "#dd2590".toColorInt() // pink_400 -> pink_600
        R.color.utility_pink_50 -> if (isDay) "#fdf2fa".toColorInt() else "#4e0d30".toColorInt() // pink_50 -> pink_950
        R.color.utility_pink_500 -> "#ee46bc".toColorInt() // pink_500
        R.color.utility_pink_600 -> if (isDay) "#dd2590".toColorInt() else "#f670c7".toColorInt() // pink_600 -> pink_400
        R.color.utility_pink_700 -> if (isDay) "#c11574".toColorInt() else "#faa7e0".toColorInt() // pink_700 -> pink_300
        R.color.utility_purple_100 -> if (isDay) "#ebe9fe".toColorInt() else "#3e1c96".toColorInt() // purple_100 -> purple_900
        R.color.utility_purple_200 -> if (isDay) "#d9d6fe".toColorInt() else "#4a1fb8".toColorInt() // purple_200 -> purple_800
        R.color.utility_purple_300 -> if (isDay) "#bdb4fe".toColorInt() else "#5925dc".toColorInt() // purple_300 -> purple_700
        R.color.utility_purple_400 -> if (isDay) "#9b8afb".toColorInt() else "#6938ef".toColorInt() // purple_400 -> purple_600
        R.color.utility_purple_50 -> if (isDay) "#f4f3ff".toColorInt() else "#27115f".toColorInt() // purple_50 -> purple_950
        R.color.utility_purple_500 -> "#7a5af8".toColorInt() // purple_500
        R.color.utility_purple_600 -> if (isDay) "#6938ef".toColorInt() else "#9b8afb".toColorInt() // purple_600 -> purple_400
        R.color.utility_purple_700 -> if (isDay) "#5925dc".toColorInt() else "#bdb4fe".toColorInt() // purple_700 -> purple_300
        R.color.utility_success_100 -> if (isDay) "#dcfae6".toColorInt() else "#074d31".toColorInt() // success_100 -> success_900
        R.color.utility_success_200 -> if (isDay) "#abefc6".toColorInt() else "#085d3a".toColorInt() // success_200 -> success_800
        R.color.utility_success_300 -> if (isDay) "#75e0a7".toColorInt() else "#067647".toColorInt() // success_300 -> success_700
        R.color.utility_success_400 -> if (isDay) "#47cd89".toColorInt() else "#079455".toColorInt() // success_400 -> success_600
        R.color.utility_success_50 -> if (isDay) "#ecfdf3".toColorInt() else "#053321".toColorInt() // success_50 -> success_950
        R.color.utility_success_500 -> "#17b26a".toColorInt() // success_500
        R.color.utility_success_600 -> if (isDay) "#079455".toColorInt() else "#47cd89".toColorInt() // success_600 -> success_400
        R.color.utility_success_700 -> if (isDay) "#067647".toColorInt() else "#75e0a7".toColorInt() // success_700 -> success_300
        R.color.utility_warning_100 -> if (isDay) "#fef0c7".toColorInt() else "#7a2e0e".toColorInt() // warning_100 -> warning_900
        R.color.utility_warning_200 -> if (isDay) "#fedf89".toColorInt() else "#93370d".toColorInt() // warning_200 -> warning_800
        R.color.utility_warning_300 -> if (isDay) "#fec84b".toColorInt() else "#b54708".toColorInt() // warning_300 -> warning_700
        R.color.utility_warning_400 -> if (isDay) "#fdb022".toColorInt() else "#dc6803".toColorInt() // warning_400 -> warning_600
        R.color.utility_warning_50 -> if (isDay) "#fffaeb".toColorInt() else "#4e1d09".toColorInt() // warning_50 -> warning_950
        R.color.utility_warning_500 -> "#f79009".toColorInt() // warning_500
        R.color.utility_warning_600 -> if (isDay) "#dc6803".toColorInt() else "#fdb022".toColorInt() // warning_600 -> warning_400
        R.color.utility_warning_700 -> if (isDay) "#b54708".toColorInt() else "#fec84b".toColorInt() // warning_700 -> warning_300
        R.color.utility_yellow_100 -> if (isDay) "#fef7c3".toColorInt() else "#713b12".toColorInt() // yellow_100 -> yellow_900
        R.color.utility_yellow_200 -> if (isDay) "#feee95".toColorInt() else "#854a0e".toColorInt() // yellow_200 -> yellow_800
        R.color.utility_yellow_300 -> if (isDay) "#fde272".toColorInt() else "#a15c07".toColorInt() // yellow_300 -> yellow_700
        R.color.utility_yellow_400 -> if (isDay) "#fac515".toColorInt() else "#ca8504".toColorInt() // yellow_400 -> yellow_600
        R.color.utility_yellow_50 -> if (isDay) "#fefbe8".toColorInt() else "#542c0d".toColorInt() // yellow_50 -> yellow_950
        R.color.utility_yellow_500 -> "#eaaa08".toColorInt() // yellow_500
        R.color.utility_yellow_600 -> if (isDay) "#ca8504".toColorInt() else "#fac515".toColorInt() // yellow_600 -> yellow_400
        R.color.utility_yellow_700 -> if (isDay) "#a15c07".toColorInt() else "#fde272".toColorInt() // yellow_700 -> yellow_300

        // Other Colors
        R.color.alpha_black_10 -> if (isDay) "#000000".toColorInt() else "#ffffff".toColorInt() // #000000 -> #ffffff
        R.color.alpha_black_100 -> if (isDay) "#000000".toColorInt() else "#ffffff".toColorInt() // #000000 -> #ffffff
        R.color.alpha_black_20 -> if (isDay) "#000000".toColorInt() else "#ffffff".toColorInt() // #000000 -> #ffffff
        R.color.alpha_black_30 -> if (isDay) "#000000".toColorInt() else "#ffffff".toColorInt() // #000000 -> #ffffff
        R.color.alpha_black_40 -> if (isDay) "#000000".toColorInt() else "#ffffff".toColorInt() // #000000 -> #ffffff
        R.color.alpha_black_50 -> if (isDay) "#000000".toColorInt() else "#ffffff".toColorInt() // #000000 -> #ffffff
        R.color.alpha_black_60 -> if (isDay) "#000000".toColorInt() else "#ffffff".toColorInt() // #000000 -> #ffffff
        R.color.alpha_black_70 -> if (isDay) "#000000".toColorInt() else "#ffffff".toColorInt() // #000000 -> #ffffff
        R.color.alpha_black_80 -> if (isDay) "#000000".toColorInt() else "#ffffff".toColorInt() // #000000 -> #ffffff
        R.color.alpha_black_90 -> if (isDay) "#000000".toColorInt() else "#ffffff".toColorInt() // #000000 -> #ffffff
        R.color.alpha_white_10 -> if (isDay) "#ffffff".toColorInt() else "#0c0e12".toColorInt() // #ffffff -> #0c0e12
        R.color.alpha_white_100 -> if (isDay) "#ffffff".toColorInt() else "#0c0e12".toColorInt() // white -> gray_950
        R.color.alpha_white_20 -> if (isDay) "#ffffff".toColorInt() else "#0c0e12".toColorInt() // #ffffff -> #0c0e12
        R.color.alpha_white_30 -> if (isDay) "#ffffff".toColorInt() else "#0c0e12".toColorInt() // #ffffff -> #0c0e12
        R.color.alpha_white_40 -> if (isDay) "#ffffff".toColorInt() else "#0c0e12".toColorInt() // #ffffff -> #0c0e12
        R.color.alpha_white_50 -> if (isDay) "#ffffff".toColorInt() else "#0c0e12".toColorInt() // #ffffff -> #0c0e12
        R.color.alpha_white_60 -> if (isDay) "#ffffff".toColorInt() else "#0c0e12".toColorInt() // #ffffff -> #0c0e12
        R.color.alpha_white_70 -> if (isDay) "#ffffff".toColorInt() else "#0c0e12".toColorInt() // #ffffff -> #0c0e12
        R.color.alpha_white_80 -> if (isDay) "#ffffff".toColorInt() else "#0c0e12".toColorInt() // #ffffff -> #0c0e12
        R.color.alpha_white_90 -> if (isDay) "#ffffff".toColorInt() else "#0c0e12".toColorInt() // #ffffff -> #0c0e12
        R.color.app_store_badge_border -> if (isDay) "#a3a3a3".toColorInt() else "#ffffff".toColorInt() // gray_true_400 -> white
        R.color.avatar_styles_bg_neutral -> "#e5e5e5".toColorInt() // gray_true_200
        R.color.focus_ring -> "#e35728".toColorInt() // brand_500
        R.color.focus_ring_error -> "#f04438".toColorInt() // error_500
        R.color.footer_button_fg -> if (isDay) "#f6cbb2".toColorInt() else "#cecfd2".toColorInt() // brand_200 -> gray_300
        R.color.footer_button_fg_hover -> if (isDay) "#ffffff".toColorInt() else "#f0f0f1".toColorInt() // white -> gray_100
        R.color.screen_mockup_border -> if (isDay) "#181d27".toColorInt() else "#373a41".toColorInt() // gray_900 -> gray_700
        R.color.shadow_2xl_01 -> if (isDay) "#0a0d12".toColorInt() else "#ffffff".toColorInt() // #0a0d12 -> transparent
        R.color.shadow_2xl_02 -> if (isDay) "#0a0d12".toColorInt() else "#ffffff".toColorInt() // #0a0d12 -> transparent
        R.color.shadow_3xl_01 -> if (isDay) "#0a0d12".toColorInt() else "#ffffff".toColorInt() // #0a0d12 -> transparent
        R.color.shadow_3xl_02 -> if (isDay) "#0a0d12".toColorInt() else "#ffffff".toColorInt() // #0a0d12 -> transparent
        R.color.shadow_grid_md -> if (isDay) "#0a0d12".toColorInt() else "#ffffff".toColorInt() // #0a0d12 -> transparent
        R.color.shadow_lg_01 -> if (isDay) "#0a0d12".toColorInt() else "#ffffff".toColorInt() // #0a0d12 -> transparent
        R.color.shadow_lg_02 -> if (isDay) "#0a0d12".toColorInt() else "#ffffff".toColorInt() // #0a0d12 -> transparent
        R.color.shadow_lg_03 -> if (isDay) "#0a0d12".toColorInt() else "#ffffff".toColorInt() // #0a0d12 -> transparent
        R.color.shadow_main_centre_lg -> if (isDay) "#0a0d12".toColorInt() else "#ffffff".toColorInt() // #0a0d12 -> transparent
        R.color.shadow_main_centre_md -> if (isDay) "#0a0d12".toColorInt() else "#ffffff".toColorInt() // #0a0d12 -> transparent
        R.color.shadow_md_01 -> if (isDay) "#0a0d12".toColorInt() else "#ffffff".toColorInt() // #0a0d12 -> transparent
        R.color.shadow_md_02 -> if (isDay) "#0a0d12".toColorInt() else "#ffffff".toColorInt() // #0a0d12 -> transparent
        R.color.shadow_overlay_lg -> if (isDay) "#0a0d12".toColorInt() else "#ffffff".toColorInt() // #0a0d12 -> transparent
        R.color.shadow_skeumorphic_inner -> if (isDay) "#0a0d12".toColorInt() else "#0c0e12".toColorInt() // #0a0d12 -> #0c0e12
        R.color.shadow_skeumorphic_inner_border -> if (isDay) "#0a0d12".toColorInt() else "#0c0e12".toColorInt() // #0a0d12 -> #0c0e12
        R.color.shadow_sm_01 -> if (isDay) "#0a0d12".toColorInt() else "#ffffff".toColorInt() // #0a0d12 -> transparent
        R.color.shadow_sm_02 -> if (isDay) "#0a0d12".toColorInt() else "#ffffff".toColorInt() // #0a0d12 -> transparent
        R.color.shadow_xl_01 -> if (isDay) "#0a0d12".toColorInt() else "#ffffff".toColorInt() // #0a0d12 -> transparent
        R.color.shadow_xl_02 -> if (isDay) "#0a0d12".toColorInt() else "#ffffff".toColorInt() // #0a0d12 -> transparent
        R.color.shadow_xl_03 -> if (isDay) "#0a0d12".toColorInt() else "#ffffff".toColorInt() // #0a0d12 -> transparent
        R.color.shadow_xs -> if (isDay) "#0a0d12".toColorInt() else "#ffffff".toColorInt() // #0a0d12 -> transparent
        R.color.slider_handle_bg -> if (isDay) "#ffffff".toColorInt() else "#e35728".toColorInt() // white -> brand_500
        R.color.slider_handle_border -> if (isDay) "#d54221".toColorInt() else "#131316".toColorInt() // brand_600 -> gray_iron_950
        R.color.toggle_border -> if (isDay) "#d5d7da".toColorInt() else "#ffffff".toColorInt() // gray_300 -> transparent
        R.color.toggle_button_fg_disabled -> if (isDay) "#fafafa".toColorInt() else "#61656c".toColorInt() // gray_50 -> gray_600
        R.color.toggle_slim_border_pressed -> if (isDay) "#d54221".toColorInt() else "#ffffff".toColorInt() // brand_600 -> transparent
        R.color.toggle_slim_border_pressed_hover -> if (isDay) "#b1311d".toColorInt() else "#ffffff".toColorInt() // brand_700 -> transparent
        R.color.tooltip_supporting_text -> if (isDay) "#d5d7da".toColorInt() else "#cecfd2".toColorInt() // gray_300
        // 默认颜色
        else -> "#000000".toColorInt() // black
    }
}