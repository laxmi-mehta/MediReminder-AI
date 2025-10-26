"""
URL configuration for the medications app.

This module defines URL patterns for medication-related views and ViewSets.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views, viewsets

# Create a router for ViewSets
router = DefaultRouter()
router.register(r'medications', viewsets.MedicationViewSet, basename='medication')
router.register(r'prescriptions', viewsets.PrescriptionViewSet, basename='prescription')

# URL patterns
urlpatterns = [
    # Include router URLs for ViewSet endpoints
    path('api/', include(router.urls)),

    # OCR Upload endpoint
    path('ocr/upload/', views.OCRUploadView.as_view(), name='ocr-upload'),
    
    # Prescription management endpoints
    path('prescriptions/', views.PrescriptionListView.as_view(), name='prescription-list'),
    path('prescriptions/<int:prescription_id>/', views.PrescriptionDetailView.as_view(), name='prescription-detail'),
]
