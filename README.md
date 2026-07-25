# python-automation-toolkit

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

I got tired of doing the same stuff over and over so I wrote scripts to do it for me. This is basically my personal collection of Python tools that I actually use — file cleanup, scraping, PDF stuff, etc.

Feel free to grab whatever's useful.

## What's in here

| Script | What it does |
|--------|-------------|
| `file_organizer.py` | Sorts a messy folder (like Downloads) into subfolders by file type |
| `web_scraper.py` | Pulls links off a webpage and dumps them to JSON or CSV |
| `pdf_merger.py` | Smashes a bunch of PDFs into one file |
| `image_resizer.py` | Bulk resize + compress images — saves a ton of space |
| `system_monitor.py` | Keeps an eye on CPU/RAM/disk and yells at you if something's high |
| `email_sender.py` | Send emails in bulk from a CSV list using a template |
| `backup_manager.py` | Zips up a folder as a backup, can run on a schedule too |

## Getting started

```bash
git clone https://github.com/medohos/python-automation-toolkit.git
cd python-automation-toolkit
pip install -r requirements.txt
```

You can use a venv if you want (`python -m venv venv && venv\Scripts\activate` on Windows).

## Usage

**Clean up a messy folder:**
```bash
python file_organizer.py ~/Downloads
```

**Scrape links from a site:**
```bash
python web_scraper.py https://example.com --output csv --filename links
```

**Merge PDFs:**
```bash
python pdf_merger.py ./my-pdfs merged.pdf
```

**Resize images in bulk:**
```bash
python image_resizer.py ./photos ./photos-small --width 1024 --height 1024 --quality 80
```

**Monitor your system:**
```bash
python system_monitor.py --interval 30 --cpu 85 --mem 90
```

**Send bulk emails:**
```bash
python email_sender.py contacts.csv template.txt "Hey check this out" you@gmail.com your_app_password
```

**Backup a folder (runs every 24h):**
```bash
python backup_manager.py ./important-stuff ./backups --schedule 24
```

## Contributing

PRs welcome. If you have a script that fits the vibe, open a PR and I'll take a look.

## License

MIT — do whatever you want with it.
