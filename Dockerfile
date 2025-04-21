# Stage 1 of 2
FROM python:3.12-slim AS builder
# Install build dependencies for buiilding packages
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

# Stage 2 of 2
FROM python:3.12-slim

# Install only runtime dependencies (for mysqlclient)
RUN apt-get update && apt-get install -y \
default-libmysqlclient-dev \
&& rm -rf /var/lib/apt/lists/*

COPY --from=builder /install /usr/local

WORKDIR /app
COPY . .
