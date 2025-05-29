@echo off
REM Atulya Zero API Test Runner for Windows
REM Professional testing script for developers

setlocal enabledelayedexpansion

REM Configuration
set SCRIPT_DIR=%~dp0
set COLLECTION_FILE=%SCRIPT_DIR%Atulya_Zero_API_Tests.postman_collection.json
set ENV_FILE=%SCRIPT_DIR%atulya_zero_dev_environment.postman_environment.json
set REPORTS_DIR=%SCRIPT_DIR%reports

REM Ensure reports directory exists
if not exist "%REPORTS_DIR%" mkdir "%REPORTS_DIR%"

REM Print banner
echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                    Atulya Zero API Test Runner                  ║
echo ║                Professional Testing Script v1.0                 ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.

REM Check command line argument
if "%1"=="" goto dev_tests
if "%1"=="help" goto show_help
if "%1"=="dev" goto dev_tests
if "%1"=="smoke" goto smoke_tests
if "%1"=="full" goto full_tests
if "%1"=="performance" goto performance_tests
if "%1"=="security" goto security_tests
if "%1"=="ci" goto ci_tests
goto show_help

:show_help
echo Usage: %0 [OPTION]
echo.
echo Options:
echo   dev         Run development tests (default)
echo   smoke       Run smoke tests (quick validation)
echo   full        Run all tests with detailed reporting
echo   performance Run performance tests (10 iterations)
echo   security    Run security-focused tests
echo   ci          Run CI/CD optimized tests
echo   help        Show this help message
echo.
echo Examples:
echo   %0 dev                    # Run development tests
echo   %0 smoke                  # Quick smoke tests
echo   %0 performance            # Performance testing
goto end

:check_prerequisites
echo Checking prerequisites...

REM Check if Newman is installed
where newman >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Newman CLI not found. Installing...
    npm install -g newman
    if !errorlevel! neq 0 (
        echo ❌ Failed to install Newman. Please install manually: npm install -g newman
        exit /b 1
    )
) else (
    echo ✅ Newman CLI found
)

REM Check if collection file exists
if not exist "%COLLECTION_FILE%" (
    echo ❌ Collection file not found: %COLLECTION_FILE%
    exit /b 1
) else (
    echo ✅ Collection file found
)

REM Check if environment file exists
if not exist "%ENV_FILE%" (
    echo ⚠️  Environment file not found: %ENV_FILE%
    echo Creating default environment file...
    call :create_default_environment
) else (
    echo ✅ Environment file found
)
goto :eof

:create_default_environment
(
echo {
echo   "id": "atulya-zero-dev",
echo   "name": "Atulya Zero - Development",
echo   "values": [
echo     {"key": "base_url", "value": "http://localhost:50080", "enabled": true},
echo     {"key": "auth_username", "value": "your_username", "enabled": true},
echo     {"key": "auth_password", "value": "your_password", "enabled": true},
echo     {"key": "api_key", "value": "your_api_key", "enabled": true},
echo     {"key": "timezone", "value": "UTC", "enabled": true}
echo   ]
echo }
) > "%ENV_FILE%"
echo ✅ Default environment file created
echo ⚠️  Please update the environment file with your actual credentials
goto :eof

:dev_tests
call :check_prerequisites
if %errorlevel% neq 0 exit /b %errorlevel%

echo Running development tests...
newman run "%COLLECTION_FILE%" ^
    -e "%ENV_FILE%" ^
    --reporters cli,html ^
    --reporter-html-export "%REPORTS_DIR%\dev-results.html" ^
    --timeout-request 30000 ^
    --delay-request 100
goto print_results

:smoke_tests
call :check_prerequisites
if %errorlevel% neq 0 exit /b %errorlevel%

echo Running smoke tests...
newman run "%COLLECTION_FILE%" ^
    -e "%ENV_FILE%" ^
    --folder "Core Messaging" ^
    --folder "System & Monitoring" ^
    --reporters cli ^
    --timeout-request 15000 ^
    --bail
goto print_results

:full_tests
call :check_prerequisites
if %errorlevel% neq 0 exit /b %errorlevel%

echo Running full test suite...
newman run "%COLLECTION_FILE%" ^
    -e "%ENV_FILE%" ^
    --reporters cli,html,json ^
    --reporter-html-export "%REPORTS_DIR%\full-results.html" ^
    --reporter-json-export "%REPORTS_DIR%\full-results.json" ^
    --timeout-request 45000 ^
    --delay-request 200
goto print_results

:performance_tests
call :check_prerequisites
if %errorlevel% neq 0 exit /b %errorlevel%

echo Running performance tests (10 iterations)...
newman run "%COLLECTION_FILE%" ^
    -e "%ENV_FILE%" ^
    -n 10 ^
    --reporters cli,json ^
    --reporter-json-export "%REPORTS_DIR%\performance-results.json" ^
    --timeout-request 60000 ^
    --delay-request 1000
goto print_results

:security_tests
call :check_prerequisites
if %errorlevel% neq 0 exit /b %errorlevel%

echo Running security-focused tests...
newman run "%COLLECTION_FILE%" ^
    -e "%ENV_FILE%" ^
    --folder "Authentication Tests" ^
    --folder "Error Scenarios" ^
    --reporters cli,html ^
    --reporter-html-export "%REPORTS_DIR%\security-results.html" ^
    --timeout-request 30000
goto print_results

:ci_tests
call :check_prerequisites
if %errorlevel% neq 0 exit /b %errorlevel%

echo Running CI/CD optimized tests...
newman run "%COLLECTION_FILE%" ^
    -e "%ENV_FILE%" ^
    --reporters cli,junit ^
    --reporter-junit-export "%REPORTS_DIR%\junit-results.xml" ^
    --timeout-request 30000 ^
    --bail ^
    --color off
goto print_results

:print_results
if %errorlevel% equ 0 (
    echo.
    echo ✅ Tests completed successfully!
    echo.
    echo ╔══════════════════════════════════════════════════════════════════╗
    echo ║                        Test Results Summary                      ║
    echo ╚══════════════════════════════════════════════════════════════════╝
    echo.
    echo 📊 Test Reports Generated:
    if exist "%REPORTS_DIR%\*.html" (
        for %%f in ("%REPORTS_DIR%\*.html") do echo    📄 %%f
    ) else (
        echo    No HTML reports generated
    )
    if exist "%REPORTS_DIR%\*.json" (
        for %%f in ("%REPORTS_DIR%\*.json") do echo    📄 %%f
    ) else (
        echo    No JSON reports generated
    )
    if exist "%REPORTS_DIR%\*.xml" (
        for %%f in ("%REPORTS_DIR%\*.xml") do echo    📄 %%f
    ) else (
        echo    No XML reports generated
    )
    echo.
    echo 🌐 View HTML Reports:
    for %%f in ("%REPORTS_DIR%\*.html") do echo    file:///%%f
) else (
    echo ❌ Tests failed!
    exit /b 1
)

:end
echo.
pause
