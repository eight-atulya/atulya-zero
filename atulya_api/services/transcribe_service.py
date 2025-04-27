"""
Service module for audio transcription using Whisper.
"""
from python.helpers import runtime, settings, whisper
from atulya import AtulyaContext

class TranscribeService:
    @staticmethod
    async def transcribe(audio: str, ctxid: str = ""):
        context = AtulyaContext.get(ctxid) if ctxid else AtulyaContext.first() or AtulyaContext()
        if await whisper.is_downloading():
            context.log.log(type="info", content="Whisper model is currently being downloaded, please wait...")
        set = settings.get_settings()
        result = await whisper.transcribe(set["stt_model_size"], audio)
        return result
