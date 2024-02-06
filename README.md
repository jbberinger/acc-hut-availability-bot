# ACC HUT Availability Bot

This bot checks if there are any available spots at an ACC hut on a specific day and sends an email via 
Gmail's SMTP server if there are.

Supported huts:
- [Scott Duncan Hut](https://alpine-club-of-canada.checkfront.com/reserve/?category_id=20,21)

## Setup

Create a .env file with the following variables:
```
EMAIL_PASSWORD
SENDER_EMAIL
RECIPIENT_EMAIL
```

## Gmail Setup

In order receive an email from the bot, you will need to create a 16 character app password for your Gmail account by 
visiting [this link](https://myaccount.google.com/apppasswords) and following the instructions. You will need to 
have 2FA enabled on your account to do this.

## Usage
It's recommended to configure a virtual environment for this project. To do so, run the following commands:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

To target a specific date, set the `date_to_check` variable in the `main` function in the format `YYYY-MM-DD`.

The bot sends logs to `hut_availabilty.log` in the root directory.

### Running the bot with a cron
To run the bot every 15 minutes, add the following line to your crontab file:
```
crontab -e
```

```
*/15 * * * * cd /path/to/hut_availability_bot /venv/bin/python3 /path/to/hut_availability_bot/main.py
```
