FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y \
    squid \
    apache2-utils \
    haproxy \
    tinyproxy \
    fail2ban \
    && pip install \
    flask \
    paramiko \
    inquirer \
    tabulate \
    psutil \
    flask_cors \
    pandas \
    matplotlib \
    kubernetes \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

CMD ["python", "proxy_manager.py"]
