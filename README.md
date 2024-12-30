# NMS_Collector

## Overview

**NMS_Collector** is the data collection layer for the **Network Monitoring System (NMS)**. Its primary purpose is to gather network metrics, logs, and other system performance data from various sources for further processing and analysis.

This repository contains scripts for collecting data such as internet speed tests and network device counts, which will be used by other components of the NMS for analysis and visualization.

## Repository Structure

The repository is organized into the following folders:

```
NMS_Collector/
|
├── common/
│   ├── __init__.py
│   ├── env_loader.py        # For loading environment variables
│   ├── logger.py            # For logging setup
│   ├── utils.py             # For shared utility functions
│   ├── folder_setup.py      # For setting up required folders
├── Speedtest_Automation/
│   ├── __init__.py
│   ├── code/         # Main source code for Speedtest Automation
│   ├── tests/        # Testing scripts and configurations
│   ├── logs/         # Log files generated during execution
│   ├── data/         # Data files
│   └── README.md     # Documentation file for Speedtest Automation
├── Device_Count_in_Network/
│   ├── __init__.py
│   ├── code/         # Code for calculating number of devices in the network
│   ├── tests/        # Testing scripts and configurations
│   ├── logs/         # Log files for device count operations
│   ├── data/         # Data files
│   └── README.md     # Documentation file for Device Count in Network
├── data/
│   ├── speedtest_results.csv # Store speed test results
│   ├── device_count_results.csv # Store device count results
├── logs/
│   ├── speedtest.log        # Log file for speed tests
│   ├── device_count.log     # Log file for device count
├── .env                 # Environment variables
├── .gitignore           # Git ignore file
├── device_count.py      # Script for counting devices
├── docker-compose.yml   # Docker Compose configuration
├── Dockerfile           # Docker container configuration
├── main.py              # Main entry point of the project
├── README.md            # Documentation file
├── requirements.txt     # Python dependencies for the project
├── speedtest.py         # Script for running speed tests
└── test.py              # Script for testing
```

## Project Structure

This repository works as part of the **Network Monitoring System (NMS)** and integrates with other components:

- **Backend**: Processes and analyzes the collected data.
- **Database**: Stores the collected data for retrieval and visualization.
- **Frontend**: Displays the data in a user-friendly interface.

## Requirements

- Python 3.8+
- Required Libraries: See `requirements.txt` for details.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/NMS_Collector.git
   ```

2. Install dependencies:

   ```bash
   cd NMS_Collector
   pip install -r requirements.txt
   ```

## Usage

Each part of the project (Speedtest Automation and Device Count in Network) has its own README for setup, usage, and configuration. Please refer to them for detailed instructions.
