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
WORKDIR /

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
COPY /api /api
COPY /configs /configs
COPY /db /db
COPY /dto /dto
COPY /metadata /metadata
COPY /models /models
COPY /modules /modules
COPY /repositories /repositories
COPY /services /services
COPY /utils /utils
COPY main.py /main.py
COPY __init__.py /__init__.py
COPY .env.dev /.env.dev
COPY alembic.ini /alembic.ini

# copy fe build
COPY --from=frontend-builder /app/fe/dist /static

ENV ENV="DEV"

# Expose the port FastAPI will run on
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--env-file", ".env.dev", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]

