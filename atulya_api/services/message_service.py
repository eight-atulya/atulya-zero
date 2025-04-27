"""
Service module for message handling in atulya_api.
Handles user messages, attachments, and Atulya context communication.
"""
from typing import List, Optional, Tuple
import os
from atulya import AtulyaContext, UserMessage
from fastapi import UploadFile

class MessageService:
    @staticmethod
    async def handle_message(
        text: str,
        ctxid: Optional[str] = None,
        message_id: Optional[str] = None,
        attachments: Optional[List[UploadFile]] = None
    ) -> Tuple[str, str]:
        """
        Process a user message, handle attachments, and communicate with Atulya context.
        Returns: (response_message, context_id)
        """
        attachment_paths = []
        if attachments:
            upload_folder_ext = os.path.abspath("tmp/uploads")
            os.makedirs(upload_folder_ext, exist_ok=True)
            for attachment in attachments:
                filename = attachment.filename
                if not filename:
                    continue
                save_path = os.path.join(upload_folder_ext, filename)
                with open(save_path, "wb") as f:
                    f.write(await attachment.read())
                attachment_paths.append(save_path)

        # Obtain or create Atulya context
        context = AtulyaContext.get(ctxid) if ctxid else AtulyaContext.first() or AtulyaContext()
        # Log the message (can be extended for more detailed logging)
        context.log.log(
            type="user",
            heading="User message",
            content=text,
            kvps={"attachments": [os.path.basename(p) for p in attachment_paths]},
            id=message_id,
        )
        # Communicate with Atulya
        result = await context.communicate(UserMessage(text, attachment_paths))
        return result, context.id
