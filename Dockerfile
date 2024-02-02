# syntax=docker/dockerfile:1

FROM python:3.11-slim

WORKDIR /app
COPY    . /app

RUN pip install --no-cache-dir -U pip setuptools && \
    pip install -r requirements.txt

EXPOSE 5000

CMD ["python3", "main.py"]