FROM python:3.12-slim

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set working directory inside container
WORKDIR /app

# Copy and install dependencies first (better Docker layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your app code
COPY app.py .

# Expose the port Flask runs on
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]