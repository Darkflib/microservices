# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install any needed packages specified in requirements.txt
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Install pico2wave for Pico TTS
RUN sed -i -e 's/ main/ main contrib non-free/g' /etc/apt/sources.list
RUN apt-get update && apt-get install -y --no-install-recommends libttspico-utils

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV NAME PicoTTS-Flask

# Copy app files into the container
COPY . /app

# Run gunicorn when the container launches
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app", "--workers=4", "--threads=4", "--timeout=120"]