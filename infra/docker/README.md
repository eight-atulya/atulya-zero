# Docker Infrastructure

This folder references the main Docker deployment files located in `../../docker/run/`.

## Quick Start (Windows)

- To build the Docker image:
  ```
  build.bat
  ```
- To run the system:
  ```
  up.bat
  ```

These scripts will use the main Dockerfile and docker-compose.yml from the `../../docker/run/` directory.

## Manual Usage

- Build:
  ```
  docker build -t atulya-zero-run:local --build-arg BRANCH=development --no-cache -f ../../docker/run/Dockerfile ../../
  ```
- Run:
  ```
  docker-compose -f ../../docker/run/docker-compose.yml up --build
  ```

Refer to the main project README or `../../docker/run/README.md` for more details.
