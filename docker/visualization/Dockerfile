FROM python:3.11-slim

WORKDIR /app

COPY docker/visualization/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY data ./data
COPY plots ./plots

CMD ["python", "src/visualization.py"]