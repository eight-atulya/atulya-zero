"""
FastAPI router for accessing atulya-zero's API handlers.

This module provides REST endpoints that map to the original atulya-zero handlers.
"""
from fastapi import APIRouter, HTTPException, Depends, Request, Response, UploadFile, File, Form, Body
from fastapi.responses import JSONResponse
from typing import Dict, Any, List, Optional
import time

from django.contrib.auth.models import User

from ..core.atulya_connector import AtulyaConnector
from ..schemas.base import HandlerRequest, HandlerResponse, AvailableHandlersResponse, ErrorResponse
from ..utils.auth import validate_api_key, log_api_request, check_handler_permission
from ..models.models import ApiKey
from ..services.message_service import MessageService
from ..services.poll_service import PollService
from ..services.pause_service import PauseService
from ..services.settings_service import SettingsService
from ..services.file_service import FileService
from pydantic import BaseModel

from ..services.history_service import HistoryService
from ..services.knowledge_service import KnowledgeService
from ..services.transcribe_service import TranscribeService
from ..services.rfc_service import RFCService
from ..services.nudge_service import NudgeService
from ..services.restart_service import RestartService
from ..services.image_service import ImageService
from fastapi.responses import FileResponse

router = APIRouter(
    prefix="/handlers",
    tags=["handlers"],
    responses={
        404: {"model": ErrorResponse, "description": "Handler not found"},
        401: {"model": ErrorResponse, "description": "Authentication failed"},
        403: {"model": ErrorResponse, "description": "Permission denied"}
    },
)

def get_connector():
    """Dependency to get the AtulyaConnector instance"""
    connector = AtulyaConnector()
    connector.load_api_handlers()  # Ensure handlers are loaded
    return connector


@router.get("/", response_model=AvailableHandlersResponse)
async def list_handlers(
    request: Request,
    connector: AtulyaConnector = Depends(get_connector),
    api_key_data: tuple[ApiKey, User] = Depends(validate_api_key)
):
    """List all available API handlers"""
    # Start timing the request for logging
    request.state.request_time = time.time()
    api_key, user = api_key_data
    
    try:
        handlers = connector.get_available_handlers()
        
        # Create the response
        response = AvailableHandlersResponse(
            success=True,
            message="Available handlers retrieved successfully",
            handlers=handlers
        )
        
        # Log the request
        await log_api_request(
            request=request,
            response=response.dict(),
            user=user,
            handler="list_handlers"
        )
        
        return response
        
    except Exception as e:
        error_msg = f"Error retrieving handlers: {str(e)}"
        
        # Log the error
        await log_api_request(
            request=request,
            response={},
            user=user,
            handler="list_handlers",
            error=error_msg
        )
        
        raise HTTPException(status_code=500, detail=error_msg)


@router.post("/{handler_name}", response_model=HandlerResponse)
async def execute_handler(
    handler_name: str,
    request: Request,
    handler_request: HandlerRequest,
    connector: AtulyaConnector = Depends(get_connector),
    api_key_data: tuple[ApiKey, User] = Depends(validate_api_key)
):
    """Execute a specific API handler by name"""
    # Start timing the request for logging
    request.state.request_time = time.time()
    api_key, user = api_key_data
    
    try:
        # Check if the handler exists
        available_handlers = connector.get_available_handlers()
        if (handler_name not in available_handlers):
            error_msg = f"Handler '{handler_name}' not found. Available handlers: {available_handlers}"
            
            # Log the error
            await log_api_request(
                request=request,
                response={},
                user=user,
                handler=handler_name,
                error=error_msg
            )
            
            raise HTTPException(status_code=404, detail=error_msg)
        
        # Check if the API key has permission to use this handler
        if not check_handler_permission(api_key, handler_name):
            error_msg = f"Permission denied: API key does not have access to handler '{handler_name}'"
            
            # Log the error
            await log_api_request(
                request=request,
                response={},
                user=user,
                handler=handler_name,
                error=error_msg
            )
            
            raise HTTPException(status_code=403, detail=error_msg)
        
        # Execute the handler with the provided parameters
        result = connector.execute_handler(handler_name, handler_request.params)
        
        # Create the response
        response = HandlerResponse(
            success=True,
            message=f"Handler '{handler_name}' executed successfully",
            data=result
        )
        
        # Log the request
        await log_api_request(
            request=request,
            response=response.dict(),
            user=user,
            handler=handler_name
        )
        
        return response
        
    except HTTPException as e:
        # Re-raise HTTP exceptions
        raise e
        
    except ValueError as e:
        error_msg = str(e)
        
        # Log the error
        await log_api_request(
            request=request,
            response={},
            user=user,
            handler=handler_name,
            error=error_msg
        )
        
        raise HTTPException(status_code=404, detail=error_msg)
        
    except Exception as e:
        error_msg = f"Error executing handler: {str(e)}"
        
        # Log the error
        await log_api_request(
            request=request,
            response={},
            user=user,
            handler=handler_name,
            error=error_msg
        )
        
        # Log the exception for debugging
        print(f"Error executing handler {handler_name}: {e}")
        raise HTTPException(status_code=500, detail=error_msg)


class MessageRequest(BaseModel):
    text: str
    context: Optional[str] = None
    message_id: Optional[str] = None

class MessageResponse(BaseModel):
    message: str
    context: Optional[str]

@router.post("/message", response_model=MessageResponse, tags=["handlers"])
async def message_handler(
    text: str = Form(..., description="User message text"),
    context: Optional[str] = Form(None, description="Context ID for the chat"),
    message_id: Optional[str] = Form(None, description="Optional message ID for tracking"),
    attachments: list[UploadFile] = File(None, description="Optional file attachments")
):
    """
    Handle a user message, including optional attachments, and return the Atulya response.
    ---
    - Accepts text, context ID, message ID, and file attachments (multipart/form-data).
    - Returns the Atulya response and context ID.
    """
    result, ctxid = await MessageService.handle_message(
        text=text,
        ctxid=context,
        message_id=message_id,
        attachments=attachments
    )
    return MessageResponse(message=result, context=ctxid)

class PollRequest(BaseModel):
    context: Optional[str] = None
    log_from: int = 0
class PollResponse(BaseModel):
    context: str
    contexts: list
    logs: list
    log_guid: str
    log_version: int
    log_progress: str
    log_progress_active: bool
    paused: bool

@router.post("/poll", response_model=PollResponse, tags=["handlers"])
async def poll_handler(
    context: Optional[str] = Body(None, description="Context ID for the chat"),
    log_from: int = Body(0, description="Log start index")
):
    """
    Poll the Atulya context for logs and status.
    """
    result = await PollService.poll_context(ctxid=context, log_from=log_from)
    return PollResponse(**result)

class PauseRequest(BaseModel):
    paused: bool
    context: Optional[str] = None
class PauseResponse(BaseModel):
    message: str
    pause: bool

@router.post("/pause", response_model=PauseResponse, tags=["handlers"])
async def pause_handler(
    paused: bool = Body(..., description="Pause or unpause Atulya"),
    context: Optional[str] = Body(None, description="Context ID for the chat")
):
    """
    Pause or unpause the Atulya context.
    """
    result = await PauseService.set_paused(paused=paused, ctxid=context)
    return PauseResponse(**result)

class SettingsResponse(BaseModel):
    settings: dict

@router.post("/settings_get", response_model=SettingsResponse, tags=["handlers"])
async def settings_get_handler():
    """
    Get current Atulya settings.
    """
    result = await SettingsService.get_settings()
    if isinstance(result, BaseModel):
        settings_dict = result.model_dump()
    elif isinstance(result, dict):
        settings_dict = result
    else:
        settings_dict = dict(result)
    return SettingsResponse(settings=settings_dict)

@router.post("/settings_set", response_model=SettingsResponse, tags=["handlers"])
async def settings_set_handler(
    settings: dict = Body(..., description="Settings to update")
):
    """
    Set Atulya settings.
    """
    result = await SettingsService.set_settings(settings)
    if isinstance(result, BaseModel):
        settings_dict = result.model_dump()
    elif isinstance(result, dict):
        settings_dict = result
    else:
        settings_dict = dict(result)
    return SettingsResponse(settings=settings_dict)

class FileUploadResponse(BaseModel):
    filenames: list[str]

@router.post("/upload", response_model=FileUploadResponse, tags=["handlers"])
async def upload_handler(
    files: list[UploadFile] = File(..., description="Files to upload")
):
    """
    Upload one or more files to the server.
    """
    filenames = await FileService.upload_files(files)
    return FileUploadResponse(filenames=filenames)

class FileInfoResponse(BaseModel):
    input_path: str
    abs_path: str
    exists: bool
    is_dir: bool
    is_file: bool
    size: int
    modified: float
    created: float
    file_name: str

@router.get("/file_info", response_model=FileInfoResponse, tags=["handlers"])
async def file_info_handler(
    path: str
):
    """
    Get file or directory metadata.
    """
    info = await FileService.get_file_info(path)
    return FileInfoResponse(**info)

class FileDeleteRequest(BaseModel):
    path: str
class FileDeleteResponse(BaseModel):
    success: bool

@router.delete("/file_delete", response_model=FileDeleteResponse, tags=["handlers"])
async def file_delete_handler(
    path: str = Body(..., description="Path to file to delete")
):
    """
    Delete a file by path.
    """
    success = await FileService.delete_file(path)
    return FileDeleteResponse(success=success)

class FileListResponse(BaseModel):
    files: list[str]

@router.get("/file_list", response_model=FileListResponse, tags=["handlers"])
async def file_list_handler(
    directory: str
):
    """
    List files in a directory.
    """
    files = await FileService.list_files(directory)
    return FileListResponse(files=files)

class HistoryResponse(BaseModel):
    history: str
    tokens: int

@router.get("/history_get", response_model=HistoryResponse, tags=["handlers"])
async def history_get_handler(
    context: str
):
    """
    Get chat history and token count for a context.
    """
    result = await HistoryService.get_history(context)
    return HistoryResponse(**result)

class ChatExportResponse(BaseModel):
    message: str
    ctxid: str
    content: dict

@router.get("/chat_export", response_model=ChatExportResponse, tags=["handlers"])
async def chat_export_handler(
    ctxid: str
):
    """
    Export chat session as JSON.
    """
    result = await HistoryService.export_chat(ctxid)
    message = result.get("message", "")
    ctxid_val = result.get("ctxid", "")
    content = result.get("content", {})
    if not isinstance(content, dict):
        import json
        try:
            content = json.loads(content)
        except Exception:
            content = {}
    return ChatExportResponse(message=message, ctxid=ctxid_val, content=content)

class ChatLoadRequest(BaseModel):
    chats: list[dict]
class ChatLoadResponse(BaseModel):
    message: str
    ctxids: list[str]

@router.post("/chat_load", response_model=ChatLoadResponse, tags=["handlers"])
async def chat_load_handler(
    chats: list[dict] = Body(..., description="Chats to load")
):
    """
    Load chat sessions from JSON.
    """
    result = await HistoryService.load_chats(chats)
    return ChatLoadResponse(**result)

class ChatResetResponse(BaseModel):
    message: str

@router.post("/chat_reset", response_model=ChatResetResponse, tags=["handlers"])
async def chat_reset_handler(
    context: str = Body(..., description="Context ID to reset")
):
    """
    Reset a chat context.
    """
    result = await HistoryService.reset_chat(context)
    return ChatResetResponse(**result)

class KnowledgeImportResponse(BaseModel):
    message: str
    filenames: list[str]

@router.post("/import_knowledge", response_model=KnowledgeImportResponse, tags=["handlers"])
async def import_knowledge_handler(
    context: str = Form(..., description="Context ID for knowledge import"),
    files: list[UploadFile] = File(..., description="Knowledge files to import")
):
    """
    Import knowledge files and reload memory.
    """
    result = await KnowledgeService.import_knowledge(context, files)
    return KnowledgeImportResponse(message=result["message"], filenames=result["filenames"])

class TranscribeRequest(BaseModel):
    audio: str
    ctxid: Optional[str] = None
class TranscribeResponse(BaseModel):
    transcription: str

@router.post("/transcribe", response_model=TranscribeResponse, tags=["handlers"])
async def transcribe_handler(
    audio: str = Body(..., description="Base64-encoded audio file"),
    ctxid: Optional[str] = Body(None, description="Context ID")
):
    """
    Transcribe audio using the Whisper model.
    """
    ctxid_val = ctxid if ctxid is not None else ""
    result = await TranscribeService.transcribe(audio, ctxid_val)
    return TranscribeResponse(transcription=result)

class RFCRequest(BaseModel):
    function: str
    args: list
class RFCResponse(BaseModel):
    result: str

@router.post("/rfc", response_model=RFCResponse, tags=["handlers"])
async def rfc_handler(
    function: str = Body(..., description="Function name"),
    args: list = Body(..., description="Function arguments")
):
    """
    Handle remote function call.
    """
    result = await RFCService.handle_rfc({"function": function, "args": args})
    return RFCResponse(result=result)

class NudgeRequest(BaseModel):
    ctxid: str
class NudgeResponse(BaseModel):
    message: str
    ctxid: str

@router.post("/nudge", response_model=NudgeResponse, tags=["handlers"])
async def nudge_handler(
    ctxid: str = Body(..., description="Context ID to nudge")
):
    """
    Nudge (reset) the Atulya context.
    """
    result = await NudgeService.nudge(ctxid)
    return NudgeResponse(**result)

class RestartResponse(BaseModel):
    message: str

@router.post("/restart", response_model=RestartResponse, tags=["handlers"])
async def restart_handler():
    """
    Restart the Atulya process.
    """
    result = await RestartService.restart()
    message = result["message"] if isinstance(result, dict) and "message" in result else str(result)
    return RestartResponse(message=message)

@router.get("/image_get", response_class=FileResponse, tags=["handlers"])
async def image_get_handler(
    path: str
):
    """
    Serve an image file by path.
    """
    return await ImageService.get_image(path)