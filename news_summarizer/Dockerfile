FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for pyttsx3
RUN apt-get update && apt-get install -y \
    espeak \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set environment variables
ENV NEWS_API_KEY=""
ENV ANTHROPIC_API_KEY=""

# Run the application
CMD ["python", "main.py"]