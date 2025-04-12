from python.helpers.api import ApiHandler, Input, Output, Request, Response


from atulya import AtulyaContext
from python.helpers import persist_chat


class RemoveChat(ApiHandler):
    async def process(self, input: Input, request: Request) -> Output:
        ctxid = input.get("context", "")

        # context instance - get or create
        AtulyaContext.remove(ctxid)
        persist_chat.remove_chat(ctxid)

        return {
            "message": "Context removed.",
        }
