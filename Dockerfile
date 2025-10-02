# 1. Use an official Python runtime as a parent image
FROM python:3.9-slim

# 2. Set the working directory in the container
WORKDIR /app

# 3. Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy the rest of your application code into the container
COPY . .

# 5. Expose the port that the app will run on
# Cloud Run expects the container to listen on the port defined by the PORT environment variable.
# 8080 is a common default.
EXPOSE 8080

# 6. Define the command to run your application
# Use gunicorn for a production-ready server. The PORT variable is automatically set by Cloud Run.
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8080"]