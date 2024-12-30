import scapy.all as scapy
import socket
import os
import platform
import subprocess
import logging
import time
from dotenv import load_dotenv
from datetime import datetime
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
def get_environment_variables() -> tuple[str, str, int]:

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

def get_ip_range():
    """Automatically detect the IP range of the current network."""
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        subnet = local_ip.rsplit('.', 1)[0]  # Extract the first three octets
        ip_range = f"{subnet}.0/24"
        logging.info(f"Detected IP range: {ip_range}")
        return ip_range
    except Exception as e:
        logging.error(f"Failed to detect IP range: {e}")
        return None

def scan(ip_range):
    """Perform an ARP scan on the given IP range."""
    if not ip_range:
        logging.error("No valid IP range provided for scanning.")
        return []

    logging.info(f"Scanning IP range: {ip_range}")
    try:
        # Create ARP request and broadcast packet
        arp_request = scapy.ARP(pdst=ip_range)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast / arp_request
        
        # Send the request and capture responses
        answered_list = scapy.srp(arp_request_broadcast, timeout=10, verbose=False)[0]
        
        # Parse responses into a list of devices
        devices = [{'ip': rcv.psrc, 'mac': rcv.hwsrc} for _, rcv in answered_list]
        logging.info(f"Found {len(devices)} connected devices.")
        return devices
    except Exception as e:
        logging.error(f"Error during ARP scan: {e}")
        return []
    
def save_scanned_devices(ssid, devices):
    """
    Save the scanned devices to a file, including:
    time, number of devices, list of IP addresses, list of MAC addresses.
    """
    try:
        # Extract information
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        num_devices = len(devices)
        ip_list = [device['ip'] for device in devices]
        mac_list = [device['mac'] for device in devices]
        
        # Save to a CSV file
        device_file = f"Networks/{ssid}/data/devices_summary.csv"
        os.makedirs(os.path.dirname(device_file), exist_ok=True)
        
        with open(device_file, "a") as file:  # Append mode to keep all summaries
            file.write(f"{timestamp},{num_devices},{ip_list},{mac_list}\n")
        
        logging.info(f"Scanned device summary saved to {device_file}")
    except Exception as e:
        logging.error(f"Error saving scanned device summary: {e}")


def display_devices(devices):
    """Display the connected devices in a readable format."""
    if devices:
        print("\nConnected Devices:")
        print("IP Address\t\tMAC Address")
        print("-----------------------------------------")
        for device in devices:
            print(f"{device['ip']}\t\t{device['mac']}")
    else:
        print("No devices found.")
        logging.info("No devices found in the network.")

def main():
    """Main function to scan network devices and run speed tests."""
    while True:
        ssid, password, poll_interval = get_environment_variables()
        logging_setup(ssid)
        if not is_connected_to_network(ssid):
            logging.info(f"Not connected to Wi-Fi network: {ssid}. Attempting to connect...")
            if not connect_to_wifi(ssid, password):
                logging.error(f"Could not connect to Wi-Fi: {ssid}. Retrying in next interval ({poll_interval} seconds.")
                time.sleep(poll_interval)
                continue

        logging.info("Starting network device scan...")
        # Detect IP range automatically
        ip_range = get_ip_range()

        # Scan the network for connected devices
        devices = scan(ip_range)


        # Save scanned devices to a file
        if devices:
            save_scanned_devices(ssid,devices)
        
        logging.info(f"Waiting for the next polling interval ({poll_interval} seconds)...")
        time.sleep(poll_interval)

if __name__ == "__main__":
    main()
