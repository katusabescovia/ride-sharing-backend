# Dockerfile
FROM python:3.9-slim

# Setting working directory in the container
WORKDIR /app

# Setting  environment variable for Python module search path
ENV PYTHONPATH=/app/src

# Copying the entire app including the src folder
COPY . .

# Installing  dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Exposing  the port your app will run on
EXPOSE 8080

# Command to run the application (Gunicorn for production)
CMD ["gunicorn", "src.server:app", "--bind", "0.0.0.0:8080"]
