from dotenv import load_dotenv
import os

def load_env():
    # Load the .env file
    load_dotenv()
    env={}
    # Access the environment variables
    env["network_name"] = os.getenv('NETWORK_NAME')
    env["network_password"] = os.getenv('NETWORK_PASSWORD')
    env["speedtest_interval"] = int(os.getenv('SPEEDTEST_INTERVAL'))
    env["device_count_interval"] = int(os.getenv('DEVICE_COUNT_INTERVAL'))

    print(f'NETWORK_NAME: {env["network_name"]}')
    print(f'NETWORK_PASSWORD: {env["network_password"]}')
    print(f'SPEEDTEST_INTERVAL: {env["speedtest_interval"]}')
    print(f'DEVICE_COUNT_INTERVAL: {env["device_count_interval"]}')

    return env
