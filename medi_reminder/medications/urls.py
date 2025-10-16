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
    
    # Additional URL patterns for function-based views
    path('search/', views.MedicationSearchView.as_view(), name='medication_search'),
    path('medication/<int:medication_id>/', views.MedicationDetailView.as_view(), name='medication_detail'),
    path('user-medications/', views.user_medications, name='user_medications'),
    path('dosage/<int:dosage_id>/', views.DosageManagementView.as_view(), name='dosage_management'),
]
