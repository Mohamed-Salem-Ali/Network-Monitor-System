import subprocess

def is_connected_to_network(network_name):
    """
    Check if the system is connected to the specified Wi-Fi network.
    """
    try:
        # Run nmcli to check the active Wi-Fi connection
        result = subprocess.run(
            ["nmcli", "-t", "-f", "active,ssid", "dev", "wifi"],
            capture_output=True,
            text=True
        )
        active_networks = result.stdout.strip().split("\n")
        for line in active_networks:
            fields = line.split(":")
            if fields[0] == "yes" and fields[1] == network_name:
                return True
        return False
    except Exception as e:
        print(f"Error checking Wi-Fi connection: {e}")
        return False

def connect_to_network(network_name, network_password):
    """
    Attempt to connect to the specified Wi-Fi network using nmcli.
    """
    try:
        # Use nmcli to connect to the Wi-Fi network
        result = subprocess.run(
            ["nmcli", "dev", "wifi", "connect", network_name, "password", network_password],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"Successfully connected to network: {network_name}")
            return True
        else:
            print(f"Failed to connect to network: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"Error connecting to Wi-Fi: {e}")
        return False

def main():
    # Wi-Fi network credentials
    network_name = "MSA"
    network_password = "12345678"

    # Check connection
    if is_connected_to_network(network_name):
        print(f"Already connected to network: {network_name}")
    else:
        print(f"Not connected to network: {network_name}. Attempting to connect...")
        if connect_to_network(network_name, network_password):
            print(f"Connected to network: {network_name}")
        else:
            print(f"Failed to connect to network: {network_name}")

if __name__ == "__main__":
    main()
