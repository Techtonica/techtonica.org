FROM python:3.6-slim

WORKDIR /app

RUN apt-get update -y && \
    apt-get install -y python-pip

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt