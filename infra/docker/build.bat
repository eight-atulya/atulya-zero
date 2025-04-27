@echo off
REM Build the Docker image using the main Dockerfile with branch argument and no cache
cd ..\..\docker\run
if exist Dockerfile (
    docker build -t atulya-zero-run:local --build-arg BRANCH=development --no-cache -f Dockerfile ..\..
) else (
    echo Dockerfile not found in docker/run
)
cd ..\..\infra\docker
