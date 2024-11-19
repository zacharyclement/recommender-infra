# Use a Python base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install required Python libraries
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the FastAPI port
EXPOSE 8080

# Start the FastAPI app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
