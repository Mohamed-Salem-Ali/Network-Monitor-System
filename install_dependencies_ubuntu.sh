#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

echo "Starting the installation of dependencies for native Ubuntu OS..."

sudo apt --fix-broken install -y 


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
echo "installing speedtest-cli via snap.. "
sudo snap install speedtest-cli -y

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
