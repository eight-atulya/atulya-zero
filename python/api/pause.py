from python.helpers.api import ApiHandler
from flask import Request, Response


class Pause(ApiHandler):
    async def process(self, input: dict, request: Request) -> dict | Response:
            # input data
            paused = input.get("paused", False)
            ctxid = input.get("context", "")

            # context instance - get or create
            context = self.get_context(ctxid)

            context.paused = paused

            return {
                "message": "Atulya paused." if paused else "Atulya unpaused.",
                "pause": paused,
            }    
