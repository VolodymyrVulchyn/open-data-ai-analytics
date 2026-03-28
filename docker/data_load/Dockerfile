FROM python:3.11-slim

WORKDIR /app

COPY docker/data_load/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY data ./data

CMD ["python", "src/data_load.py"]