# Use the official Python 3.11 slim image as the base
# “Start with a Linux machine that already has Python 3.11 installed.”

FROM python:3.11-slim

# Set the working directory inside the container

WORKDIR /app

# Copy only the pyproject.toml file first

COPY pyproject.toml ./

#first dot represents the source (where the copied code goes to)
# Represents the current directory inside the Docker image. (aka all code from backend/)

COPY . . 

# Install Python dependencies
RUN pip install --no-cache-dir ".[dev]"

EXPOSE 8000

# equivalent to uvicorn main:app --host 0.0.0.0 --port 8000
CMD ["./entrypoint.sh"]