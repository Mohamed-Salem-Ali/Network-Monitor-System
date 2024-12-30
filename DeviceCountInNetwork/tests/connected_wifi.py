from scapy.all import ARP, Ether, srp

def scan_network(ip_range):
    """
    Scans the specified IP range to find connected devices.
    Returns a list of devices with their IP and MAC addresses.
    """
    print(f"Scanning IP range: {ip_range}")
    
    # Create an ARP request and broadcast it to the network
    arp_request = ARP(pdst=ip_range)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request

    # Send the request and capture responses
    answered_list = srp(arp_request_broadcast, timeout=2, verbose=False)[0]

    # Parse the responses
    devices = []
    for sent, received in answered_list:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})

    return devices

def display_devices(devices):
    """
    Displays the connected devices in a readable format.
    """
    if devices:
        print("\nConnected devices:")
        print("IP Address\t\tMAC Address")
        print("-----------------------------------------")
        for device in devices:
            print(f"{device['ip']}\t\t{device['mac']}")
    else:
        print("No devices found.")

if __name__ == "__main__":
    # Define the IP range to scan (adjust to your subnet)
    ip_range = "192.168.0.0/24"

    # Scan the network and display results
    connected_devices = scan_network(ip_range)
    display_devices(connected_devices)

    # Optional: Extract only MAC addresses
    mac_addresses = [device['mac'] for device in connected_devices]
    print("\nList of MAC addresses:")
    print(mac_addresses)
