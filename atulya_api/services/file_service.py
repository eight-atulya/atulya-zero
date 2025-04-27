"""
Service module for file operations (upload, download, delete, info, list).
"""
from typing import List, Optional
import os
from fastapi import UploadFile

class FileService:
    @staticmethod
    async def upload_files(files: List[UploadFile], upload_dir: str = "tmp/upload") -> List[str]:
        os.makedirs(upload_dir, exist_ok=True)
        saved_filenames = []
        for file in files:
            filename = file.filename
            if not filename:
                continue
            save_path = os.path.join(upload_dir, filename)
            with open(save_path, "wb") as f:
                f.write(await file.read())
            saved_filenames.append(filename)
        return saved_filenames

    @staticmethod
    async def get_file_info(path: str) -> dict:
        abs_path = os.path.abspath(path)
        exists = os.path.exists(abs_path)
        return {
            "input_path": path,
            "abs_path": abs_path,
            "exists": exists,
            "is_dir": os.path.isdir(abs_path) if exists else False,
            "is_file": os.path.isfile(abs_path) if exists else False,
            "size": os.path.getsize(abs_path) if exists else 0,
            "modified": os.path.getmtime(abs_path) if exists else 0,
            "created": os.path.getctime(abs_path) if exists else 0,
            "file_name": os.path.basename(abs_path),
        }

    @staticmethod
    async def delete_file(path: str) -> bool:
        abs_path = os.path.abspath(path)
        if os.path.exists(abs_path):
            os.remove(abs_path)
            return True
        return False

    @staticmethod
    async def list_files(directory: str) -> list:
        abs_dir = os.path.abspath(directory)
        if not os.path.isdir(abs_dir):
            return []
        return os.listdir(abs_dir)

    # Additional methods for delete, list, download, etc. can be added as needed.
