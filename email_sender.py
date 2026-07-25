# email_sender.py
# reads a CSV of contacts and sends each one a templated email
# use {{name}} in your template and it'll swap it out per person
import csv
import smtplib
import argparse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utils.helpers import setup_logger

logger = setup_logger(__name__)

def send_bulk_emails(csv_file: str, template_file: str, subject: str, sender: str, password: str, smtp_server: str = "smtp.gmail.com", smtp_port: int = 587):
    """Reads contacts CSV + template, connects to SMTP, fires off the emails."""
    try:
        with open(template_file, 'r', encoding='utf-8') as f:
            template = f.read()
    except Exception as e:
        logger.error(f"Failed to read template: {e}")
        return

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender, password)
        logger.info("Connected to SMTP server.")
    except Exception as e:
        logger.error(f"SMTP Connection failed: {e}")
        return

    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                recipient = row.get('email')
                name = row.get('name', 'User')
                if not recipient:
                    continue
                
                msg = MIMEMultipart()
                msg['From'] = sender
                msg['To'] = recipient
                msg['Subject'] = subject
                
                body = template.replace('{{name}}', name)
                msg.attach(MIMEText(body, 'plain'))
                
                try:
                    server.send_message(msg)
                    logger.info(f"Sent email to {recipient}")
                except Exception as e:
                    logger.error(f"Failed to send email to {recipient}: {e}")
    except Exception as e:
        logger.error(f"Error reading CSV: {e}")
    finally:
        server.quit()
        logger.info("Disconnected from SMTP server.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send bulk emails.")
    parser.add_argument("csv", help="CSV file with columns 'email' and 'name'")
    parser.add_argument("template", help="Text file containing email body template (use {{name}} for replacement)")
    parser.add_argument("subject", help="Email subject")
    parser.add_argument("sender", help="Sender email address")
    parser.add_argument("password", help="Sender email password/app password")
    args = parser.parse_args()
    
    send_bulk_emails(args.csv, args.template, args.subject, args.sender, args.password)
