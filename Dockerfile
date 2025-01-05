# Use Ubuntu 20.04 base image
FROM python:3.10-slim

# Install required tools and dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    wireless-tools \
    python3-dev \
    network-manager \
    net-tools \
    iproute2 \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Optionally, install Python if needed for your app
RUN apt-get update && apt-get install -y python3-pip


# Set working directory
WORKDIR /app

# Copy project files
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose any ports your app needs
EXPOSE 5000

# Specify default command
CMD ["echo", "Container is ready to use!"]