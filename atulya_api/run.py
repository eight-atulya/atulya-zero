#!/usr/bin/env python
"""
Run script for the atulya_api system.

This script serves as the main entry point for running the hybrid Django + FastAPI
application. It initializes both the Django component and the FastAPI server.
"""
import os
import sys
from pathlib import Path

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'atulya_api.django_settings')
# Add project directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

import django
from django.core.management import call_command

# Initialize Django
django.setup()

# Import FastAPI app after Django setup to avoid import errors
from atulya_api.main import app
import uvicorn
from atulya_api.config.settings import settings

def run_django_migrations():
    """Run Django migrations to set up the database"""
    print("Running Django migrations...")
    call_command('migrate')

def create_superuser():
    """Create a Django superuser if none exists"""
    from django.contrib.auth.models import User
    if not User.objects.filter(is_superuser=True).exists():
        username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin')
        email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
        password = os.getenv('DJANGO_SUPERUSER_PASSWORD')
        
        if password:
            print(f"Creating superuser {username}...")
            User.objects.create_superuser(username, email, password)
        else:
            print("DJANGO_SUPERUSER_PASSWORD not set. Skipping superuser creation.")

def run_server():
    """Run the FastAPI server"""
    print(f"Starting atulya_api server on {settings.HOST}:{settings.PORT}...")
    uvicorn.run(
        "atulya_api.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )

def initialize():
    """Initialize the application"""
    # Run Django database migrations
    run_django_migrations()
    
    # Create superuser if needed
    create_superuser()
    
    # Additional initialization steps can be added here
    print("atulya_api initialized successfully.")

if __name__ == "__main__":
    # Process command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "migrate":
            run_django_migrations()
        elif sys.argv[1] == "createsuperuser":
            create_superuser()
        elif sys.argv[1] == "init":
            initialize()
        else:
            print(f"Unknown command: {sys.argv[1]}")
            print("Available commands: migrate, createsuperuser, init")
    else:
        # Default action: initialize and run the server
        initialize()
        run_server()