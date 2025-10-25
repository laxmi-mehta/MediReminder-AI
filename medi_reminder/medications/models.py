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
    Model to store uploaded prescription images and basic prescription details.
    Each prescription is linked to a user and can have multiple medication items.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='prescriptions',
        help_text="User who uploaded this prescription"
    )
    doctor_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Name of the prescribing doctor"
    )
    image = models.ImageField(
        upload_to='prescriptions/',
        help_text="Uploaded prescription image"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when prescription was uploaded"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Prescription'
        verbose_name_plural = 'Prescriptions'

    def __str__(self):
        return f"Prescription #{self.id} - {self.user.username} - {self.created_at.strftime('%Y-%m-%d')}"


class PrescriptionItem(models.Model):
    """
    Model to store individual medication items extracted from a prescription.
    Each item represents one medication with its dosage and frequency details.
    """
    prescription = models.ForeignKey(
        Prescription,
        on_delete=models.CASCADE,
        related_name='items',
        help_text="Parent prescription this item belongs to"
    )
    medication_name = models.CharField(
        max_length=200,
        help_text="Name of the medication"
    )
    dosage = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Dosage information (e.g., '500mg', '2 tablets')"
    )
    frequency = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Frequency of medication (e.g., 'twice daily', 'after meals')"
    )

    class Meta:
        verbose_name = 'Prescription Item'
        verbose_name_plural = 'Prescription Items'

    def __str__(self):
        return f"{self.medication_name} - {self.dosage or 'No dosage'}"