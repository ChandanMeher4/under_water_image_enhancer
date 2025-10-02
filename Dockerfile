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
EXPOSE 8080

# 6. Command to run YOUR Flask application (app.py)
#    We point it to 'app:app' which means "the 'app' object inside the 'app.py' file".
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]