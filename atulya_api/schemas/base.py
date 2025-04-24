"""
Base Pydantic schemas for API data validation and serialization.
"""
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field


class ResponseBase(BaseModel):
    """Base model for all API responses"""
    success: bool = Field(default=True, description="Whether the request was successful")
    message: Optional[str] = Field(default=None, description="Message describing the result")


class ErrorResponse(ResponseBase):
    """Error response model"""
    success: bool = Field(default=False, description="Request failed")
    error: str = Field(..., description="Error message")
    error_code: Optional[str] = Field(default=None, description="Error code")
    details: Optional[Dict[str, Any]] = Field(default=None, description="Additional error details")


class HandlerResponse(ResponseBase):
    """Response model for API handler results"""
    data: Optional[Any] = Field(default=None, description="Response data")
    
    
class HandlerRequest(BaseModel):
    """Request model for API handler inputs"""
    params: Dict[str, Any] = Field(default_factory=dict, description="Parameters for the handler")


class AvailableHandlersResponse(ResponseBase):
    """Response model for listing available API handlers"""
    handlers: List[str] = Field(default_factory=list, description="List of available API handler names")