"""
Configuration settings for atulya_api.

This module loads environment variables and provides configuration settings
for the API system.
"""
import os
from pathlib import Path
from typing import Dict, Any, Optional

# Root directory of the atulya_api package
ROOT_DIR = Path(__file__).parent.parent

# Base directory containing atulya-zero
BASE_DIR = ROOT_DIR.parent

# Default configuration values
default_config = {
    "API_TITLE": "atulya-zero API",
    "API_VERSION": "0.1.0",
    "API_PREFIX": "/api/v1",
    "DEBUG": True,
    "HOST": "0.0.0.0",
    "PORT": 8000,
    "LOG_LEVEL": "info",
    "CORS_ORIGINS": ["*"],
    "MAX_REQUEST_SIZE": 10 * 1024 * 1024,  # 10MB
    "RATE_LIMIT_PER_MINUTE": 100,
}

# Try to load settings from .env file
try:
    from dotenv import load_dotenv
    env_file = BASE_DIR / ".env"
    if env_file.exists():
        load_dotenv(env_file)
except ImportError:
    # python-dotenv is not installed, use default values
    pass

class Settings:
    """
    Application settings loaded from environment variables with defaults
    """
    def __init__(self):
        self.config = default_config.copy()
        
        # Override defaults with environment variables
        for key in self.config:
            env_value = os.getenv(key)
            if env_value is not None:
                # Convert boolean values
                if isinstance(self.config[key], bool):
                    self.config[key] = env_value.lower() in ("true", "1", "yes")
                # Convert integer values
                elif isinstance(self.config[key], int):
                    self.config[key] = int(env_value)
                # Use string values as is
                else:
                    self.config[key] = env_value
    
    def __getattr__(self, name: str) -> Any:
        """Access settings as attributes"""
        if name in self.config:
            return self.config[name]
        raise AttributeError(f"'Settings' object has no attribute '{name}'")
    
    def get(self, name: str, default: Any = None) -> Any:
        """Get a setting value with an optional default"""
        return self.config.get(name, default)
    
    def update(self, updates: Dict[str, Any]) -> None:
        """Update settings with provided values"""
        self.config.update(updates)

# Create a global settings instance
settings = Settings()

def get_settings() -> Settings:
    """
    Returns the settings instance.
    This function can be used as a FastAPI dependency.
    """
    return settings