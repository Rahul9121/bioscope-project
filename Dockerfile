# Use Python 3.9 slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies for PostgreSQL
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create requirements.txt with database support
RUN echo "Flask==2.2.3\nFlask-Cors==3.0.10\nFlask-Session==0.4.0\npsycopg2-binary==2.9.7\nWerkzeug==2.2.3\ngunicorn==21.2.0\nrequests==2.31.0" > requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application
COPY minimal_app.py .

# Create flask_session directory
RUN mkdir -p flask_session

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "minimal_app.py"]
