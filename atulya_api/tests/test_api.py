"""
Tests for the atulya_api endpoints
"""
import os
import sys
import unittest
import pytest
from fastapi.testclient import TestClient

# Set up Django environment for tests
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'atulya_api.django_settings')
import django
django.setup()

from django.contrib.auth.models import User
from atulya_api.models.models import ApiKey
from atulya_api.main import app


class TestApiEndpoints:
    """Tests for API endpoints"""
    
    @classmethod
    def setup_class(cls):
        """Set up test client and test data"""
        cls.client = TestClient(app)
        
        # Create a test user and API key
        try:
            cls.user = User.objects.create_user(
                username="testuser",
                email="test@example.com",
                password="testpassword"
            )
            
            cls.api_key = ApiKey.objects.create(
                name="Test API Key",
                key="test-api-key-12345",
                user=cls.user,
                is_active=True
            )
        except Exception as e:
            print(f"Error setting up test data: {e}")
            # Continue even if setup fails (database may not be ready)
            pass
    
    @classmethod
    def teardown_class(cls):
        """Clean up test data"""
        try:
            if hasattr(cls, 'api_key'):
                cls.api_key.delete()
            if hasattr(cls, 'user'):
                cls.user.delete()
        except Exception as e:
            print(f"Error cleaning up test data: {e}")
    
    def test_health_endpoint(self):
        """Test the health check endpoint"""
        response = self.client.get("/health")
        assert response.status_code == 200
        assert response.json().get("status") == "healthy"
    
    def test_list_handlers_requires_auth(self):
        """Test that listing handlers requires authentication"""
        response = self.client.get("/api/v1/handlers/")
        assert response.status_code == 401
    
    def test_list_handlers_with_auth(self):
        """Test listing handlers with valid authentication"""
        # Skip if API key wasn't created
        if not hasattr(self, 'api_key'):
            pytest.skip("API key not available")
            
        response = self.client.get(
            "/api/v1/handlers/",
            headers={"X-API-Key": "test-api-key-12345"}
        )
        assert response.status_code == 200
        assert "handlers" in response.json()
        assert response.json()["success"] is True
    
    def test_execute_handler_requires_auth(self):
        """Test that executing a handler requires authentication"""
        response = self.client.post(
            "/api/v1/handlers/SomeHandler",
            json={"params": {}}
        )
        assert response.status_code == 401