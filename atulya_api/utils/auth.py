"""
Authentication utilities for atulya_api

This module provides authentication and authorization functionality
for the API system, including API key validation and rate limiting.
"""
import os
from typing import Optional, Tuple, Dict, Any
import time
from datetime import datetime, timedelta

# Initialize Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'atulya_api.django_settings')
import django
django.setup()

from django.contrib.auth.models import User
from django.utils import timezone

from fastapi import Request, HTTPException, Depends, status
from fastapi.security import APIKeyHeader, APIKeyQuery

from ..models.models import ApiKey, ApiRequest, UserProfile

# API key can be specified in header or query parameter
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
api_key_query = APIKeyQuery(name="api_key", auto_error=False)

# Cache of API keys for better performance
# Structure: {key_string: (key_obj, last_validated_timestamp)}
api_key_cache = {}
CACHE_TTL_SECONDS = 60  # Cache API keys for 1 minute

def validate_api_key(
    api_key_header: Optional[str] = Depends(api_key_header),
    api_key_query: Optional[str] = Depends(api_key_query)
) -> Tuple[ApiKey, User]:
    """
    Validate the API key from header or query param and return the
    corresponding API key object and User if valid.
    """
    api_key = api_key_header or api_key_query
    
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is required",
            headers={"WWW-Authenticate": "ApiKey"},
        )
        
    # Check cache first for performance
    now = time.time()
    if api_key in api_key_cache:
        cached_key, cached_time = api_key_cache[api_key]
        # If key is in cache and cache hasn't expired
        if now - cached_time < CACHE_TTL_SECONDS:
            if cached_key.is_valid():
                cached_key.update_last_used()
                return cached_key, cached_key.user
    
    # Key not in cache or cache expired, check database
    try:
        key_obj = ApiKey.objects.select_related('user').get(key=api_key)
    except ApiKey.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "ApiKey"},
        )
        
    # Check if the key is valid and not expired
    if not key_obj.is_valid():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API key has expired or is inactive",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    
    # Update the last used timestamp
    key_obj.update_last_used()
    
    # Update cache
    api_key_cache[api_key] = (key_obj, now)
    
    return key_obj, key_obj.user

async def log_api_request(
    request: Request, 
    response: Dict[str, Any],
    user: Optional[User] = None,
    handler: Optional[str] = None,
    error: Optional[str] = None
) -> ApiRequest:
    """
    Log an API request and its response for monitoring and analytics
    """
    # Calculate response time
    request_time = getattr(request.state, "request_time", None)
    response_time_ms = None
    if request_time:
        response_time_ms = int((time.time() - request_time) * 1000)
    
    # Create API request log entry
    log_entry = ApiRequest(
        user=user,
        path=str(request.url.path),
        method=request.method,
        handler=handler,
        parameters={},  # Can extract from request if needed
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
        response_time_ms=response_time_ms,
        status_code=200,  # Default, will be updated if there's an error
        success=error is None,
        error_message=error
    )
    
    # Try to extract parameters from request
    try:
        body = await request.json()
        if isinstance(body, dict) and "params" in body:
            log_entry.parameters = body["params"]
    except:
        # Could not parse body as JSON, ignore
        pass
        
    # Save the log entry
    log_entry.save()
    
    # Update user profile stats if a user is associated
    if user:
        try:
            # Get or create user profile
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.increment_request_count()
        except Exception as e:
            # Log the error but don't fail the request
            print(f"Error updating user profile: {e}")
    
    return log_entry

def check_handler_permission(api_key: ApiKey, handler_name: str) -> bool:
    """
    Check if the API key has permission to access the specified handler.
    
    Returns True if allowed, False otherwise.
    """
    # If no allowed handlers are specified, all are allowed
    if not api_key.allowed_handlers:
        return True
        
    # Check if the handler is in the allowed list
    return handler_name in api_key.allowed_handlers