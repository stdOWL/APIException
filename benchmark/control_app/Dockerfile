FROM python:3.11-slim

WORKDIR /app

# Gereksinimleri yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyalarını kopyala
COPY ./control_app /app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
