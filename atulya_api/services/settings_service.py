"""
Service module for getting/setting Atulya settings.
"""
from python.helpers import settings

class SettingsService:
    @staticmethod
    async def get_settings():
        return {"settings": settings.convert_out(settings.get_settings())}

    @staticmethod
    async def set_settings(input_data: dict):
        set_data = settings.convert_in(input_data)
        set_data = settings.set_settings(set_data)
        return {"settings": set_data}
