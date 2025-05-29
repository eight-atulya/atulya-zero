# Atulya Zero API - Professional Postman Testing Suite

## Overview

This directory contains comprehensive Postman testing documentation and resources for professional developers working with the Atulya Zero API. The testing suite is designed for thorough API validation, integration testing, and continuous development workflows.

## Available Resources

### 📚 Documentation
- **[postman_testing_guide.md](./postman_testing_guide.md)** - Complete 900+ line developer guide covering all aspects of API testing with Postman

### 🧪 Testing Collection
- **[Atulya_Zero_API_Tests.postman_collection.json](./Atulya_Zero_API_Tests.postman_collection.json)** - Production-ready Postman collection with 34 endpoints and automated test scripts

## Quick Start for Developers

### 1. Import the Collection
```bash
# Download and import the collection file into Postman
# Or use Newman CLI for automated testing
npm install -g newman
newman run Atulya_Zero_API_Tests.postman_collection.json
```

### 2. Set Up Environment
Create a Postman environment with these essential variables:
```json
{
  "base_url": "http://localhost:50080",
  "auth_username": "your_username", 
  "auth_password": "your_password",
  "api_key": "your_api_key"
}
```

### 3. Run Tests
- **Manual Testing**: Use Postman GUI with the imported collection
- **Automated Testing**: Use Newman CLI for CI/CD integration
- **Performance Testing**: Built-in response time monitoring

## What's Included

### 🎯 34 API Endpoints Covered
- **Core Messaging** (7 endpoints): Health, messaging, async operations
- **File Management** (7 endpoints): Upload, download, processing
- **Chat & Context** (6 endpoints): Context management, chat exports
- **Settings & Config** (2 endpoints): System configuration
- **Task Scheduling** (6 endpoints): Job management and monitoring
- **Tunneling & Network** (2 endpoints): Tunnel management
- **System & Monitoring** (2 endpoints): Status and health checks
- **Additional Features** (2 endpoints): Extended functionality

### 🔧 Professional Testing Features

#### Automated Test Scripts
- ✅ Response validation
- ✅ Status code verification
- ✅ JSON schema validation
- ✅ Performance monitoring
- ✅ Data flow between requests
- ✅ Error scenario testing

#### Environment Management
- ✅ Dynamic variable generation
- ✅ Test data management
- ✅ Authentication handling
- ✅ Configuration validation

#### CI/CD Integration
- ✅ Newman CLI support
- ✅ GitHub Actions workflows
- ✅ Docker test environments
- ✅ Automated reporting

## Advanced Developer Workflows

### 1. Local Development Testing
```bash
# Start Atulya Zero locally
python run_ui.py

# Run full test suite
newman run Atulya_Zero_API_Tests.postman_collection.json \
  --environment local_env.json \
  --reporters cli,html \
  --reporter-html-export test-results.html
```

### 2. Integration Testing
```bash
# Run specific test folders
newman run Atulya_Zero_API_Tests.postman_collection.json \
  --folder "Core Messaging" \
  --environment staging_env.json
```

### 3. Performance Testing
```bash
# Run with performance monitoring
newman run Atulya_Zero_API_Tests.postman_collection.json \
  --iteration-count 10 \
  --delay-request 1000 \
  --reporters cli,json \
  --reporter-json-export performance-results.json
```

## Test Coverage Matrix

| Category | Endpoints | Auth Types | Error Cases | Performance |
|----------|-----------|------------|-------------|-------------|
| Core Messaging | 7/7 ✅ | Basic, API Key | ✅ | ✅ |
| File Management | 7/7 ✅ | Basic, API Key | ✅ | ✅ |
| Chat & Context | 6/6 ✅ | Basic, API Key | ✅ | ✅ |
| Settings | 2/2 ✅ | Basic, API Key | ✅ | ✅ |
| Task Scheduling | 6/6 ✅ | Basic, API Key | ✅ | ✅ |
| Tunneling | 2/2 ✅ | Basic, API Key | ✅ | ✅ |
| System Monitoring | 2/2 ✅ | Basic, API Key | ✅ | ✅ |
| Additional | 2/2 ✅ | Basic, API Key | ✅ | ✅ |

## Developer Best Practices

### 1. Test-Driven API Development
- Use the collection as a contract for API development
- Run tests after each code change
- Validate responses match expected schemas

### 2. Environment Separation
```bash
# Development
newman run collection.json --environment dev_env.json

# Staging  
newman run collection.json --environment staging_env.json

# Production (read-only tests)
newman run collection.json --environment prod_env.json --folder "Health Checks"
```

### 3. Continuous Integration
Add to your CI pipeline:
```yaml
# .github/workflows/api-tests.yml
- name: Run API Tests
  run: |
    newman run docs/testing/api/Atulya_Zero_API_Tests.postman_collection.json \
      --environment ci_env.json \
      --reporters cli,junit \
      --reporter-junit-export test-results.xml
```

## Troubleshooting Quick Reference

### Common Issues
1. **Connection Refused**: Verify Atulya Zero is running on expected port
2. **Auth Failures**: Check username/password in environment
3. **File Upload Issues**: Verify file paths and permissions
4. **Timeout Errors**: Increase timeout in collection settings

### Debug Mode
```bash
# Verbose Newman output
newman run collection.json --verbose

# Debug with Postman Console
# Use console.log() in test scripts for debugging
```

## Support & Contribution

### Getting Help
- Review the detailed [postman_testing_guide.md](./postman_testing_guide.md)
- Check the troubleshooting section
- Examine the collection's built-in test scripts

### Contributing
- Add new test cases for new endpoints
- Enhance error scenario coverage
- Improve automation scripts
- Update documentation with new findings

## Professional Development Tools

### Newman CLI Commands Reference
```bash
# Basic run
newman run collection.json

# With environment
newman run collection.json -e environment.json

# Specific folder
newman run collection.json --folder "Folder Name"

# Multiple iterations
newman run collection.json -n 10

# Custom timeout
newman run collection.json --timeout-request 30000

# Export results
newman run collection.json --reporters html,json
```

### Docker Testing Environment
```dockerfile
# Dockerfile for testing environment
FROM node:alpine
RUN npm install -g newman
COPY . /tests
WORKDIR /tests
CMD ["newman", "run", "Atulya_Zero_API_Tests.postman_collection.json"]
```

This comprehensive testing suite provides professional developers with everything needed for thorough API testing, validation, and integration workflows with the Atulya Zero project.
