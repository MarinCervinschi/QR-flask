# Use a stable official Python image
FROM python:3.13

# Set the working directory inside the container
WORKDIR /app

# Copy only requirements to leverage Docker's caching mechanism
COPY requirements.txt /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app

# Define the default command to run the application
CMD ["flask", "run"]