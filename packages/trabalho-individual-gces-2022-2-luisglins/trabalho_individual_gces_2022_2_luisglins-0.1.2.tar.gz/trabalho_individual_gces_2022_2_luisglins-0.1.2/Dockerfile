# Use an official Python runtime as the base image
FROM python:3.8

# Set the working directory in the container
WORKDIR /application

# Copy the requirements file to the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files to the container
COPY . .

# Run de main application
CMD ["python", "src/main.py"]