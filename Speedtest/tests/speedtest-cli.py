import subprocess
import time
import logging
from datetime import datetime
import csv

# Set up logging to log errors to a file
logging.basicConfig(filename="wifi_speedtest_errors.log", level=logging.ERROR, format="%(asctime)s - %(message)s")

# Define the CSV file path
CSV_FILE = "speedtest_data_py.csv"

# Write the header to the CSV file if it doesn't exist
def initialize_csv():
    header = [
        "id", "date", "server name", "server id", "idle latency", "idle jitter",
        "packet loss", "download (Mbps)", "upload (Mbps)", "download bytes",
        "upload bytes", "share url", "download server count", "download latency",
        "download latency jitter", "download latency low", "download latency high",
        "upload latency", "upload latency jitter", "upload latency low", "upload latency high",
        "idle latency low", "idle latency high"
    ]
    try:
        with open(CSV_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            if file.tell() == 0:  # File is empty
                writer.writerow(header)
    except Exception as e:
        logging.error(f"Failed to initialize CSV file: {e}")

# Run the speed test and log the results
def run_speedtest():
    try:
        # Run the speedtest command with CSV output
        result = subprocess.run(['speedtest', '-f', 'csv'], capture_output=True, text=True)

        if result.returncode == 0:
            # Parse the output and add timestamp and ID
            data = result.stdout.strip().split(',')
            current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Determine the ID
            try:
                with open(CSV_FILE, mode='r') as file:
                    last_id = sum(1 for _ in file) - 1  # Exclude header line
            except FileNotFoundError:
                last_id = 0

            # Add ID and date to the data
            row = [last_id + 1, current_date] + data

            # Append to the CSV file
            with open(CSV_FILE, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(row)
            
            print(f"Speed test result logged successfully: {row}")
        else:
            error_msg = result.stderr.strip()
            logging.error(f"Speed test failed: {error_msg}")
            print(f"Speed test failed: {error_msg}")
    except Exception as e:
        logging.error(f"Unexpected error during speed test: {e}")
        print(f"Unexpected error: {e}")

# Main loop to run speed test every 1 minute
def main():
    initialize_csv()
    while True:
        run_speedtest()
        time.sleep(60)  # Wait 1 minute before the next test

if __name__ == "__main__":
    main()
