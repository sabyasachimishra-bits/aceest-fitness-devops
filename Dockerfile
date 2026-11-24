# syntax=docker/dockerfile:1

FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt


# -----------------------------
# Test stage
# -----------------------------
FROM base AS test

COPY requirements-dev.txt .

RUN pip install --no-cache-dir -r requirements-dev.txt

COPY app.py .
COPY templates ./templates
COPY tests ./tests

CMD ["python", "-m", "pytest", "-v"]


# -----------------------------
# Runtime stage
# -----------------------------
FROM base AS runtime

RUN addgroup --system appgroup \
    && adduser --system --ingroup appgroup appuser

COPY --chown=appuser:appgroup app.py .
COPY --chown=appuser:appgroup templates ./templates

USER appuser

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
