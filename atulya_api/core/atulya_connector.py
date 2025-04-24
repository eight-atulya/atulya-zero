"""
Core connector to interface with atulya-zero functionality.

This module provides a bridge between our new API system and the existing
atulya-zero core functionality. It ensures that we can leverage all of the
existing capabilities while providing them through our modern API architecture.
"""

import sys
import os
from pathlib import Path
import importlib
import inspect
import threading

# Ensure atulya-zero paths are accessible
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

# Import core atulya-zero functionality
try:
    import atulya
    from python.helpers.api import ApiHandler
except ImportError as e:
    raise ImportError(f"Failed to import atulya-zero core modules: {e}")

class AtulyaConnector:
    """
    Bridge class for accessing atulya-zero functionality from the new API system.
    This provides a clean interface to the existing capabilities without modifying the core.
    """
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        """Singleton pattern to ensure only one connector instance exists"""
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(AtulyaConnector, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance
    
    def __init__(self):
        """Initialize the connector if it hasn't been initialized already"""
        if self._initialized:
            return
            
        self.atulya_instance = None
        self.api_handlers = {}
        self._initialized = True
        
    def initialize_atulya(self, config=None):
        """Initialize the atulya-zero system"""
        if self.atulya_instance is None:
            # Initialize atulya-zero with optional custom configuration
            self.atulya_instance = atulya.Atulya(config)
        return self.atulya_instance
    
    def load_api_handlers(self):
        """Load all available API handlers from the original system"""
        api_dir = ROOT_DIR / 'python' / 'api'
        
        # Skip if directory doesn't exist
        if not api_dir.exists() or not api_dir.is_dir():
            print(f"Warning: API directory not found at {api_dir}")
            return {}
            
        # Find all python files that could be handlers
        handler_files = list(api_dir.glob('*.py'))
        
        for handler_file in handler_files:
            module_name = handler_file.stem
            # Skip __init__ and other special files
            if module_name.startswith('__'):
                continue
                
            try:
                # Import the module dynamically
                module_path = f"python.api.{module_name}"
                module = importlib.import_module(module_path)
                
                # Find all classes in the module that extend ApiHandler
                for name, obj in inspect.getmembers(module):
                    if (inspect.isclass(obj) and 
                        issubclass(obj, ApiHandler) and 
                        obj != ApiHandler):
                        
                        self.api_handlers[name] = obj
                        
            except Exception as e:
                print(f"Error loading API handler {module_name}: {e}")
                
        return self.api_handlers
    
    def execute_handler(self, handler_name, params=None):
        """
        Execute a specific API handler with the given parameters
        
        Args:
            handler_name (str): The name of the handler to execute
            params (dict): Parameters to pass to the handler
            
        Returns:
            dict: The result from the API handler
        """
        if not self.api_handlers:
            self.load_api_handlers()
            
        if handler_name not in self.api_handlers:
            raise ValueError(f"API handler '{handler_name}' not found")
            
        # Instantiate the handler
        handler_class = self.api_handlers[handler_name]
        handler = handler_class()
        
        # Execute the handler with parameters
        result = handler.handle(params or {})
        return result
    
    def get_available_handlers(self):
        """Get a list of all available API handlers"""
        if not self.api_handlers:
            self.load_api_handlers()
            
        return list(self.api_handlers.keys())