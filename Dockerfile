# RODA AI FastAPI Dockerfile 🧠⚙️
FROM python:3.11-slim AS base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
 && pip install --no-cache-dir -r requirements.txt \
 && apt-get remove -y build-essential gcc \
 && apt-get autoremove -y && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Copy source code
COPY . .

# Use production-grade server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
