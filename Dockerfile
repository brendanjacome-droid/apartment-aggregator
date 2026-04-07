FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DATABASE_URL="sqlite:////tmp/apartment_aggregator.db"

# Install Node.js 20 for building the frontend
RUN apt-get update && apt-get install -y curl \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies first (for layer caching)
COPY backend/requirements.txt backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

# Install Node dependencies
COPY frontend/package.json frontend/package-lock.json* frontend/
RUN cd frontend && npm install

# Copy all source files
COPY backend/ backend/
COPY frontend/ frontend/

# Build the React frontend and copy to backend/static
RUN cd frontend && npm run build \
    && mkdir -p ../backend/static \
    && cp -r dist/. ../backend/static/

# Remove frontend source to slim the image
RUN rm -rf frontend node_modules

WORKDIR /app/backend

EXPOSE 8000

# Use shell form so $PORT is expanded at runtime by Railway
CMD ["sh", "-c", "python -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
