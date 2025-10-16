"""
ViewSets for the reminders app.

This module contains DRF ViewSets for reminder-related API endpoints.
Provides CRUD operations for reminders.
"""

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from datetime import timedelta
from .models import Reminder
from .serializers import ReminderSerializer


class ReminderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Reminder model.
    
    Provides CRUD operations for reminder management.
    Filters by current user and supports marking reminders as done.
    """
    serializer_class = ReminderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['medication__name']
    filterset_fields = ['status', 'repeat', 'notified']
    ordering_fields = ['scheduled_time', 'created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """
        Filter reminders by current user.
        """
        return Reminder.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """
        Get upcoming reminders for the next 24 hours.
        
        GET /api/reminders/upcoming/
        """
        now = timezone.now()
        next_24h = now + timedelta(hours=24)
        
        upcoming_reminders = Reminder.objects.filter(
            user=request.user,
            status='pending',
            scheduled_time__gte=now,
            scheduled_time__lte=next_24h
        ).select_related('medication')
        
        serializer = self.get_serializer(upcoming_reminders, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def mark_done(self, request, pk=None):
        """
        Mark a reminder as done.
        
        POST /api/reminders/{id}/mark_done/
        """
        reminder = self.get_object()
        reminder.status = 'done'
        reminder.save()
        return Response({'message': 'Reminder marked as done'})
    
    @action(detail=True, methods=['post'])
    def mark_missed(self, request, pk=None):
        """
        Mark a reminder as missed.
        
        POST /api/reminders/{id}/mark_missed/
        """
        reminder = self.get_object()
        reminder.status = 'missed'
        reminder.save()
        return Response({'message': 'Reminder marked as missed'})
    
    @action(detail=False, methods=['get'])
    def pending(self, request):
        """
        Get all pending reminders for the current user.
        
        GET /api/reminders/pending/
        """
        pending_reminders = Reminder.objects.filter(
            user=request.user,
            status='pending'
        ).select_related('medication')
        
        serializer = self.get_serializer(pending_reminders, many=True)
        return Response(serializer.data)
