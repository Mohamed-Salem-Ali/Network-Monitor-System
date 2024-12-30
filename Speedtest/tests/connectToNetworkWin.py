import os

def connect_to_wifi(ssid, password):
    # Create a profile for the Wi-Fi network
    profile = f"""
    <WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
        <name>{ssid}</name>
        <SSIDConfig>
            <SSID>
                <name>{ssid}</name>
            </SSID>
        </SSIDConfig>
        <connectionType>ESS</connectionType>
        <connectionMode>auto</connectionMode>
        <MSM>
            <security>
                <authEncryption>
                    <authentication>WPA2PSK</authentication>
                    <encryption>AES</encryption>
                    <useOneX>false</useOneX>
                </authEncryption>
                <sharedKey>
                    <keyType>passPhrase</keyType>
                    <protected>false</protected>
                    <keyMaterial>{password}</keyMaterial>
                </sharedKey>
            </security>
        </MSM>
    </WLANProfile>
    """
    # Save the profile to a file
    profile_path = f"{ssid}.xml"
    with open(profile_path, "w") as file:
        file.write(profile)
    
    # Add the network profile and connect
    os.system(f'netsh wlan add profile filename="{profile_path}"')
    os.system(f'netsh wlan connect name="{ssid}"')
    
    # Remove the profile file
    os.remove(profile_path)
    print(f"Attempting to connect to {ssid}")

# Example Usage
connect_to_wifi("MSA", "12345678")
