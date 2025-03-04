#! /usr/bin/env bash

set -e
set -x

# Sync dependencies
echo "Running uv sync..."
uv sync

# Run Alembic migrations (if alembic directory exists)
if [ -d "/app/alembic" ]; then
    echo "Running Alembic migrations..."
    alembic upgrade head
else
    echo "Alembic directory not found. Skipping migrations."
fi
