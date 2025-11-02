"""
Serializers for the medications app.

This module contains DRF serializers for medication-related data serialization
and validation. Handles medication information and prescription data.
"""

from rest_framework import serializers
from .models import Medication, Prescription, PrescriptionItem


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
            'id', 'user', 'name', 'dosage', 'frequency',
            'start_date', 'end_date', 'instructions', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        """
        Create a new medication instance and assign the current user.
        """
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class PrescriptionItemSerializer(serializers.ModelSerializer):
    """
    Serializer for individual prescription medication items.
    Used for nested representation within PrescriptionSerializer.
    """
    
    class Meta:
        model = PrescriptionItem
        fields = ['medication_name', 'dosage', 'frequency']

        
class PrescriptionSerializer(serializers.ModelSerializer):
    """
    Serializer for Prescription model with nested medication items.
    Includes read-only nested items and user information.
    """
    items = PrescriptionItemSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Prescription
        fields = ['id', 'user', 'doctor_name', 'image', 'created_at', 'items']
        read_only_fields = ['id', 'created_at', 'user']
    
    def to_representation(self, instance):
        """
        Customize the output representation.
        Adds full URL for the image field.
        """
        representation = super().to_representation(instance)
        request = self.context.get('request')
        
        if instance.image and request:
            representation['image'] = request.build_absolute_uri(instance.image.url)
        
        return representation

    # def create(self, validated_data):
    #     """
    #     Create a new prescription instance and assign the current user.
    #     """
    #     validated_data['user'] = self.context['request'].user
    #     return super().create(validated_data)

