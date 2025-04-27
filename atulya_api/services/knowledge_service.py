"""
Service module for knowledge import.
"""
from atulya import AtulyaContext
from python.helpers import files, memory
import os
from fastapi import UploadFile

class KnowledgeService:
    @staticmethod
    async def import_knowledge(ctxid: str, files_list: list[UploadFile]):
        context = AtulyaContext.get(ctxid) if ctxid else AtulyaContext.first() or AtulyaContext()
        KNOWLEDGE_FOLDER = files.get_abs_path(memory.get_custom_knowledge_subdir_abs(context.atulya0), "main")
        os.makedirs(KNOWLEDGE_FOLDER, exist_ok=True)
        saved_filenames = []
        for file in files_list:
            filename = file.filename
            if not filename:
                continue
            save_path = os.path.join(KNOWLEDGE_FOLDER, filename)
            with open(save_path, "wb") as f:
                f.write(await file.read())
            saved_filenames.append(filename)
        await memory.Memory.reload(context.atulya0)
        context.log.set_initial_progress()
        return {"message": "Knowledge Imported", "filenames": saved_filenames[:5]}
