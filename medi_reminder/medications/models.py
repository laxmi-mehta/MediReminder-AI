"""
Models for the medications app.

This module contains Django models for medication-related data.
Defines the structure for medications and prescriptions.
"""

from django.db import models
from django.conf import settings


class Medication(models.Model):
    """
    Model representing a user's medication.
    
    Stores information about medications including name, dosage,
    frequency, and treatment period.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    instructions = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Medication'
        verbose_name_plural = 'Medications'
    
    def __str__(self):
        return f"{self.name} - {self.dosage} ({self.frequency})"


class Prescription(models.Model):
    """
    Model representing a prescription image.
    
    Stores prescription images and their OCR extracted text
    for medication recognition and processing.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='prescriptions/')
    extracted_text = models.TextField(blank=True)
    processed = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Prescription'
        verbose_name_plural = 'Prescriptions'
    
    def __str__(self):
        return f"Prescription - {self.user.username} ({self.uploaded_at.strftime('%Y-%m-%d')})"