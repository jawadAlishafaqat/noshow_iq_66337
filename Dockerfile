# ---------- builder stage ----------
FROM python:3.11-slim AS builder
WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt && \
    find /root/.local -type f -name "*.py[co]" -delete && \
    find /root/.local -type d -name "__pycache__" -delete && \
    find /root/.local -type f -name "*.dist-info/RECORD" -delete && \
    find /root/.local -type f -name "*.dist-info/*.txt" -delete && \
    find /root/.local -type f -name "*.dist-info/top_level.txt" -delete

# ---------- runtime stage ----------
FROM python:3.11-slim

RUN useradd --create-home --shell /bin/bash app && \
    apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home/app

COPY --from=builder /root/.local /home/app/.local
ENV PATH=/home/app/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

COPY --chown=app:app noshow_iq/ ./noshow_iq/
COPY --chown=app:app models/ ./models/

USER app
EXPOSE 7860
CMD ["uvicorn", "noshow_iq.api:app", "--host", "0.0.0.0", "--port", "7860"]