# system_monitor.py
# watches CPU, RAM, and disk usage in a loop
# logs everything and warns you when something's running hot
import time
import argparse
import psutil
from utils.helpers import setup_logger

logger = setup_logger(__name__, "system_monitor.log")

def log_system_stats(threshold_cpu: float = 90.0, threshold_mem: float = 90.0):
    """Logs system statistics and alerts if thresholds are exceeded."""
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    
    stats_msg = f"CPU: {cpu}% | Memory: {mem}% | Disk: {disk}%"
    logger.info(stats_msg)
    
    if cpu > threshold_cpu:
        logger.warning(f"HIGH CPU USAGE ALERT: {cpu}%")
    if mem > threshold_mem:
        logger.warning(f"HIGH MEMORY USAGE ALERT: {mem}%")

def monitor_loop(interval: int, cpu_thresh: float, mem_thresh: float):
    """Runs the monitor continuously."""
    logger.info(f"Starting system monitor. Interval: {interval}s")
    try:
        while True:
            log_system_stats(cpu_thresh, mem_thresh)
            time.sleep(interval)
    except KeyboardInterrupt:
        logger.info("System monitor stopped.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Monitor system resources.")
    parser.add_argument("--interval", type=int, default=60, help="Check interval in seconds")
    parser.add_argument("--cpu", type=float, default=90.0, help="CPU alert threshold %")
    parser.add_argument("--mem", type=float, default=90.0, help="Memory alert threshold %")
    args = parser.parse_args()
    
    monitor_loop(args.interval, args.cpu, args.mem)
