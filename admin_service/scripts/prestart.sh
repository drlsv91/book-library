#! /usr/bin/env bash

set -e
set -x

# Let the DB start
echo "Running test sync..."
python app/prestart.py

# Run migrations
echo "Running migration"
alembic upgrade head
