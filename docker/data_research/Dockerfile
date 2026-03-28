FROM python:3.11-slim

WORKDIR /app

COPY docker/data_research/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY data ./data
COPY reports ./reports

CMD ["python", "src/data_research.py"]