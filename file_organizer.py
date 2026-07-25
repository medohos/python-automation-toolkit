# file_organizer.py
# sorts files in a directory into subfolders based on extension
# got sick of my Downloads folder being a mess so I made this
import os
import shutil
import argparse
from pathlib import Path
from utils.helpers import setup_logger

logger = setup_logger(__name__)

EXTENSION_MAP = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg'],
    'Documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.xls', '.xlsx', '.csv'],
    'Videos': ['.mp4', '.avi', '.mkv', '.mov'],
    'Audio': ['.mp3', '.wav', '.flac'],
    'Archives': ['.zip', '.tar', '.gz', '.rar'],
}

def organize_files(source_dir: str) -> None:
    """Go through every file in the dir and move it to the right subfolder."""
    source_path = Path(source_dir)
    if not source_path.exists() or not source_path.is_dir():
        logger.error(f"Invalid directory: {source_dir}")
        return

    logger.info(f"Organizing files in {source_dir}")
    
    for item in source_path.iterdir():
        if item.is_file():
            ext = item.suffix.lower()
            moved = False
            for category, extensions in EXTENSION_MAP.items():
                if ext in extensions:
                    dest_dir = source_path / category
                    dest_dir.mkdir(exist_ok=True)
                    try:
                        shutil.move(str(item), str(dest_dir / item.name))
                        logger.info(f"Moved {item.name} to {category}")
                        moved = True
                        break
                    except Exception as e:
                        logger.error(f"Error moving {item.name}: {e}")
            if not moved:
                # Move to Others
                dest_dir = source_path / 'Others'
                dest_dir.mkdir(exist_ok=True)
                try:
                    shutil.move(str(item), str(dest_dir / item.name))
                    logger.info(f"Moved {item.name} to Others")
                except Exception as e:
                    logger.error(f"Error moving {item.name}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Organize files in a directory.")
    parser.add_argument("directory", help="The directory to organize")
    args = parser.parse_args()
    organize_files(args.directory)
