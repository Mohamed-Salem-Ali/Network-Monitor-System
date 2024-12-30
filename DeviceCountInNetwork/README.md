# Device Count in Network

## Overview

The **Device Count in Network** script calculates the number of devices connected to a network. It uses network scanning techniques to detect active devices and provides a count of those currently connected.

## Features

- Scans the local network for active devices.
- Returns the count of devices detected.
- Stores logs and data for later analysis.

## Requirements

- Python 3.8+
- Libraries: `scapy`, `logging`

You can install the required libraries by running:

```bash
pip install -r requirements.txt
```

## Usage

1. Navigate to the `Device_Count_in_Network/code` directory.

2. Run the script to start the device count:

   ```bash
   python device_count.py
   ```

3. The results will be stored in the `Device_Count_in_Network/data/device_count.csv` file.

## File Structure

- **code/**: Contains the main script for scanning and counting devices.
- **tests/**: Contains testing scripts and configurations.
- **logs/**: Logs generated during device count operations.
- **data/**: Stores CSV files with device count results.

## Example Output

The results will be saved in a CSV file in the following format:

```csv
timestamp, device_count
2024-12-22 10:00:00, 10
2024-12-22 10:15:00, 12
```
