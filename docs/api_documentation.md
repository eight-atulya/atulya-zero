# Atulya Zero API Documentation

## Overview
Atulya Zero provides a robust API for interacting with its backend services. This document outlines the available API endpoints, their purposes, and how to use them effectively. The API is designed to be accessed via HTTP requests, and it supports both GET and POST methods depending on the endpoint.

## Base URL
The API is accessible at the following base URL when running locally:
```
http://localhost:50080
```

Replace `localhost` with the appropriate IP address or domain name if accessing the API from a remote machine.

## Authentication
The API supports multiple authentication methods:
- **Basic Authentication**: Username/password (configured via `AUTH_LOGIN` and `AUTH_PASSWORD` environment variables)
- **API Key**: Via `X-API-KEY` header or `api_key` in request body (configured via `API_KEY` environment variable)
- **Loopback-only**: Some endpoints are restricted to localhost access only

## Endpoints

### Core Messaging & Communication

### 1. `/` (GET)
- **Description**: Serves the main web UI.
- **Authentication**: Basic auth required
- **Example**:
  ```bash
  curl http://localhost:50080/
  ```

### 2. `/message` (POST)
- **Description**: Handles user messages and chat interactions. Supports both JSON and multipart form data for file attachments.
- **Authentication**: Basic auth required
- **Request Body (JSON)**:
  ```json
  {
    "text": "Your message here",
    "context": "optional_context_id"
  }
  ```
- **Request Body (Multipart)**:
  ```
  text: "Your message here"
  context: "optional_context_id"
  attachments: [files]
  ```
- **Response**:
  ```json
  {
    "message": "Processed message response",
    "context": "context_id"
  }
  ```
- **Example**:
  ```bash
  curl -X POST http://localhost:50080/message -H "Content-Type: application/json" -d '{"text": "Hello"}'
  ```

### 3. `/message_async` (POST)
- **Description**: Handles asynchronous message processing (returns immediately).
- **Authentication**: Basic auth required
- **Request Body**: Same as `/message`
- **Response**:
  ```json
  {
    "message": "Message received.",
    "context": "context_id"
  }
  ```

### 4. `/pause` (POST)
- **Description**: Pauses or unpauses Atulya Zero.
- **Authentication**: Basic auth required
- **Request Body**:
  ```json
  {
    "paused": true,
    "context": "optional_context_id"
  }
  ```
- **Response**:
  ```json
  {
    "message": "Atulya paused.",
    "pause": true
  }
  ```
- **Example**:
  ```bash
  curl -X POST http://localhost:50080/pause -H "Content-Type: application/json" -d '{"paused": true}'
  ```

### 5. `/restart` (POST)
- **Description**: Restarts the framework.
- **Authentication**: Basic auth required
- **Request Body**: None.
- **Response**: HTTP 200 (empty response)
- **Example**:
  ```bash
  curl -X POST http://localhost:50080/restart
  ```

### 6. `/rfc` (POST)
- **Description**: Handles remote function calls.
- **Authentication**: Basic auth required
- **Request Body**:
  ```json
  {
    "function": "function_name",
    "args": ["arg1", "arg2"]
  }
  ```
- **Response**:
  ```json
  {
    "result": "Function result"
  }
  ```
- **Example**:
  ```bash
  curl -X POST http://localhost:50080/rfc -H "Content-Type: application/json" -d '{"function": "add", "args": [1, 2]}'
  ```

### 7. `/nudge` (POST)
- **Description**: Sends nudge notifications.
- **Authentication**: Basic auth required

### File Management

### 8. `/upload` (POST)
- **Description**: Uploads files.
- **Request Body**: Multipart form data containing the file.
- **Response**:
  ```json
  {
    "status": "success",
    "file_id": "unique_file_id"
  }
  ```
- **Example**:
  ```bash
  curl -X POST http://localhost:50080/upload -F "file=@path/to/your/file"
  ```

### 8. `/upload` (POST)
- **Description**: Uploads files to temp directory.
- **Authentication**: Basic auth required
- **Request Body**: Multipart form data containing the file.
- **Response**:
  ```json
  {
    "filenames": ["uploaded_file.txt"]
  }
  ```
- **Example**:
  ```bash
  curl -X POST http://localhost:50080/upload -F "file=@path/to/your/file"
  ```

### 9. `/upload_work_dir_files` (POST)
- **Description**: Uploads files to the working directory.
- **Authentication**: Basic auth required
- **Request Body**: Multipart form data or base64 encoded files.
- **Response**:
  ```json
  {
    "message": "Files uploaded successfully"
  }
  ```
- **Example**:
  ```bash
  curl -X POST http://localhost:50080/upload_work_dir_files -F "file=@path/to/your/file"
  ```

### 10. `/download_work_dir_file` (POST/GET)
- **Description**: Downloads files from working directory.
- **Authentication**: Basic auth required
- **Request Body/Query**:
  ```json
  {
    "path": "path/to/file"
  }
  ```
- **Response**: File download
- **Example**:
  ```bash
  curl -X POST http://localhost:50080/download_work_dir_file -H "Content-Type: application/json" -d '{"path": "file.txt"}'
  ```

### 11. `/delete_work_dir_file` (POST)
- **Description**: Deletes files from working directory.
- **Authentication**: Basic auth required
- **Request Body**:
  ```json
  {
    "path": "path/to/file"
  }
  ```

### 12. `/get_work_dir_files` (GET)
- **Description**: Lists files in working directory.
- **Authentication**: Basic auth required
- **Query Parameters**: `path` (optional, defaults to root)
- **Response**:
  ```json
  {
    "data": {
      "files": [...],
      "folders": [...]
    }
  }
  ```
- **Example**:
  ```bash
  curl http://localhost:50080/get_work_dir_files?path=subfolder
  ```

### 13. `/file_info` (POST)
- **Description**: Gets file information.
- **Authentication**: Basic auth required

### 14. `/image_get` (GET)
- **Description**: Retrieves images with path validation.
- **Authentication**: Basic auth required
- **Query Parameters**: `path` (required)
- **Response**: Image file
- **Example**:
  ```bash
  curl http://localhost:50080/image_get?path=image.png
  ```

### Chat & Context Management

### 15. `/chat_export` (POST)
- **Description**: Exports chat conversations.
- **Authentication**: Basic auth required
- **Request Body**:
  ```json
  {
    "ctxid": "context_id"
  }
  ```
- **Response**:
  ```json
  {
    "message": "Chats exported.",
    "ctxid": "context_id",
    "content": "exported_chat_data"
  }
  ```

### 16. `/chat_load` (POST)
- **Description**: Loads chat conversations.
- **Authentication**: Basic auth required
- **Request Body**:
  ```json
  {
    "chats": ["chat_data_array"]
  }
  ```
- **Response**:
  ```json
  {
    "message": "Chats loaded.",
    "ctxids": ["context_ids"]
  }
  ```

### 17. `/chat_remove` (POST)
- **Description**: Removes chat conversations.
- **Authentication**: Basic auth required

### 18. `/chat_reset` (POST)
- **Description**: Resets chat conversations.
- **Authentication**: Basic auth required

### 19. `/history_get` (POST)
- **Description**: Retrieves conversation history.
- **Authentication**: Basic auth required
- **Request Body**:
  ```json
  {
    "context": "context_id"
  }
  ```
- **Response**:
  ```json
  {
    "history": "conversation_history",
    "tokens": 1234
  }
  ```

### 20. `/ctx_window_get` (POST)
- **Description**: Gets context window information.
- **Authentication**: Basic auth required

### Settings & Configuration

### 21. `/settings_set` (POST)
- **Description**: Updates application settings.
- **Authentication**: Basic auth required
- **Request Body**:
  ```json
  {
    "setting_name": "value"
  }
  ```
- **Response**:
  ```json
  {
    "settings": {...}
  }
  ```
- **Example**:
  ```bash
  curl -X POST http://localhost:50080/settings_set -H "Content-Type: application/json" -d '{"theme": "dark"}'
  ```

### 22. `/settings_get` (POST)
- **Description**: Retrieves current settings.
- **Authentication**: Basic auth required
- **Request Body**: None.
- **Response**:
  ```json
  {
    "settings": {
      "theme": "dark"
    }
  }
  ```
- **Example**:
  ```bash
  curl -X POST http://localhost:50080/settings_get
  ```

### Task Scheduling

### 23. `/scheduler_tasks_list` (POST)
- **Description**: Lists all scheduled tasks.
- **Authentication**: Basic auth required
- **Request Body**:
  ```json
  {
    "timezone": "optional_timezone"
  }
  ```

### 24. `/scheduler_task_create` (POST)
- **Description**: Creates new scheduled tasks.
- **Authentication**: Basic auth required

### 25. `/scheduler_task_delete` (POST)
- **Description**: Deletes scheduled tasks.
- **Authentication**: Basic auth required

### 26. `/scheduler_task_run` (POST)
- **Description**: Runs scheduled tasks.
- **Authentication**: Basic auth required

### 27. `/scheduler_task_update` (POST)
- **Description**: Updates scheduled tasks.
- **Authentication**: Basic auth required

### 28. `/scheduler_tick` (POST)
- **Description**: Triggers scheduler tick.
- **Authentication**: Basic auth required

### Tunneling & Network

### 29. `/tunnel` (POST)
- **Description**: Manages Cloudflare tunnels (create/stop/get status).
- **Authentication**: Basic auth required
- **Request Body**:
  ```json
  {
    "action": "create|stop|get|health"
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "tunnel_url": "https://tunnel-url.trycloudflare.com",
    "message": "Tunnel created successfully"
  }
  ```

### 30. `/tunnel_proxy` (POST)
- **Description**: Proxies tunnel requests to tunnel service.
- **Authentication**: Basic auth required

### System & Monitoring

### 31. `/health` (POST)
- **Description**: Health check endpoint with git information.
- **Authentication**: Basic auth required
- **Request Body**: None.
- **Response**:
  ```json
  {
    "gitinfo": {
      "version": "v1.0.0",
      "commit_time": "2025-05-30"
    },
    "error": null
  }
  ```
- **Example**:
  ```bash
  curl -X POST http://localhost:50080/health
  ```

### 32. `/poll` (POST)
- **Description**: Polls for updates.
- **Authentication**: Basic auth required
- **Request Body**: None.
- **Response**:
  ```json
  {
    "updates": []
  }
  ```
- **Example**:
  ```bash
  curl -X POST http://localhost:50080/poll
  ```

### Additional Features

### 33. `/transcribe` (POST)
### 33. `/transcribe` (POST)
- **Description**: Handles audio transcription tasks.
- **Authentication**: Basic auth required
- **Request Body**:
  ```json
  {
    "audio_file": "base64_encoded_audio"
  }
  ```
- **Response**:
  ```json
  {
    "transcription": "Transcribed text"
  }
  ```
- **Example**:
  ```bash
  curl -X POST http://localhost:50080/transcribe -H "Content-Type: application/json" -d '{"audio_file": "base64_encoded_audio"}'
  ```

### 34. `/import_knowledge` (POST)
- **Description**: Imports knowledge base content.
- **Authentication**: Basic auth required

## Error Handling
- All endpoints return appropriate HTTP status codes.
- Error responses include a JSON body with an `error` field describing the issue.
- 401: Authentication required or invalid credentials
- 403: Access denied (e.g., non-loopback access to restricted endpoints)
- 500: Internal server error

## Authentication Details
- **Basic Auth**: Set via `AUTH_LOGIN` and `AUTH_PASSWORD` environment variables
- **API Key**: Set via `API_KEY` environment variable, can be passed as:
  - Header: `X-API-KEY: your_api_key`
  - JSON body: `{"api_key": "your_api_key"}`
- **Loopback-only**: Some endpoints only accept requests from localhost (127.0.0.1)

## Request/Response Format
- Most endpoints accept JSON requests with `Content-Type: application/json`
- File upload endpoints use `multipart/form-data`
- All successful responses return JSON (except file downloads)
- File paths should be relative to the working directory and are validated for security

## Notes
- Ensure the Docker container is running before accessing the API.
- Use tools like Postman or curl for testing the endpoints.
- The API runs on port 50080 by default (configurable via environment variables)
- Context IDs are used to maintain conversation state across multiple requests

## Future Enhancements
- Rate limiting.
- Detailed logging and monitoring.
- Enhanced security features.

For further assistance, refer to the [troubleshooting guide](./troubleshooting.md) or contact the development team.