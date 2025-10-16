"""
Serializers for the medications app.

This module contains DRF serializers for medication-related data serialization
and validation. Handles medication information and prescription data.
"""

from rest_framework import serializers
from .models import Medication, Prescription


class MedicationSerializer(serializers.ModelSerializer):
    """
    Serializer for Medication model.
    
    Handles serialization of medication data for API responses.
    Automatically assigns the current user on creation.
    """
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Medication
        fields = [
            'id', 'user', 'user_username', 'name', 'dosage', 'frequency',
            'start_date', 'end_date', 'instructions', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        """
        Create a new medication instance and assign the current user.
        """
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class PrescriptionSerializer(serializers.ModelSerializer):
    """
    Serializer for Prescription model.
    
    Handles serialization of prescription data for API responses.
    Automatically assigns the current user on creation.
    """
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Prescription
        fields = [
            'id', 'user', 'user_username', 'image', 'extracted_text',
            'processed', 'uploaded_at'
        ]
        read_only_fields = ['id', 'user', 'uploaded_at']
    
    def create(self, validated_data):
        """
        Create a new prescription instance and assign the current user.
        """
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
