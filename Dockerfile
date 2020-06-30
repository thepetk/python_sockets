FROM python:3.6.8-alpine3.9

LABEL maintainer="Theofanis Petkos <thepetk@gmail.com>"

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

# install dependencies
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev g++ libffi-dev make libpq

# copy source code
COPY . /app

# install ingest requirements
RUN pip3 install --no-cache-dir -r /app/requirements.txt

# set as workdir app directory
WORKDIR /app

# run sockets with uwsgi. Here you can use an entrypoint.sh script.
ENTRYPOINT ["uwsgi", "--http", "0.0.0.0:8000", "--module", "app:app", "--processes", "1", "--threads", "8"]