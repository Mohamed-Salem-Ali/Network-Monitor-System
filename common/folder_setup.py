import os

def setup_folders(ssid):
    os.makedirs("data", exist_ok=True)
    os.makedirs(f"data/{ssid}", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    os.makedirs(f"logs/{ssid}", exist_ok=True)
