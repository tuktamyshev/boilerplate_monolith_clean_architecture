#!/bin/bash
set -e

echo "🔄 Startup migrations..."
alembic upgrade head

cd /app/src

echo "🚀 Startup API server..."
gunicorn -c ../gunicorn.conf.py main.web:create_app
