"""
API Key Management Utility

This script provides command-line tools for creating and managing API keys
for the atulya_api system.
"""
import os
import sys
import argparse
import secrets
import hashlib
from pathlib import Path
from datetime import datetime, timedelta

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'atulya_api.django_settings')
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import django
django.setup()

from django.contrib.auth.models import User
from django.utils import timezone

from atulya_api.models.models import ApiKey

def generate_api_key():
    """Generate a secure random API key"""
    # Generate 32 random bytes and convert to hex string
    return secrets.token_hex(32)

def create_api_key(username, name=None, expires_days=None, allowed_handlers=None):
    """
    Create a new API key for the specified user
    
    Args:
        username: Username of the user to associate with the key
        name: Name/description for the API key
        expires_days: Number of days until the key expires (None for no expiration)
        allowed_handlers: List of handler names the key can access (None for all)
        
    Returns:
        tuple: (ApiKey object, key string)
    """
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        print(f"Error: User '{username}' does not exist")
        return None, None
        
    # Generate a secure API key
    key_string = generate_api_key()
    
    # Set default name if not provided
    if not name:
        name = f"API Key for {username} ({datetime.now().strftime('%Y-%m-%d')})"
    
    # Calculate expiration date if provided
    expires_at = None
    if expires_days is not None:
        expires_at = timezone.now() + timedelta(days=expires_days)
    
    # Create the API key object
    api_key = ApiKey(
        name=name,
        key=key_string,
        user=user,
        allowed_handlers=allowed_handlers,
        expires_at=expires_at
    )
    api_key.save()
    
    return api_key, key_string

def list_api_keys(username=None):
    """
    List API keys, optionally filtered by username
    
    Args:
        username: Optional username to filter by
        
    Returns:
        queryset: ApiKey queryset
    """
    keys_query = ApiKey.objects.all()
    
    if username:
        try:
            user = User.objects.get(username=username)
            keys_query = keys_query.filter(user=user)
        except User.DoesNotExist:
            print(f"Error: User '{username}' does not exist")
            return None
    
    return keys_query

def revoke_api_key(key_id):
    """
    Revoke an API key by ID
    
    Args:
        key_id: UUID of the API key to revoke
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        api_key = ApiKey.objects.get(id=key_id)
        api_key.is_active = False
        api_key.save()
        return True
    except ApiKey.DoesNotExist:
        print(f"Error: API key with ID '{key_id}' does not exist")
        return False

def main():
    """Command-line interface for API key management"""
    parser = argparse.ArgumentParser(description="API Key Manager for atulya_api")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Create API key command
    create_parser = subparsers.add_parser("create", help="Create a new API key")
    create_parser.add_argument("username", help="Username to associate with the key")
    create_parser.add_argument("--name", "-n", help="Name/description for the API key")
    create_parser.add_argument(
        "--expires", "-e", type=int, 
        help="Number of days until the key expires"
    )
    create_parser.add_argument(
        "--handlers", "-h", nargs="+",
        help="List of handler names the key can access (space-separated)"
    )
    
    # List API keys command
    list_parser = subparsers.add_parser("list", help="List API keys")
    list_parser.add_argument(
        "--username", "-u",
        help="Filter keys by username"
    )
    
    # Revoke API key command
    revoke_parser = subparsers.add_parser("revoke", help="Revoke an API key")
    revoke_parser.add_argument("key_id", help="ID of the API key to revoke")
    
    args = parser.parse_args()
    
    # Execute the requested command
    if args.command == "create":
        api_key, key_string = create_api_key(
            args.username,
            name=args.name,
            expires_days=args.expires,
            allowed_handlers=args.handlers
        )
        
        if api_key:
            print(f"\nAPI Key created successfully:")
            print(f"ID: {api_key.id}")
            print(f"Name: {api_key.name}")
            print(f"Key: {key_string}")
            print(f"User: {api_key.user.username}")
            print(f"Expires: {api_key.expires_at or 'Never'}")
            print("\nIMPORTANT: Store this key securely. It won't be shown again.")
            
    elif args.command == "list":
        keys = list_api_keys(args.username)
        
        if keys:
            print(f"\nAPI Keys{f' for {args.username}' if args.username else ''}:")
            print(f"{'ID':<36} {'Name':<30} {'User':<15} {'Active':<6} {'Expires'}")
            print("-" * 100)
            
            for key in keys:
                expires = key.expires_at.strftime("%Y-%m-%d") if key.expires_at else "Never"
                print(f"{str(key.id):<36} {key.name:<30} {key.user.username:<15} {str(key.is_active):<6} {expires}")
                
            print(f"\nTotal: {keys.count()} keys")
            
    elif args.command == "revoke":
        success = revoke_api_key(args.key_id)
        if success:
            print(f"API key '{args.key_id}' has been revoked")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()