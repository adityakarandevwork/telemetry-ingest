FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY auth ./auth
COPY src ./src
ENV PYTHONPATH=/app:/app/src TELEMETRY_HOST=0.0.0.0
RUN useradd -r app && mkdir /data && chown app /data
USER app
ENV TELEMETRY_STORE_PATH=/data/events.jsonl
EXPOSE 8080
CMD ["python", "-m", "telemetry_ingest.service"]
