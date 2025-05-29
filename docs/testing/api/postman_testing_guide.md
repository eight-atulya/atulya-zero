# Atulya Zero API Testing with Postman - Developer Guide

## Table of Contents
1. [Overview](#overview)
2. [Environment Setup](#environment-setup)
3. [Authentication Configuration](#authentication-configuration)
4. [Collection Structure](#collection-structure)
5. [Endpoint Testing Details](#endpoint-testing-details)
6. [Automated Testing Scripts](#automated-testing-scripts)
7. [Error Handling & Validation](#error-handling--validation)
8. [Performance Testing](#performance-testing)
9. [CI/CD Integration](#cicd-integration)
10. [Troubleshooting](#troubleshooting)

## Overview

This guide provides comprehensive instructions for testing Atulya Zero API endpoints using Postman. It's designed for developers who need to perform thorough API testing, validation, and integration testing.

### Prerequisites
- Postman Desktop App (recommended) or Postman Web
- Atulya Zero running locally or accessible instance
- Basic understanding of HTTP methods and JSON
- Knowledge of Postman features (environments, collections, scripts)

## Environment Setup

### 1. Create Postman Environment

Create a new environment in Postman with the following variables:

```json
{
  "base_url": "http://localhost:50080",
  "auth_username": "your_username",
  "auth_password": "your_password",
  "api_key": "your_api_key",
  "context_id": "",
  "file_path": "",
  "tunnel_url": "",
  "upload_file_name": "",
  "chat_export_data": "",
  "task_id": "",
  "timezone": "UTC"
}
```

### 2. Environment Variables Explanation

| Variable | Description | Usage |
|----------|-------------|-------|
| `base_url` | Base URL of Atulya Zero API | All requests |
| `auth_username` | Basic auth username | Authentication |
| `auth_password` | Basic auth password | Authentication |
| `api_key` | API key for key-based auth | Alternative auth |
| `context_id` | Current conversation context ID | Message/chat endpoints |
| `file_path` | Path for file operations | File management |
| `tunnel_url` | Cloudflare tunnel URL | Tunnel testing |
| `upload_file_name` | Name of uploaded file | File upload testing |
| `chat_export_data` | Exported chat data | Chat import/export |
| `task_id` | Scheduler task ID | Task management |
| `timezone` | Timezone for scheduler | Task scheduling |

## Authentication Configuration

### Basic Authentication Setup

1. **Collection Level Auth**:
   - Select your collection
   - Go to "Authorization" tab
   - Type: "Basic Auth"
   - Username: `{{auth_username}}`
   - Password: `{{auth_password}}`

2. **Request Level Auth Override**:
   For API key endpoints, override at request level:
   - Type: "No Auth"
   - Add header: `X-API-KEY: {{api_key}}`

### Pre-request Authentication Script

Add this script to your collection's "Pre-request Script":

```javascript
// Auto-generate basic auth header if credentials exist
if (pm.environment.get("auth_username") && pm.environment.get("auth_password")) {
    const username = pm.environment.get("auth_username");
    const password = pm.environment.get("auth_password");
    const credentials = btoa(username + ":" + password);
    pm.request.headers.add({
        key: "Authorization",
        value: "Basic " + credentials
    });
}

// Set common headers
pm.request.headers.add({
    key: "Content-Type",
    value: "application/json"
});

// Log request details for debugging
console.log("Request URL:", pm.request.url.toString());
console.log("Request Method:", pm.request.method);
```

## Collection Structure

Organize your Postman collection with the following folder structure:

```
Atulya Zero API Tests/
├── 01_System_Health/
│   ├── Health Check
│   └── Basic Connectivity
├── 02_Authentication/
│   ├── Basic Auth Test
│   ├── API Key Test
│   └── Invalid Auth Test
├── 03_Core_Messaging/
│   ├── Send Message (JSON)
│   ├── Send Message (Multipart)
│   ├── Message Async
│   ├── Pause/Unpause
│   └── Restart
├── 04_File_Management/
│   ├── Upload to Temp
│   ├── Upload to Work Dir
│   ├── List Work Dir Files
│   ├── Download File
│   ├── Delete File
│   ├── Get File Info
│   └── Get Image
├── 05_Chat_Context/
│   ├── Export Chat
│   ├── Load Chat
│   ├── Remove Chat
│   ├── Reset Chat
│   ├── Get History
│   └── Get Context Window
├── 06_Settings/
│   ├── Get Settings
│   └── Set Settings
├── 07_Task_Scheduling/
│   ├── List Tasks
│   ├── Create Task
│   ├── Update Task
│   ├── Run Task
│   ├── Delete Task
│   └── Trigger Tick
├── 08_Tunneling/
│   ├── Create Tunnel
│   ├── Get Tunnel Status
│   ├── Stop Tunnel
│   └── Tunnel Proxy
├── 09_Additional_Features/
│   ├── Transcribe Audio
│   ├── Import Knowledge
│   ├── RFC Call
│   ├── Nudge
│   └── Poll Updates
└── 10_Error_Scenarios/
    ├── Invalid Endpoints
    ├── Malformed Requests
    ├── Missing Auth
    └── Invalid File Paths
```

## Endpoint Testing Details

### Core Messaging Endpoints

#### 1. Health Check (`/health`)

**Request Setup**:
```
Method: POST
URL: {{base_url}}/health
Body: {} (empty JSON)
```

**Test Script**:
```javascript
pm.test("Health check returns 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response contains git info", function () {
    const jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('gitinfo');
});

pm.test("Response time is acceptable", function () {
    pm.expect(pm.response.responseTime).to.be.below(1000);
});

// Store git info for later use
const response = pm.response.json();
if (response.gitinfo) {
    pm.environment.set("git_version", response.gitinfo.version);
}
```

#### 2. Send Message (`/message`)

**JSON Request Setup**:
```
Method: POST
URL: {{base_url}}/message
Headers: Content-Type: application/json
Body:
{
    "text": "Hello, this is a test message",
    "context": "{{context_id}}"
}
```

**Multipart Request Setup**:
```
Method: POST
URL: {{base_url}}/message
Body: form-data
- text: "Hello with attachment"
- context: {{context_id}}
- attachments: [select file]
```

**Test Script**:
```javascript
pm.test("Message sent successfully", function () {
    pm.response.to.have.status(200);
});

pm.test("Response contains message and context", function () {
    const jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('message');
    pm.expect(jsonData).to.have.property('context');
    
    // Store context ID for subsequent requests
    pm.environment.set("context_id", jsonData.context);
});

pm.test("Context ID is valid UUID format", function () {
    const jsonData = pm.response.json();
    const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
    pm.expect(jsonData.context).to.match(uuidRegex);
});
```

#### 3. Async Message (`/message_async`)

**Request Setup**:
```
Method: POST
URL: {{base_url}}/message_async
Body:
{
    "text": "Async test message",
    "context": "{{context_id}}"
}
```

**Test Script**:
```javascript
pm.test("Async message accepted", function () {
    pm.response.to.have.status(200);
});

pm.test("Response indicates message received", function () {
    const jsonData = pm.response.json();
    pm.expect(jsonData.message).to.include("received");
});

pm.test("Response time is fast (async)", function () {
    pm.expect(pm.response.responseTime).to.be.below(500);
});
```

### File Management Endpoints

#### 4. Upload File (`/upload`)

**Request Setup**:
```
Method: POST
URL: {{base_url}}/upload
Body: form-data
- file: [select file]
```

**Test Script**:
```javascript
pm.test("File uploaded successfully", function () {
    pm.response.to.have.status(200);
});

pm.test("Response contains filenames", function () {
    const jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('filenames');
    pm.expect(jsonData.filenames).to.be.an('array');
    
    if (jsonData.filenames.length > 0) {
        pm.environment.set("upload_file_name", jsonData.filenames[0]);
    }
});
```

#### 5. List Work Directory Files (`/get_work_dir_files`)

**Request Setup**:
```
Method: GET
URL: {{base_url}}/get_work_dir_files?path={{file_path}}
```

**Test Script**:
```javascript
pm.test("Directory listing successful", function () {
    pm.response.to.have.status(200);
});

pm.test("Response contains data structure", function () {
    const jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('data');
    pm.expect(jsonData.data).to.have.property('files');
    pm.expect(jsonData.data).to.have.property('folders');
});

// Store first file path for download testing
const response = pm.response.json();
if (response.data.files && response.data.files.length > 0) {
    pm.environment.set("file_path", response.data.files[0].path);
}
```

#### 6. Download File (`/download_work_dir_file`)

**Request Setup**:
```
Method: POST
URL: {{base_url}}/download_work_dir_file
Body:
{
    "path": "{{file_path}}"
}
```

**Test Script**:
```javascript
pm.test("File download successful", function () {
    pm.response.to.have.status(200);
});

pm.test("Response is file content", function () {
    // Check if response is binary or has content-disposition header
    const contentType = pm.response.headers.get("Content-Type");
    const contentDisposition = pm.response.headers.get("Content-Disposition");
    
    pm.expect(contentType || contentDisposition).to.exist;
});
```

### Chat & Context Management

#### 7. Export Chat (`/chat_export`)

**Request Setup**:
```
Method: POST
URL: {{base_url}}/chat_export
Body:
{
    "ctxid": "{{context_id}}"
}
```

**Test Script**:
```javascript
pm.test("Chat export successful", function () {
    pm.response.to.have.status(200);
});

pm.test("Export contains chat data", function () {
    const jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('content');
    pm.expect(jsonData).to.have.property('ctxid');
    
    // Store exported data for import testing
    pm.environment.set("chat_export_data", JSON.stringify(jsonData.content));
});
```

#### 8. Load Chat (`/chat_load`)

**Request Setup**:
```
Method: POST
URL: {{base_url}}/chat_load
Body:
{
    "chats": [{{chat_export_data}}]
}
```

**Test Script**:
```javascript
pm.test("Chat load successful", function () {
    pm.response.to.have.status(200);
});

pm.test("Load returns context IDs", function () {
    const jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('ctxids');
    pm.expect(jsonData.ctxids).to.be.an('array');
});
```

### Task Scheduling Endpoints

#### 9. List Tasks (`/scheduler_tasks_list`)

**Request Setup**:
```
Method: POST
URL: {{base_url}}/scheduler_tasks_list
Body:
{
    "timezone": "{{timezone}}"
}
```

**Test Script**:
```javascript
pm.test("Task list retrieved", function () {
    pm.response.to.have.status(200);
});

pm.test("Response contains tasks array", function () {
    const jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('tasks');
    
    // Store first task ID if available
    if (jsonData.tasks && jsonData.tasks.length > 0) {
        pm.environment.set("task_id", jsonData.tasks[0].id);
    }
});
```

#### 10. Create Task (`/scheduler_task_create`)

**Request Setup**:
```
Method: POST
URL: {{base_url}}/scheduler_task_create
Body:
{
    "name": "Test Task",
    "schedule": "0 */1 * * *",
    "action": "test_action",
    "enabled": true
}
```

**Test Script**:
```javascript
pm.test("Task created successfully", function () {
    pm.response.to.have.status(200);
});

pm.test("Response contains task ID", function () {
    const jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('task_id');
    pm.environment.set("task_id", jsonData.task_id);
});
```

### Tunneling Endpoints

#### 11. Create Tunnel (`/tunnel`)

**Request Setup**:
```
Method: POST
URL: {{base_url}}/tunnel
Body:
{
    "action": "create"
}
```

**Test Script**:
```javascript
pm.test("Tunnel creation initiated", function () {
    pm.response.to.have.status(200);
});

pm.test("Response contains tunnel info", function () {
    const jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('success');
    
    if (jsonData.tunnel_url) {
        pm.environment.set("tunnel_url", jsonData.tunnel_url);
    }
});
```

## Automated Testing Scripts

### Collection-Level Pre-request Script

```javascript
// Global variables and utilities
pm.globals.set("timestamp", new Date().toISOString());

// Function to generate random test data
function generateTestData() {
    return {
        randomString: Math.random().toString(36).substring(7),
        randomNumber: Math.floor(Math.random() * 1000),
        timestamp: new Date().toISOString()
    };
}

// Store test data in environment
const testData = generateTestData();
pm.environment.set("test_data", JSON.stringify(testData));

// Validate environment variables
const requiredVars = ['base_url', 'auth_username', 'auth_password'];
const missingVars = requiredVars.filter(varName => !pm.environment.get(varName));

if (missingVars.length > 0) {
    console.warn("Missing required environment variables:", missingVars);
}
```

### Collection-Level Test Script

```javascript
// Global test validations
pm.test("Response time is reasonable", function () {
    pm.expect(pm.response.responseTime).to.be.below(5000);
});

pm.test("No internal server errors", function () {
    pm.expect(pm.response.code).to.not.equal(500);
});

pm.test("Response has valid JSON structure", function () {
    try {
        const jsonData = pm.response.json();
        pm.expect(jsonData).to.be.an('object');
    } catch (e) {
        // Skip for file downloads or non-JSON responses
        if (!pm.response.headers.get("Content-Type")?.includes("application/octet-stream")) {
            throw e;
        }
    }
});

// Log response for debugging
console.log("Response Status:", pm.response.status);
console.log("Response Body:", pm.response.text());
```

### Data-Driven Testing Script

```javascript
// Test with multiple message variations
const testMessages = [
    "Simple test message",
    "Message with special characters: @#$%^&*()",
    "Long message: " + "Lorem ipsum ".repeat(100),
    "Message with emojis: 🚀🔥💡",
    "Code snippet: function test() { return 'hello'; }"
];

// Store for use in requests
pm.environment.set("test_messages", JSON.stringify(testMessages));
```

## Error Handling & Validation

### Error Response Validation Script

```javascript
pm.test("Error responses have proper structure", function () {
    if (pm.response.code >= 400) {
        try {
            const jsonData = pm.response.json();
            pm.expect(jsonData).to.have.property('error');
        } catch (e) {
            // Some errors might not be JSON
            pm.expect(pm.response.text()).to.exist;
        }
    }
});

pm.test("Authentication errors return 401", function () {
    if (pm.request.headers.get("Authorization") === null) {
        pm.expect(pm.response.code).to.equal(401);
    }
});

pm.test("Invalid paths return 404 or 400", function () {
    if (pm.request.url.toString().includes("/nonexistent")) {
        pm.expect([400, 404]).to.include(pm.response.code);
    }
});
```

### File Upload Validation

```javascript
pm.test("File upload validation", function () {
    if (pm.request.url.toString().includes("/upload")) {
        const jsonData = pm.response.json();
        
        if (pm.response.code === 200) {
            pm.expect(jsonData).to.have.property('filenames');
            pm.expect(jsonData.filenames).to.be.an('array');
        } else {
            pm.expect(jsonData).to.have.property('error');
        }
    }
});
```

## Performance Testing

### Load Testing Setup

```javascript
// Performance monitoring
const responseTime = pm.response.responseTime;
const endpoint = pm.request.url.getPath();

// Store performance data
const perfData = JSON.parse(pm.environment.get("performance_data") || "{}");
if (!perfData[endpoint]) {
    perfData[endpoint] = [];
}
perfData[endpoint].push({
    timestamp: new Date().toISOString(),
    responseTime: responseTime,
    status: pm.response.code
});

// Keep only last 100 entries per endpoint
if (perfData[endpoint].length > 100) {
    perfData[endpoint] = perfData[endpoint].slice(-100);
}

pm.environment.set("performance_data", JSON.stringify(perfData));

// Performance thresholds
const thresholds = {
    "/health": 500,
    "/message": 3000,
    "/upload": 5000,
    default: 2000
};

const threshold = thresholds[endpoint] || thresholds.default;

pm.test(`Response time under ${threshold}ms`, function () {
    pm.expect(responseTime).to.be.below(threshold);
});
```

### Memory Leak Detection

```javascript
// Monitor for memory leaks in long-running tests
pm.test("No memory leak indicators", function () {
    const jsonData = pm.response.json();
    
    // Check for memory-related error messages
    const memoryErrors = [
        "out of memory",
        "memory leak",
        "heap overflow",
        "stack overflow"
    ];
    
    const responseText = JSON.stringify(jsonData).toLowerCase();
    memoryErrors.forEach(error => {
        pm.expect(responseText).to.not.include(error);
    });
});
```

## CI/CD Integration

### Newman Command Line Usage

```bash
# Install Newman
npm install -g newman

# Run collection with environment
newman run "Atulya_Zero_API_Tests.postman_collection.json" \
  -e "Atulya_Zero_Environment.postman_environment.json" \
  --reporters cli,json,html \
  --reporter-html-export htmlResults.html \
  --reporter-json-export jsonResults.json

# Run with custom timeout and iterations
newman run "Atulya_Zero_API_Tests.postman_collection.json" \
  -e "Atulya_Zero_Environment.postman_environment.json" \
  --timeout-request 10000 \
  --iteration-count 5 \
  --delay-request 1000
```

### GitHub Actions Integration

```yaml
# .github/workflows/api-tests.yml
name: API Tests
on: [push, pull_request]

jobs:
  api-tests:
    runs-on: ubuntu-latest
    
    services:
      atulya-zero:
        image: atulya-zero:latest
        ports:
          - 50080:50080
        env:
          AUTH_LOGIN: ${{ secrets.TEST_USERNAME }}
          AUTH_PASSWORD: ${{ secrets.TEST_PASSWORD }}
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Install Newman
        run: npm install -g newman
      
      - name: Wait for service
        run: |
          timeout 60 bash -c 'until curl -f http://localhost:50080/health; do sleep 2; done'
      
      - name: Run API Tests
        run: |
          newman run docs/testing/api/postman_collection.json \
            -e docs/testing/api/postman_environment.json \
            --reporters cli,json \
            --reporter-json-export test-results.json
      
      - name: Upload test results
        uses: actions/upload-artifact@v2
        with:
          name: test-results
          path: test-results.json
```

### Docker Test Environment

```dockerfile
# Dockerfile.test
FROM postman/newman:alpine

COPY docs/testing/api/ /tests/
WORKDIR /tests

CMD ["run", "postman_collection.json", "-e", "postman_environment.json"]
```

## Troubleshooting

### Common Issues and Solutions

#### 1. Authentication Failures

**Issue**: 401 Unauthorized responses
**Solution**:
```javascript
// Debug auth in pre-request script
console.log("Auth Username:", pm.environment.get("auth_username"));
console.log("Auth Header:", pm.request.headers.get("Authorization"));

// Verify base64 encoding
const username = pm.environment.get("auth_username");
const password = pm.environment.get("auth_password");
const expectedAuth = btoa(username + ":" + password);
console.log("Expected Auth:", "Basic " + expectedAuth);
```

#### 2. Context ID Issues

**Issue**: Context not persisting between requests
**Solution**:
```javascript
// Ensure context ID is properly stored and used
pm.test("Store context for next request", function () {
    const jsonData = pm.response.json();
    if (jsonData.context) {
        pm.environment.set("context_id", jsonData.context);
        console.log("Stored context ID:", jsonData.context);
    }
});
```

#### 3. File Path Issues

**Issue**: File operations failing with path errors
**Solution**:
```javascript
// Validate file paths before use
pm.test("Validate file path", function () {
    const filePath = pm.environment.get("file_path");
    
    // Ensure path is not empty and doesn't contain dangerous characters
    pm.expect(filePath).to.exist;
    pm.expect(filePath).to.not.include("..");
    pm.expect(filePath).to.not.include("//");
});
```

#### 4. Network Timeouts

**Issue**: Requests timing out
**Solution**:
```javascript
// Increase timeout for specific endpoints
pm.test("Handle long-running operations", function () {
    if (pm.request.url.toString().includes("/transcribe") || 
        pm.request.url.toString().includes("/tunnel")) {
        // Allow longer timeout for these operations
        pm.expect(pm.response.responseTime).to.be.below(30000);
    }
});
```

### Debug Information Collection

```javascript
// Comprehensive debug info
console.log("=== DEBUG INFO ===");
console.log("Timestamp:", new Date().toISOString());
console.log("Request URL:", pm.request.url.toString());
console.log("Request Method:", pm.request.method);
console.log("Request Headers:", JSON.stringify(pm.request.headers.toObject()));
console.log("Request Body:", pm.request.body);
console.log("Response Status:", pm.response.status);
console.log("Response Time:", pm.response.responseTime + "ms");
console.log("Response Headers:", JSON.stringify(pm.response.headers.toObject()));
console.log("Response Body:", pm.response.text());
console.log("Environment Variables:", JSON.stringify(pm.environment.toObject()));
console.log("==================");
```

### Performance Monitoring

```javascript
// Detailed performance tracking
const perfStart = new Date().getTime();

pm.test("Track detailed performance", function () {
    const perfEnd = new Date().getTime();
    const totalTime = perfEnd - perfStart;
    const networkTime = pm.response.responseTime;
    const processingTime = totalTime - networkTime;
    
    console.log("Performance Metrics:");
    console.log("- Total Time:", totalTime + "ms");
    console.log("- Network Time:", networkTime + "ms");
    console.log("- Processing Time:", processingTime + "ms");
    console.log("- Response Size:", pm.response.size().body + " bytes");
});
```

## Best Practices

### 1. Test Organization
- Group related tests in folders
- Use descriptive names for requests
- Include both positive and negative test cases
- Test edge cases and error conditions

### 2. Data Management
- Use environment variables for dynamic data
- Clean up test data after test runs
- Use random data generation for uniqueness
- Store and reuse generated IDs

### 3. Error Handling
- Always test error responses
- Validate error message formats
- Test authentication edge cases
- Verify proper HTTP status codes

### 4. Documentation
- Document test scenarios in descriptions
- Include examples of expected responses
- Note any special setup requirements
- Keep troubleshooting notes updated

This comprehensive guide should enable thorough testing of all Atulya Zero API endpoints using Postman, with proper automation, error handling, and CI/CD integration capabilities.
