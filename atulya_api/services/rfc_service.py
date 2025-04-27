"""
Service module for remote function calls.
"""
from python.helpers import runtime

class RFCService:
    @staticmethod
    async def handle_rfc(input_data: dict):
        return await runtime.handle_rfc(input_data)
