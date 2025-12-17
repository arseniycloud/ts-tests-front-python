# Use the official Playwright image from the Docker Hub
FROM mcr.microsoft.com/playwright/python:v1.56.0

RUN apt-get update && \
    apt-get install -y --no-install-recommends make jq && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    CI=true \
    HEADLESS=true

# Set work directory
WORKDIR /app

# Copy and install Python dependencies (cached)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    playwright install chromium firefox webkit

# Add dummy build arg to invalidate only this part
ARG CACHE_BREAKER=default

# Copy application code (always rebuilt due to CACHE_BREAKER)
COPY . .

# Copy and prepare entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//' /entrypoint.sh \
 && chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
