package com.example.design.tokens

enum class AppRadius(
    val value: Int,
    val dimenRes: Int
) {
    NONE(0, R.dimen.radius_none),
    XXS(2, R.dimen.radius_xxs),
    XS(4, R.dimen.radius_xs),
    SM(6, R.dimen.radius_sm),
    MD(8, R.dimen.radius_md),
    LG(10, R.dimen.radius_lg),
    XL(12, R.dimen.radius_xl),
    TWO_XL(16, R.dimen.radius_2xl),
    THREE_XL(20, R.dimen.radius_3xl),
    FOUR_XL(24, R.dimen.radius_4xl),
    FIVE_XL(28, R.dimen.radius_5xl),
    FULL(9999, R.dimen.radius_full);
    
    companion object {
        fun fromValue(value: Int): AppRadius {
            return entries.find { it.value == value } ?: MD
        }
        
        fun fromDimenRes(res: Int): AppRadius {
            return entries.find { it.dimenRes == res } ?: MD
        }
    }
}