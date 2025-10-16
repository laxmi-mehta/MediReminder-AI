"""
Models for the reminders app.

This module contains Django models for reminder-related data.
Defines the structure for medication reminders.
"""

from django.db import models
from django.conf import settings


class Reminder(models.Model):
    """
    Model representing a medication reminder.
    
    Stores information about reminders including scheduled time,
    repeat frequency, status, and notification tracking.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    medication = models.ForeignKey('medications.Medication', on_delete=models.CASCADE)
    scheduled_time = models.DateTimeField()
    repeat = models.CharField(
        max_length=50, 
        choices=[('once', 'Once'), ('daily', 'Daily'), ('weekly', 'Weekly')], 
        default='once'
    )
    status = models.CharField(
        max_length=20, 
        choices=[('pending', 'Pending'), ('done', 'Done'), ('missed', 'Missed')], 
        default='pending'
    )
    notified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Reminder'
        verbose_name_plural = 'Reminders'
    
    def __str__(self):
        return f"{self.user.username} - {self.medication.name} ({self.scheduled_time.strftime('%Y-%m-%d %H:%M')})"