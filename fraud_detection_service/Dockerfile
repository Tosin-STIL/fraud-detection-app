FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

# Add timeout + retries
RUN pip install --no-cache-dir --default-timeout=100 -r requirements.txt

COPY app.py .
COPY model.pkl .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
