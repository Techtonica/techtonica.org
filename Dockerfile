FROM debian:buster-slim

WORKDIR /app

COPY . ./

RUN apt-get update -y && \
    apt-get install -y python-pip

RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ]

CMD [ "main_site.py" ]