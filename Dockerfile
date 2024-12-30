# Use Python base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install required tools 
RUN apt-get update && apt-get install -y \
    wireless-tools python3-dev\ 
    network-manager \
    iputils-ping \
    net-tools \
    iproute2 \
    curl \
    && apt-get clean

# Download and install Speedtest CLI
RUN curl -Lo /usr/bin/speedtest https://install.speedtest.net/app/cli/ookla-speedtest-1.2.0-linux-x86_64.tgz \
    && tar -xzf /usr/bin/speedtest -C /usr/bin/ \
    && chmod +x /usr/bin/speedtest

# Copy requirements 
COPY requirements.txt .

# Install the dependencies 
RUN pip install --no-cache-dir -r requirements.txt


# Copy the entire project into the container
COPY . .

# Default command
CMD ["echo", "Container is ready"]