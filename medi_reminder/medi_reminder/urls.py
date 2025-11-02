"""medi_reminder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

# Import ViewSets
from medications.viewsets import MedicationViewSet, PrescriptionViewSet
from reminders.viewsets import ReminderViewSet
from users.viewsets import UserViewSet


# Create main API router
api_router = DefaultRouter()
api_router.register(r'medications', MedicationViewSet, basename='medication')
api_router.register(r'prescriptions', PrescriptionViewSet, basename='prescription')
api_router.register(r'reminders', ReminderViewSet, basename='reminder')
api_router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # Main API router
    path('api/', include(api_router.urls)),
    
    # App URLs
    path('api/auth/', include('users.urls')),
    path('api/', include('medications.urls')),
    path('api/', include('reminders.urls')),
    path('api/', include('ai.urls')),

    # Serve React app
    path('', TemplateView.as_view(template_name='index.html')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
