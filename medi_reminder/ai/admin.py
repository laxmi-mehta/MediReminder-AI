"""
Admin configuration for the ai app.

This module configures the Django admin interface for AI-related models.
"""

from django.contrib import admin
from .models import OCRResult, MedicationRecognition, AIInsight


@admin.register(OCRResult)
class OCRResultAdmin(admin.ModelAdmin):
    """
    Admin configuration for OCRResult model.
    
    Provides interface for managing OCR results in Django admin.
    """
    list_display = [
        'id', 'image', 'confidence_score', 'processing_time', 'created_at'
    ]
    list_filter = [
        'confidence_score', 'created_at'
    ]
    search_fields = [
        'extracted_text'
    ]
    ordering = ['-created_at']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Image', {
            'fields': ('image',)
        }),
        ('OCR Results', {
            'fields': ('extracted_text', 'confidence_score', 'processing_time')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(MedicationRecognition)
class MedicationRecognitionAdmin(admin.ModelAdmin):
    """
    Admin configuration for MedicationRecognition model.
    
    Provides interface for managing medication recognition results in Django admin.
    """
    list_display = [
        'medication_name', 'dosage', 'frequency', 'confidence_score', 
        'is_verified', 'created_at'
    ]
    list_filter = [
        'is_verified', 'confidence_score', 'created_at'
    ]
    search_fields = [
        'medication_name', 'ocr_result__extracted_text'
    ]
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('OCR Result', {
            'fields': ('ocr_result',)
        }),
        ('Recognition Results', {
            'fields': ('medication_name', 'dosage', 'frequency', 'confidence_score')
        }),
        ('Verification', {
            'fields': ('is_verified',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(AIInsight)
class AIInsightAdmin(admin.ModelAdmin):
    """
    Admin configuration for AIInsight model.
    
    Provides interface for managing AI insights in Django admin.
    """
    list_display = [
        'title', 'insight_type', 'confidence_score', 'is_active', 'created_at'
    ]
    list_filter = [
        'insight_type', 'is_active', 'confidence_score', 'created_at'
    ]
    search_fields = [
        'title', 'description'
    ]
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'insight_type', 'description')
        }),
        ('Recommendations', {
            'fields': ('recommendations',)
        }),
        ('Status', {
            'fields': ('confidence_score', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )