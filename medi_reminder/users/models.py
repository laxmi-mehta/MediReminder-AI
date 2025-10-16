"""
Models for the users app.

This module contains Django models for user-related data.
Defines a custom user model extending AbstractUser with additional fields.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    
    Adds additional fields like phone_number and age to the default user model.
    """
    phone_number = models.CharField(max_length=15, blank=True, help_text="User's phone number")
    age = models.PositiveIntegerField(null=True, blank=True, help_text="User's age")
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.username} ({self.email})"
