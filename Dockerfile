FROM python:3.6.8-slim

COPY requirements.txt /tmp
RUN pip install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /app
