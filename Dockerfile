# Deprecated: Use Dockerfile.backend and Dockerfile.frontend instead
FROM python:latest
LABEL authors="Marius"

WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python3", "main.py"]