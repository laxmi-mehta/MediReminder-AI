"""
URL configuration for the reminders app.

This module defines URL patterns for reminder-related views and ViewSets.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views, viewsets

# Create a router for ViewSets
router = DefaultRouter()
router.register(r'reminders', viewsets.ReminderViewSet, basename='reminder')

# URL patterns
urlpatterns = [
    # Include router URLs for ViewSet endpoints
    path('api/', include(router.urls)),
    
    # Additional URL patterns for function-based views
    path('create/', views.ReminderCreateView.as_view(), name='reminder_create'),
    path('user-reminders/', views.user_reminders, name='user_reminders'),
    path('upcoming/', views.upcoming_reminders, name='upcoming_reminders'),
    path('reminder/<int:reminder_id>/', views.ReminderDetailView.as_view(), name='reminder_detail'),
    path('schedule/<int:schedule_id>/', views.ReminderScheduleView.as_view(), name='reminder_schedule'),
    path('notifications/', views.reminder_notifications, name='reminder_notifications'),
]
