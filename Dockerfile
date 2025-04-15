FROM python:3.12-slim

# Install required system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp
RUN pip install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /app
