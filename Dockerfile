# Use official lightweight Python image
FROM python:3.12-slim

# Set environment variables for Google Cloud Run
ENV PYTHONUNBUFFERED=1 \
    PORT=8080 \
    APP_HOME=/app

WORKDIR $APP_HOME

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project source code
COPY . .

# Expose standard Cloud Run port
EXPOSE 8080

# Execute FastAPI application
CMD exec uvicorn app:app --host 0.0.0.0 --port ${PORT}
