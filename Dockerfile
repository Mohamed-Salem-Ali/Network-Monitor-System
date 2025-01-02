# Use Ubuntu 20.04 base image
FROM ubuntu:20.04


# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Africa/Cairo

# Install required tools and dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    wireless-tools \
    python3-dev \
    network-manager \
    iputils-ping \
    net-tools \
    iproute2 \
    dbus \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Optionally, install Python if needed for your app
RUN apt-get update && apt-get install -y python3 python3-pip


# Add the start script
COPY start_script.sh /etc/init/start_script.sh

# Ensure the script is executable
RUN chmod +x /etc/init/start_script.sh

# Set working directory
WORKDIR /app

# Copy project files
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Expose any ports your app needs
EXPOSE 5000

# Start the NetworkManager service
ENTRYPOINT ["/etc/init/start_script.sh"]