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
from fastapi.openapi.utils import get_openapi

from .config.settings import settings, get_settings
from .api.handlers import router as handlers_router

# Create FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    description="Modern API system for atulya-zero using FastAPI + Django",
    version=settings.API_VERSION,
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

# Health check endpoint
@app.get("/health")
async def health_check():
    """Simple health check endpoint to verify API is running"""
    return {"status": "healthy", "version": settings.API_VERSION}

# Custom OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=settings.API_TITLE,
        version=settings.API_VERSION,
        description="Modern API system for atulya-zero",
        routes=app.routes,
    )
    
    # Custom schema modifications can go here
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host=settings.HOST, 
        port=settings.PORT, 
        reload=settings.DEBUG
    )