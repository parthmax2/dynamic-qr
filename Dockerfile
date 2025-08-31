FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Create static directory and give permissions
RUN mkdir -p /app/static && chmod -R 777 /app/static

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Expose the default port Hugging Face Spaces expects
EXPOSE 7860

# Run the FastAPI app with uvicorn
# Replace "app:app" with the correct filename:app_name if your entrypoint differs
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
