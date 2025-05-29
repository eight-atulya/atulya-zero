#!/bin/bash

# Atulya Zero API Test Runner
# Professional testing script for developers

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COLLECTION_FILE="$SCRIPT_DIR/Atulya_Zero_API_Tests.postman_collection.json"
ENV_FILE="$SCRIPT_DIR/atulya_zero_dev_environment.postman_environment.json"
REPORTS_DIR="$SCRIPT_DIR/reports"

# Ensure reports directory exists
mkdir -p "$REPORTS_DIR"

# Print banner
print_banner() {
    echo -e "${BLUE}"
    echo "╔══════════════════════════════════════════════════════════════════╗"
    echo "║                    Atulya Zero API Test Runner                  ║"
    echo "║                Professional Testing Script v1.0                 ║"
    echo "╚══════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Print usage
print_usage() {
    echo -e "${YELLOW}Usage: $0 [OPTION]${NC}"
    echo ""
    echo "Options:"
    echo "  dev         Run development tests (default)"
    echo "  smoke       Run smoke tests (quick validation)"
    echo "  full        Run all tests with detailed reporting"
    echo "  performance Run performance tests (10 iterations)"
    echo "  security    Run security-focused tests"
    echo "  folder      Run specific folder tests"
    echo "  docker      Run tests in Docker container"
    echo "  ci          Run CI/CD optimized tests"
    echo "  help        Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 dev                    # Run development tests"
    echo "  $0 smoke                  # Quick smoke tests"
    echo "  $0 folder 'Core Messaging' # Test specific folder"
    echo "  $0 performance            # Performance testing"
}

# Check prerequisites
check_prerequisites() {
    echo -e "${BLUE}Checking prerequisites...${NC}"
    
    # Check if Newman is installed
    if ! command -v newman &> /dev/null; then
        echo -e "${RED}❌ Newman CLI not found. Installing...${NC}"
        npm install -g newman
        if [ $? -ne 0 ]; then
            echo -e "${RED}❌ Failed to install Newman. Please install manually: npm install -g newman${NC}"
            exit 1
        fi
    else
        echo -e "${GREEN}✅ Newman CLI found${NC}"
    fi
    
    # Check if collection file exists
    if [ ! -f "$COLLECTION_FILE" ]; then
        echo -e "${RED}❌ Collection file not found: $COLLECTION_FILE${NC}"
        exit 1
    else
        echo -e "${GREEN}✅ Collection file found${NC}"
    fi
    
    # Check if environment file exists
    if [ ! -f "$ENV_FILE" ]; then
        echo -e "${YELLOW}⚠️  Environment file not found: $ENV_FILE${NC}"
        echo -e "${YELLOW}Creating default environment file...${NC}"
        create_default_environment
    else
        echo -e "${GREEN}✅ Environment file found${NC}"
    fi
}

# Create default environment file
create_default_environment() {
    cat > "$ENV_FILE" << 'EOF'
{
  "id": "atulya-zero-dev",
  "name": "Atulya Zero - Development",
  "values": [
    {"key": "base_url", "value": "http://localhost:50080", "enabled": true},
    {"key": "auth_username", "value": "your_username", "enabled": true},
    {"key": "auth_password", "value": "your_password", "enabled": true},
    {"key": "api_key", "value": "your_api_key", "enabled": true},
    {"key": "timezone", "value": "UTC", "enabled": true}
  ]
}
EOF
    echo -e "${GREEN}✅ Default environment file created${NC}"
    echo -e "${YELLOW}⚠️  Please update the environment file with your actual credentials${NC}"
}

# Run development tests
run_dev_tests() {
    echo -e "${BLUE}Running development tests...${NC}"
    newman run "$COLLECTION_FILE" \
        -e "$ENV_FILE" \
        --reporters cli,html \
        --reporter-html-export "$REPORTS_DIR/dev-results.html" \
        --timeout-request 30000 \
        --delay-request 100
}

# Run smoke tests
run_smoke_tests() {
    echo -e "${BLUE}Running smoke tests...${NC}"
    newman run "$COLLECTION_FILE" \
        -e "$ENV_FILE" \
        --folder "Core Messaging" \
        --folder "System & Monitoring" \
        --reporters cli \
        --timeout-request 15000 \
        --bail
}

# Run full test suite
run_full_tests() {
    echo -e "${BLUE}Running full test suite...${NC}"
    newman run "$COLLECTION_FILE" \
        -e "$ENV_FILE" \
        --reporters cli,html,json \
        --reporter-html-export "$REPORTS_DIR/full-results.html" \
        --reporter-json-export "$REPORTS_DIR/full-results.json" \
        --timeout-request 45000 \
        --delay-request 200
}

# Run performance tests
run_performance_tests() {
    echo -e "${BLUE}Running performance tests (10 iterations)...${NC}"
    newman run "$COLLECTION_FILE" \
        -e "$ENV_FILE" \
        -n 10 \
        --reporters cli,json \
        --reporter-json-export "$REPORTS_DIR/performance-results.json" \
        --timeout-request 60000 \
        --delay-request 1000
}

# Run security tests
run_security_tests() {
    echo -e "${BLUE}Running security-focused tests...${NC}"
    newman run "$COLLECTION_FILE" \
        -e "$ENV_FILE" \
        --folder "Authentication Tests" \
        --folder "Error Scenarios" \
        --reporters cli,html \
        --reporter-html-export "$REPORTS_DIR/security-results.html" \
        --timeout-request 30000
}

# Run specific folder tests
run_folder_tests() {
    if [ -z "$2" ]; then
        echo -e "${RED}❌ Please specify a folder name${NC}"
        echo "Available folders:"
        echo "  - Core Messaging"
        echo "  - File Management" 
        echo "  - Chat & Context Management"
        echo "  - Settings & Configuration"
        echo "  - Task Scheduling"
        echo "  - Tunneling & Network"
        echo "  - System & Monitoring"
        echo "  - Authentication Tests"
        echo "  - Error Scenarios"
        exit 1
    fi
    
    FOLDER_NAME="$2"
    echo -e "${BLUE}Running tests for folder: $FOLDER_NAME${NC}"
    newman run "$COLLECTION_FILE" \
        -e "$ENV_FILE" \
        --folder "$FOLDER_NAME" \
        --reporters cli,html \
        --reporter-html-export "$REPORTS_DIR/folder-${FOLDER_NAME// /-}-results.html" \
        --timeout-request 30000
}

# Run tests in Docker
run_docker_tests() {
    echo -e "${BLUE}Running tests in Docker container...${NC}"
    
    # Check if Docker is available
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}❌ Docker not found. Please install Docker first.${NC}"
        exit 1
    fi
    
    docker run --rm \
        -v "$SCRIPT_DIR:/workspace" \
        -w /workspace \
        postman/newman:alpine \
        run Atulya_Zero_API_Tests.postman_collection.json \
        -e atulya_zero_dev_environment.postman_environment.json \
        --reporters cli,html \
        --reporter-html-export reports/docker-results.html
}

# Run CI/CD optimized tests
run_ci_tests() {
    echo -e "${BLUE}Running CI/CD optimized tests...${NC}"
    newman run "$COLLECTION_FILE" \
        -e "$ENV_FILE" \
        --reporters cli,junit \
        --reporter-junit-export "$REPORTS_DIR/junit-results.xml" \
        --timeout-request 30000 \
        --bail \
        --color off
}

# Print test results summary
print_results_summary() {
    echo -e "${GREEN}"
    echo "╔══════════════════════════════════════════════════════════════════╗"
    echo "║                        Test Results Summary                      ║"
    echo "╚══════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    echo -e "${BLUE}📊 Test Reports Generated:${NC}"
    ls -la "$REPORTS_DIR"/*.html 2>/dev/null | awk '{print "   📄 " $9}' || echo "   No HTML reports generated"
    ls -la "$REPORTS_DIR"/*.json 2>/dev/null | awk '{print "   📄 " $9}' || echo "   No JSON reports generated"
    ls -la "$REPORTS_DIR"/*.xml 2>/dev/null | awk '{print "   📄 " $9}' || echo "   No XML reports generated"
    
    echo ""
    echo -e "${BLUE}🌐 View HTML Reports:${NC}"
    for html_file in "$REPORTS_DIR"/*.html; do
        if [ -f "$html_file" ]; then
            echo "   file://$html_file"
        fi
    done
}

# Main execution
main() {
    print_banner
    
    case "${1:-dev}" in
        "dev")
            check_prerequisites
            run_dev_tests
            ;;
        "smoke")
            check_prerequisites
            run_smoke_tests
            ;;
        "full")
            check_prerequisites
            run_full_tests
            ;;
        "performance")
            check_prerequisites
            run_performance_tests
            ;;
        "security")
            check_prerequisites
            run_security_tests
            ;;
        "folder")
            check_prerequisites
            run_folder_tests "$@"
            ;;
        "docker")
            run_docker_tests
            ;;
        "ci")
            check_prerequisites
            run_ci_tests
            ;;
        "help"|"-h"|"--help")
            print_usage
            exit 0
            ;;
        *)
            echo -e "${RED}❌ Unknown option: $1${NC}"
            print_usage
            exit 1
            ;;
    esac
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Tests completed successfully!${NC}"
        print_results_summary
    else
        echo -e "${RED}❌ Tests failed!${NC}"
        exit 1
    fi
}

# Run main function with all arguments
main "$@"
