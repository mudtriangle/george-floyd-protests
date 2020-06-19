FROM python:3.8-slim-buster

RUN apt-get -y update && apt-get install -y python3-pip

WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r /app/requirements.txt

CMD ["/bin/sh", "-c", "while true; do echo hello world; sleep 1; done"]
