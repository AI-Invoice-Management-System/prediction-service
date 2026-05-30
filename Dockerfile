FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --default-timeout=100 --upgrade pip setuptools wheel && \
    pip install --no-cache-dir --default-timeout=100 -r requirements.txt

COPY . .

EXPOSE 9779

ENV PYTHONPATH=/app

CMD ["python", "main.py"]
