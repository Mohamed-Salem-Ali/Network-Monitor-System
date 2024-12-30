import os

def connect_to_wifi(ssid, password):
    # Replace 'en0' with your Wi-Fi interface name if different
    interface = "en0"
    os.system(f'networksetup -setairportnetwork {interface} "{ssid}" "{password}"')
    print(f"Attempting to connect to {ssid}")

# Example Usage
connect_to_wifi("YourNetworkName", "YourPassword")