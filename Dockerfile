FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y netcat-openbsd && apt-get clean

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
WORKDIR /app/src
COPY src /app/src
COPY .env /app/.env
