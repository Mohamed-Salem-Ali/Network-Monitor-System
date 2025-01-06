#!/bin/bash

# Ensure the script exits on error
set -e

echo "Updating system and installing dependencies..."

# Check if Homebrew is installed, and install it if not
if ! command -v brew &>/dev/null; then
    echo "Homebrew not found. Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Update Homebrew
echo "Updating Homebrew..."
brew update

# Install Python3
if ! command -v python3 &>/dev/null; then
    echo "Python3 is not installed. Installing Python3..."
    brew install python3
fi

# Install pip3
if ! command -v pip3 &>/dev/null; then
    echo "pip3 is not installed. Installing pip3..."
    brew install pip3
fi

# Install required Python packages
echo "Installing Python packages from requirements.txt..."
pip3 install -r requirements.txt

# Install Speedtest CLI via Homebrew (if not installed)
if ! command -v speedtest-cli &>/dev/null; then
    echo "Speedtest CLI is not installed. Installing it via Homebrew..."
    brew install speedtest-cli
fi

echo "All dependencies are installed successfully."
