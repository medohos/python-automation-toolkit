# backup_manager.py
# zips up a folder into a timestamped backup
# can also run it on a loop so it backs up every X hours
import os
import time
import shutil
import argparse
from datetime import datetime
from pathlib import Path
from utils.helpers import setup_logger

logger = setup_logger(__name__)

def create_backup(source: str, dest: str) -> None:
    """Zip up the source folder and drop it in dest with a timestamp."""
    src_path = Path(source)
    dest_path = Path(dest)
    
    if not src_path.exists():
        logger.error(f"Source path {source} does not exist.")
        return
        
    dest_path.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"backup_{src_path.name}_{timestamp}"
    backup_path = dest_path / backup_name
    
    logger.info(f"Starting backup of {source} to {backup_path}.zip")
    
    try:
        shutil.make_archive(str(backup_path), 'zip', str(src_path))
        logger.info("Backup completed successfully.")
    except Exception as e:
        logger.error(f"Backup failed: {e}")

def schedule_backup(source: str, dest: str, interval_hours: float):
    """Runs backup on a schedule."""
    interval_seconds = interval_hours * 3600
    logger.info(f"Scheduled backup every {interval_hours} hours.")
    try:
        while True:
            create_backup(source, dest)
            logger.info(f"Waiting {interval_hours} hours for next backup...")
            time.sleep(interval_seconds)
    except KeyboardInterrupt:
        logger.info("Backup schedule stopped.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Backup a directory.")
    parser.add_argument("source", help="Directory to backup")
    parser.add_argument("dest", help="Destination directory for backup files")
    parser.add_argument("--schedule", type=float, help="Run on schedule every X hours")
    args = parser.parse_args()
    
    if args.schedule:
        schedule_backup(args.source, args.dest, args.schedule)
    else:
        create_backup(args.source, args.dest)
