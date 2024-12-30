import time
from common.utils import is_connected_to_network, connect_to_network , bytes_to_mbps 
from common.folder_setup import  setup_folders
from common.env_loader import load_env
from common.logger import setup_logger 
import subprocess
import csv
import os 

def speedtest_csv(CSV_FILE,logger,data):
    # Add ID and write header if needed
    try:
        if not os.path.exists(CSV_FILE):
            last_id = 0
            with open(CSV_FILE, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["id", "Server ID","Sponsor","Server Name","Timestamp","Distance","Ping","Download","Upload","Share","IP Address"])  # Add headers
        else:
            with open(CSV_FILE, mode='r') as file:
                last_id = sum(1 for _ in file) - 1

        row = [last_id + 1] + data
        with open(CSV_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(row)
    except Exception as e:
        logger.error(f"Failed to initialize CSV file: {e}")


def Calculate_speedtest(CSV_FILE, logger, retries=3, sleep_duration=5):
    attempt = 0
    while attempt < retries:
        try:
            logger.info(f"Starting speed test (Attempt {attempt + 1})...")
            result = subprocess.run(['speedtest', '--csv'], capture_output=True, text=True)

            if result.returncode == 0:
                data = result.stdout.strip().split(',')
                
                if len(data) <= 7:
                    logger.error("Speed test output is incomplete. Skipping this attempt.")
                    return
                
                # Convert speeds
                download_mbps = bytes_to_mbps(float(data[6]))
                upload_mbps = bytes_to_mbps(float(data[7]))
                data[6] = f"{download_mbps:.2f}"
                data[7] = f"{upload_mbps:.2f}"

                speedtest_csv(CSV_FILE,logger,data)

                logger.info(f"Speed test result logged successfully")
                print(f"Speed test result logged successfully")
                return
            else:
                logger.error(f"Speed test failed: {result.stderr.strip()}")
        except Exception as e:
            logger.error(f"Unexpected error during speed test: {e}")
            print(f"Unexpected error: {e}")
        
        attempt += 1
        if attempt < retries:
            logger.info(f"Retrying speed test (Attempt {attempt + 1} of {retries})...")
            time.sleep(sleep_duration)
        else:
            logger.error(f"Speed test failed after {retries} attempts.")


def run_speedtest(env):
    """Main function to run speed test periodically."""
    
    ssid=env["network_name"]
    password=env["network_password"]
    setup_folders(ssid)
    logger = setup_logger("speedtest", f"logs/{ssid}/speedtest.log")
    CSV_FILE = f"data/{ssid}/speedtest.csv"
    interval =int(env["speedtest_interval"])
    #initialize_speedtest_csv(CSV_FILE,logger)
    
    while True:
        if not is_connected_to_network(ssid,logger):
            logger.info(f"Not connected to Wi-Fi network: {ssid}. Attempting to connect...")
            if not connect_to_network(ssid,password,logger):
                logger.error(f"Could not connect to Wi-Fi: {ssid}.")
                logger.info(f"Waiting for the next polling interval ({interval} seconds)...")
                time.sleep(interval)
                continue

        logger.info(f"Connected to Wi-Fi network: {ssid}. Running speed test...")
        Calculate_speedtest(CSV_FILE,logger,retries=3)
        logger.info(f"Waiting for the next polling interval ({interval} seconds)...")
        time.sleep(interval)

def main(): 
    
    env = load_env()
    run_speedtest(env)  


if __name__ == "__main__": 
    main()