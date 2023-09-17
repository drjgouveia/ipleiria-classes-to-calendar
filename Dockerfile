# Use the official Python image as a parent image
FROM python:3.11-slim

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Install system dependencies
RUN apt-get update && apt-get install -y nginx

# Create a directory for your app code
WORKDIR /app

# Install Flask and Gunicorn (a WSGI HTTP server)
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
RUN pip install Flask gunicorn

# Copy your Flask app code into the container
COPY ./ /app

# Expose port 80 for Nginx
EXPOSE 80

# Start Nginx and Gunicorn when the container runs
CMD service nginx start && gunicorn -w 4 -b 0.0.0.0:8000 app:app
