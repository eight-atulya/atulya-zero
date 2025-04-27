"""
Service module for chat history, export, load, reset.
"""
from atulya import AtulyaContext
from python.helpers import persist_chat
from typing import List

class HistoryService:
    @staticmethod
    async def get_history(ctxid: str):
        context = AtulyaContext.get(ctxid) if ctxid else AtulyaContext.first() or AtulyaContext()
        atulya = getattr(context, 'streaming_atulya', None) or getattr(context, 'atulya0', None)
        history = atulya.history.output_text()
        size = atulya.history.get_tokens()
        return {"history": history, "tokens": size}

    @staticmethod
    async def export_chat(ctxid: str):
        context = AtulyaContext.get(ctxid) if ctxid else AtulyaContext.first() or AtulyaContext()
        content = persist_chat.export_json_chat(context)
        return {"message": "Chats exported.", "ctxid": context.id, "content": content}

    @staticmethod
    async def load_chats(chats: List[dict]):
        ctxids = persist_chat.load_json_chats(chats)
        return {"message": "Chats loaded.", "ctxids": ctxids}

    @staticmethod
    async def reset_chat(ctxid: str):
        context = AtulyaContext.get(ctxid) if ctxid else AtulyaContext.first() or AtulyaContext()
        context.reset()
        persist_chat.save_tmp_chat(context)
        return {"message": "Atulya restarted."}
