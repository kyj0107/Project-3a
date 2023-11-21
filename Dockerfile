# Use an official python image as the base image
FROM python:3.8-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Copy the contents from the current directory into the container at /app
COPY . /app

# Upgrade pip
RUN pip install --upgrade pip

# Install any needed packages
RUN pip install --no-cache-dir -r requirements.txt

# Set the default command to run when starting the container
CMD ["python", "app.py"]