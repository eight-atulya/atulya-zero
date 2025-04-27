"""
Service module for process restart.
"""
from python.helpers import process

class RestartService:
    @staticmethod
    async def restart():
        process.reload()
        return {"message": "Process restarted."}
