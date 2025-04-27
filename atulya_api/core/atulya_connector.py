"""
Connector module for atulya-zero integration

This module provides a bridge between the atulya_api system and the core
atulya-zero functionality. It dynamically loads API handlers and allows
executing them through the FastAPI interface.
"""
import sys
import os
import importlib
import inspect
import threading
from pathlib import Path
from typing import Dict, Any, List, Callable, Optional

# Ensure atulya-zero root is in the Python path
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

# Import core atulya-zero functionality
try:
    # Import core modules
    import python.helpers.api as api_helper
    from python.helpers.api import ApiHandler
except ImportError as e:
    print(f"Error importing atulya-zero modules: {e}")
    print("Make sure atulya-zero is correctly installed and accessible")
    raise


class AtulyaConnector:
    """
    Connector class for atulya-zero functionality
    
    This class provides an interface to load and execute API handlers
    from the atulya-zero system.
    """
    
    def __init__(self):
        """Initialize the connector"""
        self.handlers = {}
        self.handlers_lock = threading.RLock()
        self.api_base_dir = ROOT_DIR / "python" / "api"
    
    def load_api_handlers(self) -> Dict[str, ApiHandler]:
        """
        Load all available API handlers from atulya-zero
        
        Returns:
            Dict[str, ApiHandler]: Dictionary of loaded handlers
        """
        with self.handlers_lock:
            if self.handlers:
                # Handlers already loaded
                return self.handlers
            
            # Find and load all handler modules
            for handler_file in self.api_base_dir.glob("**/*.py"):
                if handler_file.name.startswith("_"):
                    continue
                
                try:
                    # Convert path to module name
                    rel_path = handler_file.relative_to(ROOT_DIR)
                    module_path = ".".join(rel_path.with_suffix("").parts)
                    
                    # Import the module
                    module = importlib.import_module(module_path)
                    
                    # Find all ApiHandler subclasses in the module
                    for name, obj in inspect.getmembers(module):
                        if (inspect.isclass(obj) and 
                            issubclass(obj, ApiHandler) and 
                            obj is not ApiHandler):
                            
                            # Create an instance of the handler
                            handler_instance = obj()
                            handler_name = handler_instance.__class__.__name__
                            self.handlers[handler_name] = handler_instance
                            
                except Exception as e:
                    print(f"Error loading handler from {handler_file}: {e}")
            
            print(f"Loaded {len(self.handlers)} API handlers from atulya-zero")
            return self.handlers
    
    def get_available_handlers(self) -> List[str]:
        """
        Get a list of all available handler names
        
        Returns:
            List[str]: List of handler names
        """
        self.load_api_handlers()
        return list(self.handlers.keys())
    
    def get_handler(self, handler_name: str) -> Optional[ApiHandler]:
        """
        Get a specific handler by name
        
        Args:
            handler_name: Name of the handler to get
            
        Returns:
            ApiHandler: Handler instance or None if not found
        """
        self.load_api_handlers()
        return self.handlers.get(handler_name)
    
    def execute_handler(self, handler_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a handler with the given parameters
        
        Args:
            handler_name: Name of the handler to execute
            params: Parameters to pass to the handler
            
        Returns:
            Dict[str, Any]: Result from the handler
            
        Raises:
            ValueError: If the handler is not found
            Exception: If the handler execution fails
        """
        handler = self.get_handler(handler_name)
        if not handler:
            raise ValueError(f"Handler '{handler_name}' not found")
        
        try:
            # Execute the handler
            result = handler.handle(params)
            return result
        except Exception as e:
            print(f"Error executing handler {handler_name}: {e}")
            # Raise a more informative exception with context
            raise type(e)(f"Handler '{handler_name}' execution failed: {str(e)}") from e