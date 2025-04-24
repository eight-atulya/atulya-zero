"""
Core Django models for atulya_api

These models store data related to API usage, configurations, and user interactions.
They provide persistence for the atulya-zero functionality exposed through our API.
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid
import json


class ApiRequest(models.Model):
    """
    Tracks API requests made to the system.
    Useful for analytics, debugging, and usage tracking.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Request details
    path = models.CharField(max_length=500)
    method = models.CharField(max_length=10)
    handler = models.CharField(max_length=255, null=True, blank=True)
    parameters = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    
    # Timestamps
    timestamp = models.DateTimeField(auto_now_add=True)
    response_time_ms = models.IntegerField(null=True, blank=True)
    
    # Response details
    status_code = models.IntegerField(null=True, blank=True)
    response_size = models.IntegerField(null=True, blank=True)
    success = models.BooleanField(default=True)
    error_message = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.method} {self.path} ({self.timestamp})"
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['timestamp']),
            models.Index(fields=['path']),
            models.Index(fields=['user']),
        ]


class ApiKey(models.Model):
    """
    API keys for authenticating external clients.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    key = models.CharField(max_length=64, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='api_keys')
    is_active = models.BooleanField(default=True)
    
    # Key restrictions
    allowed_handlers = models.JSONField(null=True, blank=True, 
                                       help_text="List of handlers this key can access")
    rate_limit = models.IntegerField(default=100, 
                                   help_text="Maximum requests per minute")
    expires_at = models.DateTimeField(null=True, blank=True)
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    last_used_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    def is_valid(self):
        """Check if the API key is valid and not expired"""
        if not self.is_active:
            return False
        
        if self.expires_at and timezone.now() > self.expires_at:
            return False
            
        return True
    
    def update_last_used(self):
        """Update the last used timestamp"""
        self.last_used_at = timezone.now()
        self.save(update_fields=['last_used_at'])

    class Meta:
        verbose_name = "API Key"
        verbose_name_plural = "API Keys"


class UserProfile(models.Model):
    """
    Extended profile information for users.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # User preferences and settings
    preferences = models.JSONField(default=dict, blank=True)
    
    # Usage statistics
    request_count = models.IntegerField(default=0)
    last_active = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Profile for {self.user.username}"
    
    def increment_request_count(self):
        """Increment the request counter and update last active timestamp"""
        self.request_count += 1
        self.last_active = timezone.now()
        self.save(update_fields=['request_count', 'last_active'])
    
    def update_preference(self, key, value):
        """Update a specific user preference"""
        preferences = self.preferences or {}
        preferences[key] = value
        self.preferences = preferences
        self.save(update_fields=['preferences'])
    
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"