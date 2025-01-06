#!/bin/bash

# Ensure the script exits on error
set -e

echo "Updating system and installing dependencies..."

# Install dependencies (example)
if ! command -v python3 &>/dev/null; then
    echo "Python3 is not installed. Installing it..."
    brew install python3
fi

if ! command -v pip3 &>/dev/null; then
    echo "pip3 is not installed. Installing it..."
    brew install pip3
fi

echo "Installing project dependencies from requirements.txt..."
pip3 install -r requirements.txt

# Install PyInstaller (if not already installed)
if ! command -v pyinstaller &>/dev/null; then
    echo "PyInstaller is not installed. Installing it..."
    pip3 install pyinstaller
fi

echo "Building the executable..."
pyinstaller --onefile file.py

echo "Executable created in dist/ directory. Running the executable..."

# Run the executable
./dist/file
