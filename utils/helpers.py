import logging
from pathlib import Path

def setup_logger(name: str, log_file: str = None) -> logging.Logger:
    """Sets up and returns a configured logger."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    
    if log_file:
        fh = logging.FileHandler(log_file)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        
    return logger

def ensure_dir(path: Path) -> bool:
    """Ensures a directory exists."""
    path.mkdir(parents=True, exist_ok=True)
    return path.exists()
