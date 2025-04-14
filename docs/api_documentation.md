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
Currently, the API does not require authentication. However, this may change in future versions.

## Endpoints

### 1. `/` (GET)
- **Description**: Serves the main web UI.
- **Example**:
  ```bash
  curl http://localhost:50080/
  ```

### 2. `/message` (POST)
- **Description**: Handles user messages.
- **Request Body**:
  ```json
  {
    "message": "Your message here"
  }
  ```
- **Response**:
  ```json
  {
    "response": "Processed message response"
  }
  ```
- **Example**:
  ```bash
  curl -X POST http://localhost:50080/message -H "Content-Type: application/json" -d '{"message": "Hello"}'
  ```

### 3. `/pause` (POST)
- **Description**: Pauses or unpauses Atulya Zero.
- **Request Body**:
  ```json
  {
    "pause": true
  }
  ```
- **Response**:
  ```json
  {
    "status": "paused"
  }
  ```
- **Example**:
  ```bash
  curl -X POST http://localhost:50080/pause -H "Content-Type: application/json" -d '{"pause": true}'
  ```

### 4. `/restart` (POST)
- **Description**: Restarts the framework.
- **Request Body**: None.
- **Response**:
  ```json
  {
    "status": "restarted"
  }
  ```
- **Example**:
  ```bash
  curl -X POST http://localhost:50080/restart
  ```

### 5. `/rfc` (POST)
- **Description**: Handles remote function calls.
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

### 6. `/upload` (POST)
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

### 7. `/upload_work_dir_files` (POST)
- **Description**: Uploads files to the working directory.
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
  curl -X POST http://localhost:50080/upload_work_dir_files -F "file=@path/to/your/file"
  ```

### 8. `/transcribe` (POST)
- **Description**: Handles transcription tasks.
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

### 9. `/settings_set` (POST)
- **Description**: Updates settings.
- **Request Body**:
  ```json
  {
    "setting_name": "value"
  }
  ```
- **Response**:
  ```json
  {
    "status": "updated"
  }
  ```
- **Example**:
  ```bash
  curl -X POST http://localhost:50080/settings_set -H "Content-Type: application/json" -d '{"theme": "dark"}'
  ```

### 10. `/settings_get` (POST)
- **Description**: Retrieves settings.
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

### 11. `/poll` (POST)
- **Description**: Polls for updates.
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

### 12. `/health` (POST)
- **Description**: Performs a health check.
- **Request Body**: None.
- **Response**:
  ```json
  {
    "status": "healthy"
  }
  ```
- **Example**:
  ```bash
  curl -X POST http://localhost:50080/health
  ```

## Error Handling
- All endpoints return appropriate HTTP status codes.
- Error responses include a JSON body with an `error` field describing the issue.

## Notes
- Ensure the Docker container is running before accessing the API.
- Use tools like Postman or curl for testing the endpoints.

## Future Enhancements
- Authentication and authorization.
- Rate limiting.
- Detailed logging and monitoring.

For further assistance, refer to the [troubleshooting guide](./troubleshooting.md) or contact the development team.