FROM python:3.6-slim

WORKDIR /app

RUN apt-get update -y && \
    apt-get install -y python-pip

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

ENV FLASK_APP main_site.py
ENV FLASK_ENV development
ENV FLASK_RUN_HOST 0.0.0.0
ENV PYTHONUNBUFFERED TRUE

CMD ["flask", "run"]