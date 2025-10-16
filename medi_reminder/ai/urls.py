"""
URL configuration for the ai app.

This module defines URL patterns for AI-related views and ViewSets.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views, viewsets

# Create a router for ViewSets
router = DefaultRouter()
router.register(r'ocr-results', viewsets.OCRResultViewSet, basename='ocr-result')
router.register(r'medication-recognitions', viewsets.MedicationRecognitionViewSet, basename='medication-recognition')
router.register(r'ai-insights', viewsets.AIInsightViewSet, basename='ai-insight')

# URL patterns
urlpatterns = [
    # Include router URLs for ViewSet endpoints
    path('api/', include(router.urls)),
    
    # Additional URL patterns for function-based views
    path('upload/', views.ImageUploadView.as_view(), name='image_upload'),
    path('ocr/process/', views.OCRProcessView.as_view(), name='ocr_process'),
    path('recognize/', views.MedicationRecognitionView.as_view(), name='medication_recognition'),
    path('insights/', views.ai_insights, name='ai_insights'),
    path('ocr-result/<int:result_id>/', views.OCRResultView.as_view(), name='ocr_result'),
    path('recognition/<int:recognition_id>/', views.MedicationRecognitionDetailView.as_view(), name='recognition_detail'),
    path('history/', views.user_ai_history, name='user_ai_history'),
]
