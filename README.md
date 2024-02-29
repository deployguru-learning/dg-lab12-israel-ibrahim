# Backup and Notification Script

## Features
- **Backup Creation:** The script creates a unique backup directory based on the current date and time and copies the contents of the specified source directory into it.
- **Compression:** After copying the files, the script compresses the backup directory into a zip file for efficient storage.
- **Notification:** Upon completion of the backup process, the script sends a notification via Slack and email to notify the user.

## Dependencies
- Python 3
- Requests library (for Slack notification)
- SMTP library (for email notification)

## Configuration
- **Slack Notification:** To enable Slack notification, update the `webhook_url` variable with the appropriate webhook URL provided by Slack.
- **Email Notification:** To enable email notification, update the `smtp_server`, `smtp_port`, `smtp_username`, `smtp_password`, `from_email`, and `to_email` variables with the appropriate SMTP server details and email addresses.

## Notes
- Make sure the necessary permissions are set for the source and target directories to avoid permission errors during the backup process.
- Ensure that the required Python libraries are installed before executing the script.
- Replace the `to_email` variable with the desired email address or addresses to receive notifications.
- **Using SCP:** Use SCP (Secure Copy Protocol) to push the script file to the server before executing it. Example: `scp <local_script_path> <remote_user>@<server_ip>:<remote_directory_path>`
- **Setting up Cron Job:** To schedule routine backups, set up a cron job to execute the script at specified intervals. Example: `0 0 * * * <path_to_python3_executable> <path_to_script>` for daily backups.
- **Script Location:** The script file should be placed inside the `scripts` folder of the root directory of the LAMP server on AWS. This organization ensures better management and organization of scripts within the server environment