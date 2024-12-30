# Speedtest Automation Script

## Overview

The **Speedtest Automation Script** runs automated internet speed tests using the `speedtest-cli` library and saves the results to a CSV file for further analysis. The script measures download speed, upload speed, and ping at regular intervals, ensuring network performance is logged.

## Features

- Measures download and upload speeds, and ping.
- Saves results with timestamps to a CSV file.
- Retries tests in case of failure.
- Logs the results for troubleshooting.

## Requirements

- Python 3.8+
- Libraries: `speedtest-cli`, `logging`, `python-dotenv`

You can install the required libraries by running:

```bash
pip install -r requirements.txt
```

## Usage

1. Navigate to the `Speedtest_Automation/code` directory.

2. Run the script to start the speed tests:

   ```bash
   python speedtest.py
   ```

3. The results will be saved in the `Speedtest_Automation/code/Networks/wifi_ssid/data/results.csv` file.

## File Structure

- **code/**: Contains the main script for running speed tests.
- **tests/**: Contains testing scripts and configurations.
- **logs/**: Logs generated during script execution.
- **data/**: Stores CSV files with speed test results.

## Example Output

The results will be saved in a CSV file in the following format:

```csv
timestamp, download_speed, upload_speed, ping ,server_host, server_port
2024-12-22 10:00:00, 50.2, 20.3, 10, speedtest.orange.eg:8080
2024-12-22 10:15:00, 48.7, 19.1, 12, speedtest.orange.eg:8080
```
