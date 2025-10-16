"""
Views for the users app.

This module contains Django views for user-related functionality
including registration, login, profile management, etc.
"""

from django.shortcuts import render
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json


@method_decorator(csrf_exempt, name='dispatch')
class UserRegistrationView(View):
    """
    View for user registration.
    
    Handles POST requests to create new user accounts.
    """
    def post(self, request):
        # Implementation for user registration
        pass


@method_decorator(csrf_exempt, name='dispatch')
class UserLoginView(View):
    """
    View for user login.
    
    Handles POST requests to authenticate users.
    """
    def post(self, request):
        # Implementation for user login
        pass


@login_required
def user_profile(request):
    """
    View for user profile.
    
    Returns user profile information for authenticated users.
    """
    user = request.user
    return JsonResponse({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'date_joined': user.date_joined.isoformat()
    })


@login_required
def user_logout(request):
    """
    View for user logout.
    
    Logs out the current user.
    """
    logout(request)
    return JsonResponse({'message': 'Successfully logged out'})