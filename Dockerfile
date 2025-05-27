# Stage 1: Build frontend
FROM node:22-alpine AS frontend-builder

WORKDIR /app/fe

# Install pnpm
RUN corepack enable && corepack prepare pnpm@latest --activate

COPY ./fe ./

# Install dependencies and build
RUN pnpm install && pnpm build

# Use an official Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# build fe
# RUN cd fe && 

# Install system dependencies
RUN apt-get update && apt-get install -y \
 gcc \
 default-libmysqlclient-dev \
 libssl-dev \
 build-essential \
 pkg-config \
 && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# copy fe build
COPY --from=frontend-builder /app/fe/dist ./app/static

# Expose the port FastAPI will run on
EXPOSE 8000

# Run the application
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8000"]

