#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

echo "Starting the installation of dependencies for native Ubuntu OS..."

# 1. Update and install system dependencies
echo "Updating package lists and installing necessary system dependencies..."
sudo apt-get update && sudo apt-get install -y --no-install-recommends \
    wireless-tools \
    python3-dev \
    network-manager \
    iputils-ping \
    net-tools \
    iproute2 \
    dbus \
    curl

# Clean up to reduce unused files
echo "Cleaning up temporary files..."
sudo apt-get clean
sudo rm -rf /var/lib/apt/lists/*

# 2. Install Ookla's Speedtest CLI
echo "Downloading and installing Ookla's Speedtest CLI..."
curl -Lo /tmp/speedtest.tgz https://install.speedtest.net/app/cli/ookla-speedtest-1.2.0-linux-x86_64.tgz
sudo tar -xzf /tmp/speedtest.tgz -C /usr/local/bin
sudo chmod +x /usr/local/bin/speedtest
rm /tmp/speedtest.tgz

# Verify installation
if ! command -v speedtest &>/dev/null; then
    echo "Error: Speedtest CLI installation failed!"
    exit 1
else
    echo "Speedtest CLI installed successfully!"
fi

# 3. Additional steps if needed for your `.exe`:
# If your .exe relies on other tools or libraries, add commands here.
# Example: Installing Python libraries globally
# sudo apt-get install python3-pip
# sudo pip3 install some-library

# 4. Confirm dependencies are installed
echo "All dependencies have been installed successfully!"
echo "You can now run your application."

exit 0
