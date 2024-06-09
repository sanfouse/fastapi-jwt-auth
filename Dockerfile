FROM python:3.12.2-slim
LABEL authors="sanfit"

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . /app

RUN apt-get update && \
    apt-get install -y openssl && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root

RUN mkdir -p certs && \
    openssl genrsa -out certs/jwt-private.pem 2048 && \
    openssl rsa -in certs/jwt-private.pem -outform PEM -pubout -out certs/jwt-public.pem

EXPOSE 8000