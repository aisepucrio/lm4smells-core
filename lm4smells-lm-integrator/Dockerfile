FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src

WORKDIR /app

COPY src/app/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /app/src/app

EXPOSE 8001

CMD ["python", "main.py"]