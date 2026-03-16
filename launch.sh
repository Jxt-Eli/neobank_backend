#!/bin/bash

# 1. Go to the dir of this script
cd "$(dirname "$0")"

# 2. Activate the venv (for dev stage)
# source myenv/bin/activate

# 3. Print something to show its not failed at this stage
echo "Starting Backend.........⏳"

# 4. Run FastAPI with uvicorn
exec uvicorn main:app --host 0.0.0.0 --port 5000 --reload
