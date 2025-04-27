"""
Main FastAPI application entry point for atulya_api
"""
import sys
import os
from pathlib import Path

# Add parent directory to path to access atulya-zero modules
sys.path.append(str(Path(__file__).parent.parent))

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi
from fastapi.responses import FileResponse, HTMLResponse

from .config.settings import settings, get_settings
from .api.handlers import router as handlers_router
from .api.docs import router as docs_router, tags_metadata, api_metadata

# Create FastAPI app with custom documentation
app = FastAPI(
    title=api_metadata["title"],
    description=api_metadata["description"],
    version=api_metadata["version"],
    openapi_tags=tags_metadata,
    contact=api_metadata["contact"],
    license_info=api_metadata["license_info"],
    # Disable default docs routes - we'll use our custom ones
    docs_url=None,
    redoc_url=None,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(handlers_router, prefix=settings.API_PREFIX)
app.include_router(docs_router)  # Include the docs router for custom documentation

# Health check endpoint
@app.get("/health", tags=["health"])
async def health_check():
    """Simple health check endpoint to verify API is running"""
    return {"status": "healthy", "version": settings.API_VERSION}

# Root endpoint to serve documentation landing page
@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def root():
    """Serve the API documentation landing page"""
    static_dir = Path(__file__).parent / "static"
    index_path = static_dir / "index.html"
    
    if index_path.exists():
        with open(index_path, "r") as f:
            return HTMLResponse(content=f.read())
    else:
        # Fallback if index.html doesn't exist
        return HTMLResponse("<html><body><h1>atulya-zero API</h1><p>API is running. Visit <a href='/docs'>docs</a> for documentation.</p></body></html>")

# Favicon endpoint
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    """Serve the favicon"""
    static_dir = Path(__file__).parent / "static"
    favicon_path = static_dir / "favicon.ico"
    
    if favicon_path.exists():
        return FileResponse(favicon_path)
    # Return empty response if favicon doesn't exist
    return ""

# Custom OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=api_metadata["title"],
        version=api_metadata["version"],
        description=api_metadata["description"],
        routes=app.routes,
        tags=tags_metadata,
        contact=api_metadata["contact"],
        license_info=api_metadata["license_info"],
    )
    
    # Add security schemes to OpenAPI schema
    openapi_schema["components"] = openapi_schema.get("components", {})
    openapi_schema["components"]["securitySchemes"] = {
        "ApiKeyHeader": {
            "type": "apiKey",
            "in": "header",
            "name": "X-API-Key"
        },
        "ApiKeyQuery": {
            "type": "apiKey",
            "in": "query",
            "name": "api_key"
        }
    }
    
    # Apply security globally to all operations
    openapi_schema["security"] = [
        {"ApiKeyHeader": []},
        {"ApiKeyQuery": []}
    ]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Try to serve static files if the directory exists
static_dir = Path(__file__).parent / "static"
if static_dir.exists() and static_dir.is_dir():
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host=settings.HOST, 
        port=settings.PORT, 
        reload=settings.DEBUG
    )