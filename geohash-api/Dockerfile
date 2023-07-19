# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Install any needed packages specified in requirements.txt
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --trusted-host pypi.python.org -r requirements.txt


RUN apt-get update && apt-get upgrade -y

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV NAME GeoHash-Flask

# Copy app files into the container
COPY . /app

# Run gunicorn when the container launches
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app", "--workers=4", "--threads=4", "--timeout=120"]