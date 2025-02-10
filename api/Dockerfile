FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y curl \
    && pip install fastapi uvicorn redis kubernetes

CMD ["uvicorn", "proxy_manager:app", "--host", "127.0.0.1", "--port", "5003"]
