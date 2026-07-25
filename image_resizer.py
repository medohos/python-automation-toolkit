# image_resizer.py
# resize + compress a bunch of images at once
# useful when you need to shrink photos before uploading somewhere
import argparse
from pathlib import Path
from PIL import Image
from utils.helpers import setup_logger

logger = setup_logger(__name__)

def process_images(input_dir: str, output_dir: str, size: tuple, quality: int) -> None:
    """Loop through images, resize them, save to output dir."""
    in_path = Path(input_dir)
    out_path = Path(output_dir)
    
    if not in_path.exists() or not in_path.is_dir():
        logger.error(f"Invalid input directory: {input_dir}")
        return
        
    out_path.mkdir(parents=True, exist_ok=True)
    
    for ext in ('*.jpg', '*.jpeg', '*.png'):
        for img_path in in_path.glob(ext):
            try:
                with Image.open(img_path) as img:
                    img.thumbnail(size)
                    save_path = out_path / img_path.name
                    img.save(save_path, optimize=True, quality=quality)
                    logger.info(f"Processed {img_path.name}")
            except Exception as e:
                logger.error(f"Failed to process {img_path.name}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch resize images.")
    parser.add_argument("input", help="Input directory")
    parser.add_argument("output", help="Output directory")
    parser.add_argument("--width", type=int, default=800, help="Max width")
    parser.add_argument("--height", type=int, default=800, help="Max height")
    parser.add_argument("--quality", type=int, default=85, help="JPEG quality (1-100)")
    args = parser.parse_args()
    
    process_images(args.input, args.output, (args.width, args.height), args.quality)
