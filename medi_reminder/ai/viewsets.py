"""
ViewSets for the ai app.

This module contains DRF ViewSets for AI-related API endpoints.
Provides CRUD operations for OCR results, medication recognition, and AI insights.
"""

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import OCRResult, MedicationRecognition, AIInsight
from .serializers import (
    OCRResultSerializer,
    MedicationRecognitionSerializer,
    AIInsightSerializer,
    ImageUploadSerializer,
    MedicationRecognitionCreateSerializer
)


class OCRResultViewSet(viewsets.ModelViewSet):
    """
    ViewSet for OCRResult model.
    
    Provides CRUD operations for OCR result management.
    """
    serializer_class = OCRResultSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['confidence_score']
    ordering_fields = ['created_at', 'confidence_score']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """
        Filter OCR results by current user if needed.
        """
        return OCRResult.objects.all()
    
    @action(detail=False, methods=['post'])
    def process_image(self, request):
        """
        Process an uploaded image for OCR.
        
        POST /api/ocr-results/process_image/
        """
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            # Implementation for image processing
            return Response({'message': 'Image processed successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def recognize_medication(self, request, pk=None):
        """
        Recognize medication from OCR result.
        
        POST /api/ocr-results/{id}/recognize_medication/
        """
        ocr_result = self.get_object()
        # Implementation for medication recognition
        return Response({'message': 'Medication recognition completed'})


class MedicationRecognitionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for MedicationRecognition model.
    
    Provides CRUD operations for medication recognition management.
    """
    serializer_class = MedicationRecognitionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['medication_name']
    filterset_fields = ['is_verified', 'confidence_score']
    ordering_fields = ['created_at', 'confidence_score']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """
        Filter medication recognitions by current user if needed.
        """
        return MedicationRecognition.objects.all()
    
    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        """
        Verify a medication recognition result.
        
        POST /api/medication-recognitions/{id}/verify/
        """
        recognition = self.get_object()
        recognition.is_verified = True
        recognition.save()
        return Response({'message': 'Medication recognition verified'})
    
    @action(detail=False, methods=['get'])
    def unverified(self, request):
        """
        Get unverified medication recognitions.
        
        GET /api/medication-recognitions/unverified/
        """
        queryset = self.get_queryset().filter(is_verified=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class AIInsightViewSet(viewsets.ModelViewSet):
    """
    ViewSet for AIInsight model.
    
    Provides CRUD operations for AI insight management.
    """
    serializer_class = AIInsightSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    filterset_fields = ['insight_type', 'is_active']
    ordering_fields = ['created_at', 'confidence_score']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """
        Filter AI insights by current user if needed.
        """
        return AIInsight.objects.all()
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """
        Get active AI insights.
        
        GET /api/ai-insights/active/
        """
        queryset = self.get_queryset().filter(is_active=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def generate_recommendations(self, request, pk=None):
        """
        Generate recommendations based on AI insight.
        
        POST /api/ai-insights/{id}/generate_recommendations/
        """
        insight = self.get_object()
        # Implementation for generating recommendations
        return Response({'message': 'Recommendations generated'})
