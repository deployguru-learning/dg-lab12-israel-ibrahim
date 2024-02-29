import os
import subprocess
from datetime import datetime
import smtplib
import requests
import shutil
import json
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email import encoders

# Configure logging
logging.basicConfig(filename='backup.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_backup_directory(source_directory, target_directory):
    """Create a unique backup directory."""
    backup_directory_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_directory_path = os.path.join(target_directory, backup_directory_name)
    os.makedirs(backup_directory_path, exist_ok=True)
    return backup_directory_path

def copy_files(source_directory, backup_directory_path):
    """Copy contents from source directory to backup directory."""
    try:
        subprocess.run(['cp', '-r', source_directory, backup_directory_path])
        logging.info("Backup completed successfully!")
    except subprocess.CalledProcessError as error:
        logging.error(f'Error during backup: {error}')
    except Exception as error:
        logging.error(f'Something went wrong: {error}')

def compress_directory(backup_directory_path, target_directory):
    """Compress backup directory into a zip file."""
    try:
        zip_file_name = os.path.basename(backup_directory_path) + '.zip'
        zip_file_path = os.path.join(target_directory, zip_file_name)
        shutil.make_archive(backup_directory_path, 'zip', backup_directory_path)
        os.rename(backup_directory_path + ".zip", zip_file_path)
        logging.info("Backup directory compressed into a zip file")
    except Exception as error:
        logging.error(f'Error compressing directory: {error}')

def remove_directory(backup_directory_path):
    """Remove the temporary backup directory."""
    try:
        shutil.rmtree(backup_directory_path)
        logging.info("Temporary directory removed")
    except Exception as error:
        logging.error(f'Error removing directory: {error}')

def send_slack_notification(webhook_url, message_content):
    """Send a notification via Slack."""
    message_payload = {"text": f"```\n{json.dumps(message_content, indent = 4)}\n```"}
    response = requests.post(webhook_url, json = message_payload)
    if response.status_code == 200:
        logging.info('Slack message sent successfully')
    else:
        logging.error(f'Failed to send Slack message, status code: {response.status_code}')

def send_email_notification(from_email, to_email, subject, body, csv_data=None, cc=None):
    try:
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = 'israel7manuel@gmail.com'
        smtp_password = 'nlol mujs xssw rpon'

        # Create a multipart message
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = ', '.join(to_email)
        msg['Subject'] = subject

        # Add CC recipients if provided
        if cc:
            msg['Cc'] = ', '.join(cc)
            to_email += cc

        # Add body to email
        msg.attach(MIMEText(body, 'plain'))

        # Attach CSV file
        if csv_data:
            # Convert CSV data to string
            csv_content = '\n'.join([','.join(row) for row in csv_data])

            attachment = MIMEBase('text', 'csv')
            attachment.set_payload(csv_content.encode('utf-8'))
            attachment.add_header('Content-Disposition', f'attachment; filename="{subject}.csv"')
            encoders.encode_base64(attachment)
            msg.attach(attachment)

        # Connect to SMTP server and send email
        with smtplib.SMTP(smtp_server, smtp_port) as smtp:
            smtp.starttls()
            smtp.login(smtp_username, smtp_password)
            smtp.sendmail(from_email, to_email, msg.as_string())

        logging.info('Email sent successfully!')
    except Exception as e:
        logging.error(f'Error sending email: {e}')

# Current time
current_time = datetime.now().strftime("%a %d/%m/%Y %I:%M %p IST")
# Define the directory paths
source_directory = "/var/www/html/"
target_directory = "/opt/backups"

# Create backup directory
backup_directory_path = create_backup_directory(source_directory, target_directory)
logging.info("Backup directory created: %s", backup_directory_path)

# Copy files
copy_files(source_directory, backup_directory_path)

# Compress directory
compress_directory(backup_directory_path, target_directory)

# Remove temporary directory
remove_directory(backup_directory_path)

# Send Slack notification
webhook_url = 'https://hooks.slack.com/services/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'
message_content = {
    'notification_by': 'Israel Immanuel',
    'backup_time': f'{current_time}',
    'backup_path': f'{backup_directory_path}'
}

send_slack_notification(webhook_url, message_content)

# Send email notification
from_email = 'israel7manuel@gmail.com'
to_email = ['israel7payment@gmail.com', '64f8221be51d53cf7a9f7db1@gmail.com']
cc = ['64f8221be51d53cf7a9f7db1@gmail.com']
subject = 'Backup Complete'
body = f'Completed time {current_time}. Backup directory path: {backup_directory_path}. Attached is a csv file with additional information.'

csv_data = [['From', 'To', 'time'], ['israel7manuel@gmail.com', 'felix@deployguru.com', f'{current_time}'],
            ['israel7manuel@gmail.com', 'israel7payment@gmail.com', f'{current_time}']]

send_email_notification(from_email, to_email, subject, body, csv_data, cc)
