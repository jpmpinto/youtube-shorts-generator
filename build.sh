#!/bin/bash

# Install ffmpeg
apt-get update && apt-get install -y ffmpeg

# Continue with Vercel's default build process for Python
# This will install dependencies from requirements.txt
python3 -m pip install -r backend/requirements.txt

# Build frontend (if not already built and copied)
# Since we already built frontend and copied to backend/src/static, this might not be strictly necessary
# but it's good practice to ensure it's there if you change your workflow
# cd frontend && pnpm install && pnpm run build && cp -r dist/* ../backend/src/static/

# Ensure the Flask app is ready
# This might not be needed as Vercel's @vercel/python builder handles it
