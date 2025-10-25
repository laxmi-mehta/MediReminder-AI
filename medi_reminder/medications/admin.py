"""
Admin configuration for the medications app.

This module configures the Django admin interface for medication-related models.
"""

from django.contrib import admin
from .models import Medication, Prescription, PrescriptionItem


@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    """
    Admin configuration for Medication model.
    
    Provides interface for managing medications in Django admin.
    """
    list_display = [
        'name', 'user', 'dosage', 'frequency', 'start_date', 'end_date', 'created_at'
    ]
    list_filter = [
        'frequency', 'start_date', 'end_date', 'created_at'
    ]
    search_fields = [
        'name', 'user__username', 'dosage', 'frequency', 'instructions'
    ]
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'name', 'dosage', 'frequency')
        }),
        ('Schedule', {
            'fields': ('start_date', 'end_date')
        }),
        ('Instructions', {
            'fields': ('instructions',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    """
    Admin configuration for Prescription model.
    
    Provides interface for managing prescriptions in Django admin.
    """
    list_display = [
        'user', 'image', 'doctor_name', 'created_at'
    ]
    list_filter = [
        'doctor_name', 'created_at'
    ]
    search_fields = [
        'user__username', 'doctor_name'
    ]
    ordering = ['-created_at']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'image')
        }),
        ('Processing', {
            'fields': ('doctor_name',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(PrescriptionItem)
class PrescriptionItemAdmin(admin.ModelAdmin):
    """
    Admin configuration for PrescriptionItem model.
    
    Provides interface for managing prescription items in Django admin.
    """
    list_display = [
        'prescription', 'medication_name', 'dosage', 'frequency'
    ]
    list_filter = [
        'dosage', 'frequency'
    ]
    