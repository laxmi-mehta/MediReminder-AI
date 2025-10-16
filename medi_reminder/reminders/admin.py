"""
Admin configuration for the reminders app.

This module configures the Django admin interface for reminder-related models.
"""

from django.contrib import admin
from .models import Reminder


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    """
    Admin configuration for Reminder model.
    
    Provides interface for managing reminders in Django admin.
    """
    list_display = [
        'user', 'medication', 'scheduled_time', 'repeat', 'status', 'notified', 'created_at'
    ]
    list_filter = [
        'status', 'repeat', 'notified', 'scheduled_time', 'created_at'
    ]
    search_fields = [
        'user__username', 'medication__name', 'status', 'repeat'
    ]
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'medication', 'scheduled_time')
        }),
        ('Schedule', {
            'fields': ('repeat',)
        }),
        ('Status', {
            'fields': ('status', 'notified')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )