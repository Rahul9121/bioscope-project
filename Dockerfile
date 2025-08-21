# Use Python 3.9 slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy minimal requirements first (for faster builds)
COPY requirements-minimal.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the minimal app
COPY minimal_app.py .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production

# Expose port
EXPOSE 5000

# Run the minimal application
CMD ["python", "minimal_app.py"]
