"""
Common utility functions:

"""
import platform
import subprocess
import time
#from pywifi import PyWiFi, const, Profile
import time
def currentOs():
    """Returns the current operating system."""
    
    return platform.system().lower()


# def is_connected_network(network_name,logger):
#     try:
#         wifi = PyWiFi()
#         iface = wifi.interfaces()[0]  # Get the first Wi-Fi interface
#         iface.scan()  # Scan for networks
#         scan_results = iface.scan_results()  # Get scanned networks

#         for network in scan_results:
#             if network.ssid == network_name and iface.status() == const.IFACE_CONNECTED:
#                 return True
#     except Exception as e:
#         logger.error(f"Error checking network connection: {e}")
#         return False    # Logic to check network connectivity
    
# def connect_network(network_name, network_password,logger):
#     try:
#         wifi = PyWiFi()
#         iface = wifi.interfaces()[0]
#         iface.disconnect()

#         profile = Profile()
#         profile.ssid = network_name
#         profile.auth = const.AUTH_ALG_OPEN
#         profile.akm.append(const.AKM_TYPE_WPA2PSK)
#         profile.cipher = const.CIPHER_TYPE_CCMP
#         profile.key = network_password

#         iface.remove_all_network_profiles()
#         iface.add_network_profile(profile)
#         iface.connect(profile)

#         # Wait for connection to establish
#         for _ in range(10):  # Retry for up to 10 seconds
#             if iface.status() == const.IFACE_CONNECTED:
#                 logger.info(f"Successfully connected to Wi-Fi: {network_name}")
#                 return True
#             time.sleep(1)
#     except Exception as e:
#         logger.warning(f"Attempt to connect to Wi-Fi failed: {e}")
#         time.sleep(5)  # Wait before retrying
#     logger.error(f"Failed to connect to Wi-Fi after 3 attempts.")
#     return False




def is_connected_to_network(ssid,logger):
    """Checks if the device is connected to the specified Wi-Fi network."""
    
    try:
        current_os = currentOs()
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
            logger.error("Unsupported OS.")
            return False
    except Exception as e:
        logger.error(f"Error checking network connection: {e}")
        return False# Logic to check network connectivity

def connect_to_network(ssid, password, logger, max_attempts=3, retry_interval=5):
    """Attempts to connect to a Wi-Fi network with retries."""
    attempt = 0
    current_os = currentOs()
    
    while attempt < max_attempts:
        try:
            logger.info(f"Attempt {attempt + 1} to connect to Wi-Fi: {ssid}...")
            if current_os == 'windows':
                subprocess.run(['netsh', 'wlan', 'connect', f'name={ssid}'], check=True)
            elif current_os == 'linux':
                subprocess.run(['nmcli', 'dev', 'wifi', 'connect', ssid, 'password', password], check=True)
            elif current_os == 'darwin':  # macOS
                subprocess.run(['networksetup', '-setairportnetwork', 'en0', ssid, password], check=True)

            # Validate connection
            if is_connected_to_network(ssid, logger):
                logger.info(f"Successfully connected to Wi-Fi: {ssid}")
                return True
            else:
                logger.warning(f"Connection attempt {attempt + 1} to Wi-Fi: {ssid} failed validation. Retrying...")
        
        except subprocess.CalledProcessError as e:
            logger.warning(f"Attempt {attempt + 1} failed with error code {e.returncode}. Retrying...")
        
        except Exception as e:
            logger.error(f"Attempt {attempt + 1} failed with error: {e}. Retrying...")
        
        # Wait before the next retry
        attempt += 1
        if attempt < max_attempts:
            logger.info(f"Waiting {retry_interval} seconds before retrying...")
            time.sleep(retry_interval)

    # If all retries fail, log the failure
    logger.error(f"Failed to connect to Wi-Fi: {ssid} after {max_attempts} attempts.")
    return False


def bytes_to_mbps(bytes_value):
    return (bytes_value) / 1_000_000


