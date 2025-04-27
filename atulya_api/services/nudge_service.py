"""
Service module for nudging (resetting) Atulya context.
"""
from atulya import AtulyaContext

class NudgeService:
    @staticmethod
    async def nudge(ctxid: str):
        context = AtulyaContext.get(ctxid) if ctxid else AtulyaContext.first() or AtulyaContext()
        context.nudge()
        msg = "Process reset, atulya nudged."
        context.log.log(type="info", content=msg)
        return {"message": msg, "ctxid": context.id}
