FROM python:3.8

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY flask/requirements.txt .

# Install any needed packages specified in requirements-flask.txt
RUN pip install -r requirements.txt

# Copy the rest of your flask folder into the container at /app
COPY flask/ .

# Make port 8502 available to the world outside this container
EXPOSE 8502

# Define environment variable
ENV NAME HealthCheck

# Run health_check.py when the container launches
CMD ["python", "health_check.py"]
