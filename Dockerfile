# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI application code into the container
COPY . /app/

# Set environment variables
ARG HOST
ARG PORT
ENV HOST=${HOST}
ENV PORT=${PORT}

# Make port available to the world outside this container
EXPOSE ${PORT}

# Run app.py when the container launches
#CMD ["uvicorn", "main:app", "--host", "${HOST}", "--port", "${PORT}"]
CMD ["sh", "-c", "uvicorn api:app --host $HOST --port $PORT"]