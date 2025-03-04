#! /usr/bin/env bash

set -e
set -x

# sync
uv sync

# Run migrations
alembic upgrade head

