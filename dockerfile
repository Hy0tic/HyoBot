# Use an official Python runtime as the base image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /

# Copy the requirements.txt file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . .

# Specify the command to run your application
CMD ["python", "main.py"]
