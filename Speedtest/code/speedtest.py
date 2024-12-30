import os
import platform
import subprocess
import logging
import time
from dotenv import load_dotenv
import json
import speedtest
import csv
from datetime import datetime

def get_environment_variables():

    """Retrieve environment variables for Wi-Fi credentials and polling interval."""

    try:
        load_dotenv()
        ssid = os.getenv('WIFI_SSID',default="test")
        password = os.getenv('WIFI_PASSWORD',default="test")
        poll_interval = int(os.getenv('POLL_INTERVAL', 3600))
        return ssid, password, poll_interval
    except Exception as e:
        logging.error(f"Error Loading environment variables: {e}")
        raise

ssid, password, poll_interval = get_environment_variables()
CSV_FILE = f"Networks/{ssid}/data/NMS_{ssid}_{datetime.now().strftime("%Y-%m-%d")}.csv"

def setup_folders(ssid):
    
    """Set up folders structure for the given network SSID."""
    
    try:
        os.makedirs(f"Networks", exist_ok=True)
        os.makedirs(f"Networks/{ssid}/logs", exist_ok=True)
        os.makedirs(f"Networks/{ssid}/data", exist_ok=True)
    except Exception as e:
        logging.error(f"Error creating folders for SSID {ssid}: {e}")

def logging_setup(ssid):
    
    """Set up logging configuration for the given network SSID."""
    
    setup_folders(ssid)
    log_file=f"Networks/{ssid}/logs/NMS_{ssid}_{datetime.now().strftime("%Y-%m-%d")}.log"
    # Set up logging
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
def get_environment_variables():

    """Retrieve environment variables for Wi-Fi credentials and polling interval."""

    try:
        load_dotenv()
        ssid = os.getenv('WIFI_SSID',default="test")
        password = os.getenv('WIFI_PASSWORD',default="test")
        poll_interval = int(os.getenv('POLL_INTERVAL', 3600))
        return ssid, password, poll_interval
    except Exception as e:
        logging.error(f"Error Loading environment variables: {e}")
        raise

def set_environment_variables():

    """Prompt user to set Wi-Fi credentials and polling interval as environment variables."""
    
    os.environ['WIFI_SSID'] = os.getenv('WIFI_SSID', input("Enter the Wi-Fi SSID: "))
    os.environ['WIFI_PASSWORD'] = os.getenv('WIFI_PASSWORD', input("Enter the Wi-Fi Password: "))
    os.environ['POLL_INTERVAL'] = os.getenv('POLL_INTERVAL', input("Enter polling interval in seconds (default 3600): ") or "3600")

def is_connected_to_network(ssid):

    """Checks if the device is connected to the specified Wi-Fi network."""
    
    try:
        current_os = platform.system().lower()
        if current_os == 'windows':
            result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], capture_output=True, text=True)
            return ssid in result.stdout
        elif current_os == 'linux':
            result = subprocess.run(['nmcli', '-t', '-f', 'active,ssid', 'dev', 'wifi'], capture_output=True, text=True)
            return f'yes:{ssid}' in result.stdout
        elif current_os == 'darwin':  # macOS
            result = subprocess.run(['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport', '-I'], capture_output=True, text=True)
            for line in result.stdout.splitlines():
                if "SSID:" in line:
                    return ssid in line
        else:
            logging.error("Unsupported OS.")
            return False
    except Exception as e:
        logging.error(f"Error checking network connection: {e}")
        return False

def connect_to_wifi(ssid, password, retries=3):

    """Attempts to connect to a Wi-Fi network with retries."""
    
    current_os = platform.system().lower()
    attempt = 0

    while attempt < retries:
        try:
            if current_os == 'windows':
                subprocess.run(['netsh', 'wlan', 'connect', f'name={ssid}'], check=True)
            elif current_os == 'linux':
                subprocess.run(['nmcli', 'dev', 'wifi', 'connect', ssid, 'password', password], check=True)
            elif current_os == 'darwin':  # macOS
                subprocess.run(['networksetup', '-setairportnetwork', 'en0', ssid, password], check=True)
            logging.info(f"Successfully connected to Wi-Fi: {ssid}")
            return True
        except Exception as e:
            attempt += 1
            logging.warning(f"Attempt {attempt} to connect to Wi-Fi failed: {e}")
            time.sleep(5)  # Wait before retrying
    logging.error(f"Failed to connect to Wi-Fi after {retries} attempts.")
    return False

def initialize_csv():
    header = [
        "id", "Server ID","Sponsor","Server Name","Timestamp","Distance","Ping","Download","Upload","Share","IP Address"
    ]
    try:
        os.makedirs(os.path.dirname(CSV_FILE), exist_ok=True)
        with open(CSV_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            if file.tell() == 0:  # File is empty
                writer.writerow(header)
                logging.info(f"Initialized CSV file with headers: {header}")
    except Exception as e:
        logging.error(f"Failed to initialize CSV file: {e}")

# Function to convert bytes to Mbps
def bytes_to_mbps(bytes_value):
    return (bytes_value) / 1_000_000


def run_speedtest(retries=3):
    attempt = 0
    while attempt < retries:
        try:
            # Run the speedtest command with CSV output
            result = subprocess.run(['speedtest', '--csv'], capture_output=True, text=True)

            if result.returncode == 0:
                # Parse the output and add timestamp and ID
                data = result.stdout.strip().split(',')

                # Convert the download and upload speeds from bytes to Mbps
                download_bytes = float(data[6])  # Assuming the download value is in the 8th column (index 7)
                upload_bytes = float(data[7])    # Assuming the upload value is in the 9th column (index 8)

                download_mbps = bytes_to_mbps(download_bytes)
                upload_mbps = bytes_to_mbps(upload_bytes)

                # Replace the original download and upload values with the converted Mbps values
                data[6] = f"{download_mbps:.2f}"
                data[7] = f"{upload_mbps:.2f}"

                # Determine the ID
                try:
                    with open(CSV_FILE, mode='r') as file:
                        last_id = sum(1 for _ in file) - 1  # Exclude header line
                except FileNotFoundError:
                    last_id = 0

                # Add ID and date to the data
                row = [last_id + 1] + data

                # Append to the CSV file
                with open(CSV_FILE, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(row)
                
                logging.info(f"Speed test result logged successfully: {row}")
                print(f"Speed test result logged successfully: {row}")
                return
            else:
                error_msg = result.stderr.strip()
                logging.error(f"Speed test failed: {error_msg}")
                print(f"Speed test failed: {error_msg}")
        except Exception as e:
            logging.error(f"Unexpected error during speed test: {e}")
            print(f"Unexpected error: {e}")
        
        # Retry mechanism
        attempt += 1
        if attempt < retries:
            logging.info(f"Retrying speed test (Attempt {attempt + 1} of {retries})...")
            time.sleep(5)  # Wait before retrying
        else:
            logging.error(f"Speed test failed after {retries} attempts.")

def main():
    """Main function to monitor network speed periodically."""
    while True:
        logging_setup(ssid)
        initialize_csv()
        if not is_connected_to_network(ssid):
            logging.info(f"Not connected to Wi-Fi network: {ssid}. Attempting to connect...")
            if not connect_to_wifi(ssid, password):
                logging.error(f"Could not connect to Wi-Fi: {ssid}. Retrying in next interval ({poll_interval} seconds.")
                time.sleep(poll_interval)
                continue

        logging.info(f"Connected to Wi-Fi network: {ssid}. Running speed test...")
        run_speedtest()
        logging.info(f"Waiting for the next polling interval ({poll_interval} seconds)...")
        time.sleep(poll_interval)

if __name__ == '__main__':
    main()
