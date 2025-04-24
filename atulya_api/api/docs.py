"""
API documentation module using Swagger UI

This module provides API documentation using OpenAPI specification and Swagger UI.
It includes route definitions, request/response schemas, and authentication details.
"""
from fastapi import APIRouter, Depends
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["documentation"])

@router.get("/docs", response_class=HTMLResponse, include_in_schema=False)
async def get_swagger_documentation():
    """
    Get custom Swagger UI HTML with proper branding for atulya_api
    """
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="atulya-zero API Documentation",
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
        swagger_favicon_url="/favicon.ico",
        oauth2_redirect_url="/docs/oauth2-redirect",
    )

@router.get("/redoc", response_class=HTMLResponse, include_in_schema=False)
async def get_redoc_documentation():
    """
    Get ReDoc HTML documentation
    """
    return get_redoc_html(
        openapi_url="/openapi.json",
        title="atulya-zero API Documentation",
        redoc_js_url="https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js",
        redoc_favicon_url="/favicon.ico",
    )

# Custom OpenAPI Tags metadata
tags_metadata = [
    {
        "name": "handlers",
        "description": "Operations with atulya-zero API handlers. These endpoints provide access to the core functionality.",
    },
    {
        "name": "health",
        "description": "Health check endpoints to verify API is working properly.",
    },
    {
        "name": "user",
        "description": "User management operations (when implemented).",
    },
    {
        "name": "authentication",
        "description": "Authentication operations for API access.",
    },
]

# Custom OpenAPI metadata
api_metadata = {
    "title": "atulya-zero API",
    "description": """
    # atulya-zero API Documentation
    
    This API provides access to all atulya-zero functionality through a modern, RESTful interface.
    
    ## Authentication
    
    The API uses API Key authentication. You can provide your API key in one of two ways:
    - As a header: `X-API-Key: your-api-key`
    - As a query parameter: `?api_key=your-api-key`
    
    ## Base URL
    
    When running locally, the base URL is: `http://localhost:8000`
    
    ## Error Handling
    
    Errors are returned with appropriate HTTP status codes and include a consistent response body:
    ```json
    {
        "success": false,
        "error": "Error message description",
        "error_code": "ERROR_CODE"
    }
    ```
    
    ## API Structure
    
    The API is organized around handlers that provide specific functionality:
    - `GET /api/v1/handlers/` - List all available handlers
    - `POST /api/v1/handlers/{handler_name}` - Execute a specific handler
    """,
    "version": "0.1.0",
    "contact": {
        "name": "atulya-zero Support",
        "url": "https://github.com/your-username/atulya-zero",
        "email": "support@example.com",
    },
    "license_info": {
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
}