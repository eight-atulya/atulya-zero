@echo off
REM Run the system using the main docker-compose.yml
cd ..\..\docker\run
if exist docker-compose.yml (
    docker-compose -f docker-compose.yml up --build
) else (
    echo docker-compose.yml not found in docker/run
)
cd ..\..\infra\docker
