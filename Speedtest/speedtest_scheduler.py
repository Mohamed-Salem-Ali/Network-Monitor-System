import schedule
import time
from speedtest import run_speedtest

def schedule_speedtest(env):
    
    interval = env["speedtest_interval"]

    run_speedtest(env)  # Run immediately for debugging
    print(f"Scheduling speed test every {interval} hours.")
    schedule.every(interval).minutes.do(run_speedtest(env))
    
    while True:
        schedule.run_pending()
        time.sleep(1)
