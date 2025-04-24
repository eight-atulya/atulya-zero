"""
Admin configurations for atulya_api Django models
"""
from django.contrib import admin
from .models import ApiRequest, ApiKey, UserProfile


@admin.register(ApiRequest)
class ApiRequestAdmin(admin.ModelAdmin):
    """Admin interface for API request tracking"""
    list_display = ('method', 'path', 'handler', 'user', 'timestamp', 'status_code', 'response_time_ms', 'success')
    list_filter = ('method', 'success', 'handler')
    search_fields = ('path', 'handler', 'user__username')
    date_hierarchy = 'timestamp'
    readonly_fields = ('id', 'timestamp')


@admin.register(ApiKey)
class ApiKeyAdmin(admin.ModelAdmin):
    """Admin interface for API keys"""
    list_display = ('name', 'user', 'is_active', 'created_at', 'last_used_at', 'expires_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'user__username')
    readonly_fields = ('id', 'created_at', 'last_used_at')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin interface for user profiles"""
    list_display = ('user', 'request_count', 'last_active')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('request_count', 'last_active')