import os
import platform
import subprocess
import logging
import time
from dotenv import load_dotenv
import speedtest
from datetime import datetime

def setup_logging(ssid):
    """Set up logging configuration for the given network SSID."""
    log_folder = os.path.join(ssid, "logs")
    os.makedirs(log_folder, exist_ok=True)
    log_file = os.path.join(log_folder, f"NMS_{datetime.now().strftime('%Y-%m-%d')}.log")

    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

def get_environment_variables():
    """Retrieve environment variables for Wi-Fi credentials and polling interval."""
    try:
        load_dotenv()
        ssid = os.getenv('WIFI_SSID', default="test")
        password = os.getenv('WIFI_PASSWORD', default="test")
        poll_interval = int(os.getenv('POLL_INTERVAL', 3600))
        return ssid, password, poll_interval
    except Exception as e:
        logging.error(f"Error loading environment variables: {e}")
        raise

def set_environment_variables():
    """Prompt user to set Wi-Fi credentials and polling interval as environment variables."""
    os.environ['WIFI_SSID'] = os.getenv('WIFI_SSID', input("Enter the Wi-Fi SSID: "))
    os.environ['WIFI_PASSWORD'] = os.getenv('WIFI_PASSWORD', input("Enter the Wi-Fi Password: "))
    os.environ['POLL_INTERVAL'] = os.getenv('POLL_INTERVAL', input("Enter polling interval in seconds (default 3600): ") or "3600")

def is_connected_to_network(ssid):
    """Check if the device is connected to the specified Wi-Fi network."""
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
    """Attempt to connect to a Wi-Fi network with retries."""
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

def run_speedtest(retries=3):
    """Run a speed test and return the results."""
    attempt = 0
    while attempt < retries:
        try:
            st = speedtest.Speedtest()
            st.get_best_server()
            download_speed = round(st.download() / 1000000, 3)  # Convert to Mbps
            upload_speed = round(st.upload() / 1000000, 3)  # Convert to Mbps
            ping = round(st.results.ping, 3)
            server = st.results.server['host']
            results = {
                "download_speed_mbps": download_speed,
                "upload_speed_mbps": upload_speed,
                "ping_ms": ping,
                "server_host": server,
                "timestamp": datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
            }
            logging.info(f"Speedtest results: {results}")
            return results
        except Exception as e:
            attempt += 1
            logging.warning(f"Attempt {attempt} to run speed test: {e}")
            time.sleep(5)  # Wait before retrying
    logging.error(f"Failed to run speed test after {retries} attempts.")        
    return None

def save_results_to_file(ssid, results):

    """Save the speed test results to a CSV file."""
    
    try:
        data_folder = os.path.join(ssid, "data")
        os.makedirs(data_folder, exist_ok=True)
        filename = os.path.join(data_folder, f"NMS_{datetime.now().strftime('%Y-%m-%d')}.csv")

        file_exists = os.path.isfile(filename)
        with open(filename, "a") as file:
            if not file_exists:
                file.write("timestamp,download_speed_mbps,upload_speed_mbps,ping_ms,server_host\n")
            file.write(
                f"{results['timestamp']},{results['download_speed_mbps']},{results['upload_speed_mbps']},{results['ping_ms']},{results['server_host']}\n"
            )
        logging.info(f"Results saved to {filename}")
    except Exception as e:
        logging.error(f"Error saving results to file: {e}")

def main():
    """Main function to monitor network speed periodically."""
    while True:
        ssid, password, poll_interval = get_environment_variables()

        setup_logging(ssid)
        if not is_connected_to_network(ssid):
            logging.info(f"Not connected to Wi-Fi network: {ssid}. Attempting to connect...")
            if not connect_to_wifi(ssid, password):
                logging.error(f"Could not connect to Wi-Fi: {ssid}. Retrying in next interval ({poll_interval} seconds).")
                time.sleep(poll_interval)
                continue

        logging.info(f"Connected to Wi-Fi network: {ssid}. Running speed test...")
        results = run_speedtest()
        if results:
            save_results_to_file(ssid, results)

        logging.info(f"Waiting for the next polling interval ({poll_interval} seconds)...")
        time.sleep(poll_interval)

if __name__ == '__main__':
    main()
