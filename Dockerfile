FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000 \
    DATABASE_PATH=/data/aceest_fitness.db

WORKDIR /app

RUN addgroup --system aceest \
    && adduser --system --ingroup aceest aceest \
    && mkdir -p /data \
    && chown -R aceest:aceest /app /data

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY --chown=aceest:aceest app.py .
COPY --chown=aceest:aceest templates ./templates

USER aceest

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/health', timeout=3)"

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--threads", "2", "--timeout", "30", "app:app"]
