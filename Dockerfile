# Step 1: Use lightweight base image
FROM python:3.11-slim AS base

# Step 2: Set work directory
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

# Step 6: Expose port
EXPOSE 5000

# Step 7: Run the app (modify if needed)
CMD ["python", "run.py"]
