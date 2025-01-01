from datetime import datetime
import time
from common.folder_setup import setup_folders
from common.utils import is_connected_to_network, connect_to_network
from common.logger import setup_logger
from common.env_loader import load_env
import scapy.all as scapy
import socket
import netifaces
import csv
import os
def get_ip_range_old(logger):
    """Automatically detect the IP range of the current network."""
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        subnet = local_ip.rsplit('.', 1)[0]  # Extract the first three octets
        ip_range = f"{subnet}.0/24"
        logger.info(f"Detected IP range: {ip_range}")
        return ip_range
    except Exception as e:
        logger.error(f"Failed to detect IP range: {e}")
        return None

def get_ip_range(logger):
    """Automatically detect the IP range of the current network."""
    try:
        # Get the active interface's IP address
        interfaces = netifaces.interfaces()
        for interface in interfaces:
            if netifaces.AF_INET in netifaces.ifaddresses(interface):
                addr_info = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]
                local_ip = addr_info['addr']
                if local_ip.startswith("127.") or local_ip.startswith("::1"):
                    continue  # Skip loopback interface
                subnet = local_ip.rsplit('.', 1)[0]  # Extract the first three octets
                ip_range = f"{subnet}.0/24"
                logger.info(f"Detected IP range: {ip_range}")
                return ip_range

        logger.error("No active network interface with a valid IP found.")
        return None
    except Exception as e:
        logger.error(f"Failed to detect IP range: {e}")
        return None

def scan(ip_range,logger):
    """Perform an ARP scan on the given IP range."""
    if not ip_range:
        logger.error("No valid IP range provided for scanning.")
        return []

    logger.info(f"Scanning IP range: {ip_range}")
    try:
        # Create ARP request and broadcast packet
        arp_request = scapy.ARP(pdst=ip_range)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast / arp_request
        
        # Send the request and capture responses
        answered_list = scapy.srp(arp_request_broadcast, timeout=10, verbose=False)[0]
        
        # Parse responses into a list of devices
        devices = [{'ip': rcv.psrc, 'mac': rcv.hwsrc} for _, rcv in answered_list]
        logger.info(f"Found {len(devices)} connected devices.")
        return devices
    except Exception as e:
        logger.error(f"Error during ARP scan: {e}")
        return []


def save_scanned_devices(ssid, devices,logger):
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
        device_file = f"data/{ssid}/devices_summary.csv"
        os.makedirs(os.path.dirname(device_file), exist_ok=True)
        
        with open(device_file, "a") as file:  # Append mode to keep all summaries
            file.write(f"{timestamp},{num_devices},{ip_list},{mac_list}\n")
        
        logger.info(f"Scanned device summary saved to {device_file}")
        print(f"Scanned device summary saved to {device_file}")
    except Exception as e:
        logger.error(f"Error saving scanned device summary: {e}")
        print(f"Error saving scanned device summary: {e}")

def scan_all_devices(env):
    ssid=env["network_name"]
    password=env["network_password"]
    setup_folders(ssid)
    logger = setup_logger("device_count", f"logs/{ssid}/device_count.log")
    interval =int(env["device_count_interval"])
    while True:
        if not is_connected_to_network(ssid,logger):
            logger.info(f"Not connected to Wi-Fi network: {ssid}. Attempting to connect...")
            if not connect_to_network(ssid,password,logger):
                logger.error(f"Could not connect to Wi-Fi: {ssid}.")  
                time.sleep(interval)
                continue 

        logger.info(f"Connected to Wi-Fi network: {ssid}")
        logger.info("Starting network device scan...")
        
        # Detect IP range automatically
        ip_range = get_ip_range(logger)

        # Scan the network for connected devices
        devices = scan(ip_range,logger)

        # Save scanned devices to a file
        if devices:
            save_scanned_devices(ssid,devices,logger)
        
        logger.info(f"Waiting for the next polling interval ({interval} seconds)...")
        time.sleep(interval)

def main(): 
    env = load_env()
    scan_all_devices(env) 

if __name__ == "__main__": 
    main()