FROM python:3.11-slim

WORKDIR /app

COPY docker/web/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY web ./web

WORKDIR /app/web

CMD ["python", "app.py"]