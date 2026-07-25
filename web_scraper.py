# web_scraper.py
# grabs all the links from a page and saves them to json/csv
# handy when you need to quickly pull data off a site
import argparse
import csv
import json
import requests
from bs4 import BeautifulSoup
from utils.helpers import setup_logger

logger = setup_logger(__name__)

def fetch_page(url: str) -> str:
    """Download the page HTML. Returns empty string if it fails."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logger.error(f"Failed to fetch {url}: {e}")
        return ""

def scrape_links(html: str, base_url: str) -> list:
    """Scrapes all links from the HTML content."""
    soup = BeautifulSoup(html, 'html.parser')
    links = []
    for a_tag in soup.find_all('a', href=True):
        href = a_tag.get('href', '')
        if href.startswith('/'):
            href = base_url.rstrip('/') + href
        links.append({'text': a_tag.text.strip(), 'url': href})
    return links

def save_to_json(data: list, filename: str) -> None:
    """Saves data to a JSON file."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    logger.info(f"Data saved to {filename}")

def save_to_csv(data: list, filename: str) -> None:
    """Saves data to a CSV file."""
    if not data:
        return
    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)
    logger.info(f"Data saved to {filename}")

def main():
    parser = argparse.ArgumentParser(description="Configurable web scraper.")
    parser.add_argument("url", help="URL to scrape")
    parser.add_argument("--output", choices=['json', 'csv'], default='json', help="Output format")
    parser.add_argument("--filename", default="output", help="Output filename (without extension)")
    args = parser.parse_args()
    
    logger.info(f"Scraping {args.url}")
    html = fetch_page(args.url)
    if html:
        data = scrape_links(html, args.url)
        filename = f"{args.filename}.{args.output}"
        if args.output == 'json':
            save_to_json(data, filename)
        else:
            save_to_csv(data, filename)

if __name__ == "__main__":
    main()
