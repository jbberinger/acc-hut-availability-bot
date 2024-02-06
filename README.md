# ACC HUT Availability Bot

This bot checks if there are any available spots at an ACC hut on a specific day and sends an email via 
Gmail's SMTP server if there are.

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
have 2FA enabled on your account to do this. Add this password to your .env file as `EMAIL_PASSWORD`.

The subject and body of the email can be customized in the `send_email` function in `bot.py`.

## Usage
It's recommended to configure a virtual environment for this project. To do so, run the following commands:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

To target a specific date, set the `date_to_check` variable in the `main` function in the format `YYYY-MM-DD`.

The bot sends logs to `hut_availabilty.log` in the root directory.

## Adding Huts to the Script
The `huts` dictionary in `bot.py` contains the names of the huts and their respective URLs and headers. You can add or remove huts
from this dictionary as you see fit.

### Getting the hut API data you need using Chrome

Using the Scott Duncan hut as an example, navigate to the hut's [ACC page](https://www.alpineclubofcanada.ca/scott-duncan-hut/)
and click the "Booking" tab. Open the Chrome developer tools and click the "Network" tab. Click the date you want to
check from the date picker and notice the network request that is made. It should look something like:
```
https://alpine-club-of-canada.checkfront.com/reserve/inventory/?inline...
```
Right click the request and click "Copy" -> "Copy as cURL (bash)". Paste the cURL command into a text editor and
extract the URL and headers needed to make the request. The Scott Duncan hut comes default in bot.py but may require 
updating due to cookie expiration.

### Running the bot with a cron
To run the bot every 15 minutes, add the following line to your crontab file:
```
crontab -e
```

```
*/15 * * * * cd /path/to/acc-hut-availability-bot && /venv/bin/python3 bot.py
```
