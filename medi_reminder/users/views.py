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


from django.contrib.auth import get_user_model, authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt

User = get_user_model()  # This will get your CustomUser model

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def register_user(request):
    print("12")
    """Register a new user"""
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    
    # Validation
    if not username or not email or not password:
        return Response(
            {'error': 'Please provide username, email and password'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Check if user already exists
    if User.objects.filter(username=username).exists():
        return Response(
            {'error': 'Username already exists'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if User.objects.filter(email=email).exists():
        return Response(
            {'error': 'Email already registered'},
            status=status.HTTP_400_BAD_REQUEST
        )
     # Create user
    try:
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        # Create token
        token, _ = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """Login user"""
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'Please provide username and password'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = authenticate(request, username=username, password=password)
    
    if user is None:
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    token, _ = Token.objects.get_or_create(user=user)
    
    return Response({
        'token': token.key,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
    })


@api_view(['GET'])
def get_user(request):
    """Get current user details"""
    return Response({
        'id': request.user.id,
        'username': request.user.username,
        'email': request.user.email
    })


@api_view(['POST'])
def logout_user(request):
    """Logout user"""
    try:
        request.user.auth_token.delete()
        return Response({'message': 'Logged out successfully'})
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )