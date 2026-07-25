# pdf_merger.py
# takes all PDFs in a folder and combines them into one
# mainly wrote this for merging scanned documents
import argparse
from pathlib import Path
from PyPDF2 import PdfMerger
from utils.helpers import setup_logger

logger = setup_logger(__name__)

def merge_pdfs(input_dir: str, output_file: str) -> None:
    """Finds all PDFs in input_dir, merges them, writes to output_file."""
    dir_path = Path(input_dir)
    if not dir_path.exists() or not dir_path.is_dir():
        logger.error(f"Invalid directory: {input_dir}")
        return

    pdf_files = sorted(dir_path.glob('*.pdf'))
    if not pdf_files:
        logger.warning(f"No PDF files found in {input_dir}")
        return

    merger = PdfMerger()
    try:
        for pdf in pdf_files:
            logger.info(f"Appending {pdf.name}")
            merger.append(str(pdf))
        
        merger.write(output_file)
        logger.info(f"Successfully merged {len(pdf_files)} files into {output_file}")
    except Exception as e:
        logger.error(f"Error merging PDFs: {e}")
    finally:
        merger.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge multiple PDF files.")
    parser.add_argument("directory", help="Directory containing PDF files")
    parser.add_argument("output", help="Output PDF file name")
    args = parser.parse_args()
    merge_pdfs(args.directory, args.output)
