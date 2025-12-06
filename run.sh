#!/bin/bash
# run.sh - Start Celery framework

set -euo pipefail

VENV_DIR="venv"

# Activate venv
if [ -f "$VENV_DIR/bin/activate" ]; then
    ACTIVATE_PATH="$VENV_DIR/bin/activate"
elif [ -f "$VENV_DIR/Scripts/activate" ]; then
    ACTIVATE_PATH="$VENV_DIR/Scripts/activate"
else
    echo "ERROR: Could not find virtual environment activation script."
    exit 1
fi

source "$ACTIVATE_PATH"

# Optional Redis check
if command -v redis-cli &> /dev/null; then
    if ! redis-cli ping &> /dev/null; then
        echo "Warning: Redis is not running."
    else
        echo "Redis is running."
    fi
else
    echo "Warning: redis-cli not found."
fi

# Start Celery
echo "Starting Celery worker..."
celery -A src.celery_app worker --loglevel=info
