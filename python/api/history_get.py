from python.helpers import tokens
from python.helpers.api import ApiHandler
from flask import Request, Response


class GetHistory(ApiHandler):
    async def process(self, input: dict, request: Request) -> dict | Response:
        ctxid = input.get("context", [])
        context = self.get_context(ctxid)
        atulya = context.streaming_atulya or context.atulya0
        history = atulya.history.output_text()
        size = atulya.history.get_tokens()

        return {
            "history": history,
            "tokens": size
        }