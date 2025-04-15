FROM python:3.13

COPY requirements.txt /tmp
RUN pip install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /app
