"""
Service module for serving image files.
"""
import os
from fastapi.responses import FileResponse

class ImageService:
    @staticmethod
    async def get_image(path: str):
        if not path or not os.path.exists(path):
            raise FileNotFoundError("No path provided or file does not exist")
        return FileResponse(path)
