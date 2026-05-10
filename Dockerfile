# Stage: base image 
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements first (Docker layer cache: only re-installs if this file changes)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Tell Docker this container listens on port 5000
EXPOSE 5000

# Start the Flask app
CMD ["python", "app.py"]
