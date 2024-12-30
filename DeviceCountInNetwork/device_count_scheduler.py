import schedule
import time
from device_count import scan_all_devices


def schedule_device_count(env):
    interval = env["device_count_interval"]

    scan_all_devices(env)  # Run immediately for debugging
    print(f"Scheduling device count every {interval} minutes.")
    schedule.every(env["device_count_interval"]).minutes.do(scan_all_devices(env))
    
    while True:
        schedule.run_pending()
        time.sleep(1)
