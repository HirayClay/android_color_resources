package com.example.design.tokens

import android.animation.Animator
import android.animation.AnimatorListenerAdapter
import android.animation.ValueAnimator
import android.content.Context
import android.graphics.Canvas
import android.graphics.Paint
import android.graphics.Path
import android.graphics.RectF
import android.util.AttributeSet
import android.view.View
import android.view.animation.AccelerateDecelerateInterpolator

class RadiusView @JvmOverloads constructor(
    context: Context,
    attrs: AttributeSet? = null,
    defStyleAttr: Int = 0
) : View(context, attrs, defStyleAttr) {

    private val paint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        color = 0xFF3F51B5.toInt()
        style = Paint.Style.FILL
    }
    
    private var currentRadius: AppRadius = AppRadius.MD
    private var animatedRadius: Float = currentRadius.value.toFloat()
    private var isFullMode: Boolean = false
    private var animatedFullMode: Float = 0f
    private var transitionProgress: Float = 0f
    private val path = Path()
    private val rectF = RectF()
    
    private var radiusAnimator: ValueAnimator? = null
    private val defaultDuration = 300L
    
    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)
        
        val width = width.toFloat()
        val height = height.toFloat()
        
        if (width <= 0 || height <= 0) return
        
        path.reset()
        
        rectF.set(0f, 0f, width, height)
        
        if (isFullMode) {
            val maxRadius = Math.min(width, height) / 2f
            val currentRadiusValue = animatedRadius + (maxRadius - animatedRadius) * animatedFullMode
            
            if (animatedFullMode < 1f) {
                path.addRoundRect(rectF, currentRadiusValue, currentRadiusValue, Path.Direction.CW)
            } else {
                path.addCircle(width / 2f, height / 2f, maxRadius, Path.Direction.CW)
            }
        } else {
            val maxRadius = Math.min(width, height) / 2f
            val currentRadiusValue = maxRadius + (animatedRadius - maxRadius) * (1f - animatedFullMode)
            
            if (animatedFullMode > 0f) {
                path.addRoundRect(rectF, currentRadiusValue, currentRadiusValue, Path.Direction.CW)
            } else {
                path.addRoundRect(rectF, animatedRadius, animatedRadius, Path.Direction.CW)
            }
        }
        
        canvas.drawPath(path, paint)
    }
    
    fun setRadius(radius: AppRadius) {
        setRadius(radius, defaultDuration)
    }
    
    fun setRadius(radius: AppRadius, duration: Long) {
        if (currentRadius == radius) return
        
        val oldRadius = currentRadius
        val oldIsFullMode = isFullMode
        currentRadius = radius
        isFullMode = radius == AppRadius.FULL
        
        radiusAnimator?.cancel()
        
        when {
            oldIsFullMode || isFullMode -> {
                animateFullModeTransition(oldIsFullMode, isFullMode, oldRadius, radius, duration)
            }
            else -> {
                animateRadiusChange(oldRadius.value.toFloat(), radius.value.toFloat(), duration)
            }
        }
    }
    
    private fun animateRadiusChange(fromRadius: Float, toRadius: Float, duration: Long) {
        radiusAnimator = ValueAnimator.ofFloat(fromRadius, toRadius).apply {
            this.duration = duration
            interpolator = AccelerateDecelerateInterpolator()
            
            addUpdateListener { animation ->
                animatedRadius = animation.animatedValue as Float
                invalidate()
            }
            
            addListener(object : AnimatorListenerAdapter() {
                override fun onAnimationEnd(animation: Animator) {
                    radiusAnimator = null
                }
            })
            
            start()
        }
    }
    
    private fun animateFullModeTransition(fromFullMode: Boolean, toFullMode: Boolean, oldRadius: AppRadius, newRadius: AppRadius, duration: Long) {
        val width = width.toFloat()
        val height = height.toFloat()
        
        if (width <= 0 || height <= 0) {
            animatedRadius = newRadius.value.toFloat()
            animatedFullMode = if (toFullMode) 1f else 0f
            invalidate()
            return
        }
        
        val maxRadius = Math.min(width, height) / 2f
        
        radiusAnimator = ValueAnimator.ofFloat(if (fromFullMode) 1f else 0f, if (toFullMode) 1f else 0f).apply {
            this.duration = duration
            interpolator = AccelerateDecelerateInterpolator()
            
            addUpdateListener { animation ->
                animatedFullMode = animation.animatedValue as Float
                
                if (toFullMode) {
                    animatedRadius = oldRadius.value.toFloat() + (maxRadius - oldRadius.value.toFloat()) * animatedFullMode
                } else {
                    animatedRadius = maxRadius + (newRadius.value.toFloat() - maxRadius) * (1f - animatedFullMode)
                }
                
                invalidate()
            }
            
            addListener(object : AnimatorListenerAdapter() {
                override fun onAnimationEnd(animation: Animator) {
                    radiusAnimator = null
                    if (!toFullMode) {
                        animatedRadius = newRadius.value.toFloat()
                        animatedFullMode = 0f
                    }
                }
            })
            
            start()
        }
    }
    
    fun setRadiusImmediate(radius: AppRadius) {
        if (currentRadius != radius) {
            currentRadius = radius
            isFullMode = radius == AppRadius.FULL
            animatedRadius = radius.value.toFloat()
            animatedFullMode = if (isFullMode) 1f else 0f
            invalidate()
        }
    }
    
    fun getCurrentRadius(): AppRadius = currentRadius
    
    fun setViewColor(color: Int) {
        if (paint.color != color) {
            paint.color = color
            invalidate()
        }
    }
    
    override fun onMeasure(widthMeasureSpec: Int, heightMeasureSpec: Int) {
        val desiredWidth = 200
        val desiredHeight = 200
        
        val widthMode = MeasureSpec.getMode(widthMeasureSpec)
        val widthSize = MeasureSpec.getSize(widthMeasureSpec)
        val heightMode = MeasureSpec.getMode(heightMeasureSpec)
        val heightSize = MeasureSpec.getSize(heightMeasureSpec)
        
        val finalWidth = when (widthMode) {
            MeasureSpec.EXACTLY -> widthSize
            MeasureSpec.AT_MOST -> Math.min(desiredWidth, widthSize)
            else -> desiredWidth
        }
        
        val finalHeight = when (heightMode) {
            MeasureSpec.EXACTLY -> heightSize
            MeasureSpec.AT_MOST -> Math.min(desiredHeight, heightSize)
            else -> desiredHeight
        }
        
        setMeasuredDimension(finalWidth, finalHeight)
    }
}