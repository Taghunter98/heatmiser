# Use a base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy files
COPY requirements.txt /app/requirements.txt
COPY heating.log /app/heating.log

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy application files into the container
COPY . /app/

# Expose the application port
EXPOSE 6000

# Run the server with Gunicorn
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:6000", "app:create_app()"]