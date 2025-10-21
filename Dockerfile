# Step 1: Use lightweight base image
FROM python:3.11-slim AS base

# Step 2: Set working directory
WORKDIR /app

# Step 3: Install system dependencies (if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Step 4: Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy app code
COPY . .

# Step 6: Expose the port Gunicorn will listen on
EXPOSE 5000

# Step 7: Use Gunicorn to serve the Flask app
# -w: number of worker processes (use 2-4 for small instances)
# -b: bind address and port
# app:app = module_name:Flask_instance_name
CMD ["gunicorn", "-w", "3", "-b", "0.0.0.0:5000", "run:app"]

