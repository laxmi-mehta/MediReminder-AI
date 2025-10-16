"""
URL configuration for the users app.

This module defines URL patterns for user-related views and ViewSets.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views, viewsets

# Create a router for ViewSets
router = DefaultRouter()
router.register(r'users', viewsets.UserViewSet, basename='user')

# URL patterns
urlpatterns = [
    # Include router URLs for ViewSet endpoints
    path('api/', include(router.urls)),
    
    # Additional URL patterns for function-based views
    path('profile/', views.user_profile, name='user_profile'),
    path('logout/', views.user_logout, name='user_logout'),
]
