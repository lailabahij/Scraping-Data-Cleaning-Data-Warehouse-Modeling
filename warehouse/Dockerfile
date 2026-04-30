# ======================
# WAREHOUSE SERVICE
# ======================
FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt || true

RUN mkdir -p /app/logs

CMD ["python", "main.py"]