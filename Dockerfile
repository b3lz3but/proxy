# Using the slim version of the Python 3.9 image to reduce the image size and improve build times
FROM python:3.9-slim

WORKDIR /app

COPY ./ /app

RUN apt-get update && apt-get install -y --no-install-recommends \
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
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

CMD ["python", "proxy_manager.py"]
