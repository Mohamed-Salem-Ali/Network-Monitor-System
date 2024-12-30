from speedtest import run_speedtest
from device_count import scan_all_devices
from common.env_loader import load_env
if __name__ == "__main__":
    env = load_env()

    
    print("Testing function without threading...")
    run_speedtest(env)
    scan_all_devices(env)