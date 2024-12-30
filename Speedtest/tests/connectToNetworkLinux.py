import os

def connect_to_wifi(ssid, password):
    os.system(f'nmcli dev wifi connect "{ssid}" password "{password}"')
    print(f"Attempting to connect to {ssid}")

# Example Usage
connect_to_wifi("YourNetworkName", "YourPassword")
