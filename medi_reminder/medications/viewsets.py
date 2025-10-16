"""
ViewSets for the medications app.

This module contains DRF ViewSets for medication-related API endpoints.
Provides CRUD operations for medications and prescriptions.
"""

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models
from .models import Medication, Prescription
from .serializers import MedicationSerializer, PrescriptionSerializer


class MedicationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Medication model.
    
    Provides CRUD operations for medication management.
    Filters by current user and supports search by medication name.
    """
    serializer_class = MedicationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'dosage', 'frequency']
    filterset_fields = ['status', 'start_date', 'end_date']
    ordering_fields = ['name', 'start_date', 'created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """
        Filter medications by current user.
        """
        return Medication.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        Search medications by name.
        
        GET /api/medications/search/?name=aspirin
        """
        name = request.query_params.get('name', '')
        if name:
            queryset = self.get_queryset().filter(
                models.Q(name__icontains=name)
            )
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        return Response({'error': 'name parameter is required'}, status=status.HTTP_400_BAD_REQUEST)


class PrescriptionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Prescription model.
    
    Provides CRUD operations for prescription management.
    Filters by current user.
    """
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['processed']
    ordering_fields = ['uploaded_at']
    ordering = ['-uploaded_at']
    
    def get_queryset(self):
        """
        Filter prescriptions by current user.
        """
        return Prescription.objects.filter(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def process(self, request, pk=None):
        """
        Mark a prescription as processed.
        
        POST /api/prescriptions/{id}/process/
        """
        prescription = self.get_object()
        prescription.processed = True
        prescription.save()
        return Response({'message': 'Prescription marked as processed'})
