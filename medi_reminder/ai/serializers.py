"""
Serializers for the ai app.

This module contains DRF serializers for AI-related data serialization
and validation. Handles OCR processing, medication recognition, and AI insights.
"""

from rest_framework import serializers
from .models import OCRResult, MedicationRecognition, AIInsight


class OCRResultSerializer(serializers.ModelSerializer):
    """
    Serializer for OCRResult model.
    
    Handles serialization of OCR processing results.
    """
    class Meta:
        model = OCRResult
        fields = [
            'id', 'image', 'extracted_text', 'confidence_score',
            'processing_time', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class MedicationRecognitionSerializer(serializers.ModelSerializer):
    """
    Serializer for MedicationRecognition model.
    
    Handles serialization of AI medication recognition results.
    """
    ocr_result_text = serializers.CharField(source='ocr_result.extracted_text', read_only=True)
    
    class Meta:
        model = MedicationRecognition
        fields = [
            'id', 'ocr_result', 'ocr_result_text', 'medication_name',
            'dosage', 'frequency', 'confidence_score', 'is_verified',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AIInsightSerializer(serializers.ModelSerializer):
    """
    Serializer for AIInsight model.
    
    Handles serialization of AI-generated insights and recommendations.
    """
    class Meta:
        model = AIInsight
        fields = [
            'id', 'insight_type', 'title', 'description', 'recommendations',
            'confidence_score', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ImageUploadSerializer(serializers.Serializer):
    """
    Serializer for image upload and OCR processing.
    
    Handles image upload for medication recognition.
    """
    image = serializers.ImageField(help_text="Image file to process for medication recognition")
    process_ocr = serializers.BooleanField(default=True, help_text="Whether to perform OCR on the image")
    recognize_medication = serializers.BooleanField(default=True, help_text="Whether to recognize medication from OCR text")


class MedicationRecognitionCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating medication recognition results.
    
    Handles creation of medication recognition from OCR results.
    """
    class Meta:
        model = MedicationRecognition
        fields = [
            'ocr_result', 'medication_name', 'dosage', 'frequency',
            'confidence_score', 'is_verified'
        ]
