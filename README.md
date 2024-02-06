# ACC Hut Availability Bot

The ACC Hut Availability Bot is a Python-based tool that checks for available spots at Alpine Club of Canada (ACC) huts
on a specific date and sends an email notification if spots are available. Popular huts often have limited availability
and high demand. This bot aims to assist those holding their breath for cancellations.

## Setup

To set up the bot, create a `.env` file in the root directory with the following variables:

```
EMAIL_PASSWORD=your_gmail_app_password
SENDER_EMAIL=your_email@gmail.com
RECIPIENT_EMAIL=recipient_email@example.com
```

Each variable serves the following purpose:

- `EMAIL_PASSWORD`: The 16-character app password for your Gmail account.
- `SENDER_EMAIL`: The email address that will send the notification.
- `RECIPIENT_EMAIL`: The email address that will receive the notification.

## Gmail Setup

To receive an email from the bot, create a 16-character app password for your Gmail account. This requires 2FA (
Two-Factor Authentication) to be enabled on your account. Follow these steps:

1. Visit [App Passwords](https://myaccount.google.com/apppasswords).
2. Follow the instructions to generate a new app password.
3. Add this password to your `.env` file as `EMAIL_PASSWORD`.

Customize the subject and body of the email in the `send_email` function in `bot.py`.

## Usage

It's recommended to use a virtual environment for this project. Run the following commands to set up:

```bash
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Set the `target_date` variable in the `if __name__ == "__main__":` section in `bot.py` to the desired date in the
format `YYYY-MM-DD`.

Logs are saved to `hut_availability.log` in the root directory.

## Adding Huts to the Script

The `huts` dictionary in `bot.py` contains configurations for each hut, including names, URLs, headers, and booking
links. Add or remove huts as needed.

### Getting the Hut API Data

For example, to add the Scott Duncan Hut:

1. Go to the [Scott Duncan Hut ACC page](https://www.alpineclubofcanada.ca/scott-duncan-hut/) and click the "Booking"
   tab.
2. Open Chrome Developer Tools and select the "Network" tab.
3. Click the desired date on the date picker and observe the network request that appears.
4. Right-click the request and select "Copy" > "Copy as cURL (bash)".
5. Extract the URL and headers from the copied cURL command.

The default configuration for the Scott Duncan Hut is included but may need updating due to cookie expiration.

## Running the Bot with Cron

To run the bot every 15 minutes using cron:

1. Open your crontab file with `crontab -e`.
2. Add the following line:

   ```
   */15 * * * * cd /path/to/acc-hut-availability-bot && ./venv/bin/python3 bot.py
   ```

This will execute `bot.py` from the specified directory every 15 minutes. Ensure the path is correct for your setup.

## Troubleshooting

If you encounter issues, check the following:

- Ensure all dependencies are installed and the virtual environment is activated.
- Verify that the `.env` file contains the correct email credentials.
- Check `hut_availability.log` for error messages.
