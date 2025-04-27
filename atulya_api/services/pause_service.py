"""
Service module for pausing/unpausing Atulya context.
"""
from typing import Optional
from atulya import AtulyaContext

class PauseService:
    @staticmethod
    async def set_paused(paused: bool, ctxid: Optional[str] = None):
        context = AtulyaContext.get(ctxid) if ctxid else AtulyaContext.first() or AtulyaContext()
        context.paused = paused
        return {
            "message": "Atulya paused." if paused else "Atulya unpaused.",
            "pause": paused,
        }
