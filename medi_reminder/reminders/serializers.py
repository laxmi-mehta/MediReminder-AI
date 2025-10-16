"""
Serializers for the reminders app.

This module contains DRF serializers for reminder-related data serialization
and validation. Handles reminder creation and management.
"""

from rest_framework import serializers
from .models import Reminder
from medications.serializers import MedicationSerializer


class ReminderSerializer(serializers.ModelSerializer):
    """
    Serializer for Reminder model.
    
    Handles serialization of reminder data for API responses.
    Includes nested medication details and automatically assigns the current user on creation.
    """
    user_username = serializers.CharField(source='user.username', read_only=True)
    medication_details = MedicationSerializer(source='medication', read_only=True)
    
    class Meta:
        model = Reminder
        fields = [
            'id', 'user', 'user_username', 'medication', 'medication_details',
            'scheduled_time', 'repeat', 'status', 'notified', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        """
        Create a new reminder instance and assign the current user.
        """
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
