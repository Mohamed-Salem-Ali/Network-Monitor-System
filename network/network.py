from pywifi import PyWiFi, const, Profile
import time
def is_connected_to_network(network_name):
    wifi = PyWiFi()
    iface = wifi.interfaces()[0]  # Get the first Wi-Fi interface
    iface.scan()  # Scan for networks
    scan_results = iface.scan_results()  # Get scanned networks

    for network in scan_results:
        if network.ssid == network_name and iface.status() == const.IFACE_CONNECTED:
            return True
    return False

def connect_to_network(network_name, network_password):
    wifi = PyWiFi()
    iface = wifi.interfaces()[0]
    iface.disconnect()

    profile = Profile()
    profile.ssid = network_name
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP
    profile.key = network_password

    iface.remove_all_network_profiles()
    iface.add_network_profile(profile)
    iface.connect(profile)

    # Wait for connection to establish
    for _ in range(10):  # Retry for up to 10 seconds
        if iface.status() == const.IFACE_CONNECTED:
            return True
        time.sleep(1)
    return False

def main ():
    network_name = "MSA"
    network_password = "12345678"
    if is_connected_to_network(network_name):
        print(f"Already Connected to network: {network_name}")
    else:
        print(f"Not connected to network: {network_name}. Attempting to connect...")
        if connect_to_network(network_name, network_password):
            print(f"Connected to network: {network_name}")
if __name__ == "__main__":
    main()