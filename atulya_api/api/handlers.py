"""
FastAPI router for accessing atulya-zero's API handlers.

This module provides REST endpoints that map to the original atulya-zero handlers.
"""
from fastapi import APIRouter, HTTPException, Depends, Request, Response
from fastapi.responses import JSONResponse
from typing import Dict, Any, List, Optional
import time

from django.contrib.auth.models import User

from ..core.atulya_connector import AtulyaConnector
from ..schemas.base import HandlerRequest, HandlerResponse, AvailableHandlersResponse, ErrorResponse
from ..utils.auth import validate_api_key, log_api_request, check_handler_permission
from ..models.models import ApiKey

router = APIRouter(
    prefix="/handlers",
    tags=["handlers"],
    responses={
        404: {"model": ErrorResponse, "description": "Handler not found"},
        401: {"model": ErrorResponse, "description": "Authentication failed"},
        403: {"model": ErrorResponse, "description": "Permission denied"}
    },
)

def get_connector():
    """Dependency to get the AtulyaConnector instance"""
    connector = AtulyaConnector()
    connector.load_api_handlers()  # Ensure handlers are loaded
    return connector


@router.get("/", response_model=AvailableHandlersResponse)
async def list_handlers(
    request: Request,
    connector: AtulyaConnector = Depends(get_connector),
    api_key_data: tuple[ApiKey, User] = Depends(validate_api_key)
):
    """List all available API handlers"""
    # Start timing the request for logging
    request.state.request_time = time.time()
    api_key, user = api_key_data
    
    try:
        handlers = connector.get_available_handlers()
        
        # Create the response
        response = AvailableHandlersResponse(
            success=True,
            message="Available handlers retrieved successfully",
            handlers=handlers
        )
        
        # Log the request
        await log_api_request(
            request=request,
            response=response.dict(),
            user=user,
            handler="list_handlers"
        )
        
        return response
        
    except Exception as e:
        error_msg = f"Error retrieving handlers: {str(e)}"
        
        # Log the error
        await log_api_request(
            request=request,
            response={},
            user=user,
            handler="list_handlers",
            error=error_msg
        )
        
        raise HTTPException(status_code=500, detail=error_msg)


@router.post("/{handler_name}", response_model=HandlerResponse)
async def execute_handler(
    handler_name: str,
    request: Request,
    handler_request: HandlerRequest,
    connector: AtulyaConnector = Depends(get_connector),
    api_key_data: tuple[ApiKey, User] = Depends(validate_api_key)
):
    """Execute a specific API handler by name"""
    # Start timing the request for logging
    request.state.request_time = time.time()
    api_key, user = api_key_data
    
    try:
        # Check if the handler exists
        available_handlers = connector.get_available_handlers()
        if handler_name not in available_handlers:
            error_msg = f"Handler '{handler_name}' not found. Available handlers: {available_handlers}"
            
            # Log the error
            await log_api_request(
                request=request,
                response={},
                user=user,
                handler=handler_name,
                error=error_msg
            )
            
            raise HTTPException(status_code=404, detail=error_msg)
        
        # Check if the API key has permission to use this handler
        if not check_handler_permission(api_key, handler_name):
            error_msg = f"Permission denied: API key does not have access to handler '{handler_name}'"
            
            # Log the error
            await log_api_request(
                request=request,
                response={},
                user=user,
                handler=handler_name,
                error=error_msg
            )
            
            raise HTTPException(status_code=403, detail=error_msg)
        
        # Execute the handler with the provided parameters
        result = connector.execute_handler(handler_name, handler_request.params)
        
        # Create the response
        response = HandlerResponse(
            success=True,
            message=f"Handler '{handler_name}' executed successfully",
            data=result
        )
        
        # Log the request
        await log_api_request(
            request=request,
            response=response.dict(),
            user=user,
            handler=handler_name
        )
        
        return response
        
    except HTTPException as e:
        # Re-raise HTTP exceptions
        raise e
        
    except ValueError as e:
        error_msg = str(e)
        
        # Log the error
        await log_api_request(
            request=request,
            response={},
            user=user,
            handler=handler_name,
            error=error_msg
        )
        
        raise HTTPException(status_code=404, detail=error_msg)
        
    except Exception as e:
        error_msg = f"Error executing handler: {str(e)}"
        
        # Log the error
        await log_api_request(
            request=request,
            response={},
            user=user,
            handler=handler_name,
            error=error_msg
        )
        
        # Log the exception for debugging
        print(f"Error executing handler {handler_name}: {e}")
        raise HTTPException(status_code=500, detail=error_msg)