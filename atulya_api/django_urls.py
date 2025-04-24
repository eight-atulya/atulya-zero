"""
Django URL configurations for atulya_api
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Add Django-specific URLs here
]