#!/bin/bash

# activate venv
. "/ins/setup_venv.sh" "$@"

# install playwright if not installed
pip install playwright

# install chromium with dependencies
playwright install chromium

# Ensure the Playwright cache directory exists and contains Chromium
CACHE_DIR="$HOME/.cache/ms-playwright/chromium"
if [ ! -e "$CACHE_DIR/chrome-linux/headless_shell" ]; then
    echo "Chromium binary not found. Reinstalling..."
    playwright install chromium
else
    echo "Chromium binary is already installed."
fi