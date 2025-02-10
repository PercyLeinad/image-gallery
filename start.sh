#!/bin/bash

# Set default host and port if not provided
HOST=${HOST:-"0.0.0.0"}
PORT=${PORT:-8000}

# Navigate to backend folder
cd backend

# Activate virtual environment if exists
if [ -d "venv" ]; then
    source ~/venv/bin/activate
fi

# Run Uvicorn server
uvicorn main:app --host $HOST --port $PORT --reload
