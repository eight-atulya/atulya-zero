"""
Service module for polling Atulya context/logs.
"""
from typing import Optional
from atulya import AtulyaContext

class PollService:
    @staticmethod
    async def poll_context(ctxid: Optional[str] = None, log_from: int = 0):
        context = AtulyaContext.get(ctxid) if ctxid else AtulyaContext.first() or AtulyaContext()
        logs = context.log.output(start=log_from)
        ctxs = []
        for ctx in AtulyaContext._contexts.values():
            ctxs.append({
                "id": ctx.id,
                "name": ctx.name,
                "no": ctx.no,
                "log_guid": ctx.log.guid,
                "log_version": len(ctx.log.updates),
                "log_length": len(ctx.log.logs),
                "paused": ctx.paused,
            })
        return {
            "context": context.id,
            "contexts": ctxs,
            "logs": logs,
            "log_guid": context.log.guid,
            "log_version": len(context.log.updates),
            "log_progress": context.log.progress,
            "log_progress_active": context.log.progress_active,
            "paused": context.paused,
        }
