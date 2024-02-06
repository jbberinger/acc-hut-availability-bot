import logging
import os

import requests
import smtplib
from datetime import datetime
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

logging.basicConfig(
    filename="hut_availability.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
RECIPIENT_EMAIL = os.environ.get("RECIPIENT_EMAIL")


def send_email(subject, message, recipient_email=RECIPIENT_EMAIL):
    """
    Send an email using Gmail's SMTP server.
    """

    msg = MIMEMultipart()
    msg.attach(MIMEText(message, "plain"))

    msg["From"] = SENDER_EMAIL
    msg["To"] = recipient_email
    msg["Subject"] = subject

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(SENDER_EMAIL, EMAIL_PASSWORD)
        server.send_message(msg)


def check_scott_duncan_hut_availability(date_to_check):
    """
    Check the availability of the Scott Duncan Hut on a specific date.

    The following was derived from the "copy cURL" command in Chrome on the ACC
    website when checking the availability of the Scott Duncan Hut.

    The website uses Checkfront to manage the availability of the huts, and their API
    appears to work when provided with the correct headers.
    """
    # Convert the date to YYYYMMDD format for the availability check
    date_formatted = datetime.strptime(date_to_check, "%Y-%m-%d").strftime("%Y%m%d")

    # URL specific to the Scott Duncan Hut
    url = f"https://alpine-club-of-canada.checkfront.com/reserve/inventory/?inline=1&header=hide&options=category_select&src=https%3A%2F%2Fwww.alpineclubofcanada.ca&style=color%3A%20000&filter_item_id=50&filter_category_id=13&ssl=1&provider=droplet&filter_item_id=50&customer_id=&original_start_date=&original_end_date=&date={date_to_check}&language=&cacheable=1&view=&category_id=13&start_date={date_to_check}&end_date={date_to_check}&cf-month={date_formatted[:6]}01&tags%5B%5D="

    # Headers extracted from the cURL command
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9,fr;q=0.8,es;q=0.7,en-GB;q=0.6,co;q=0.5",
        "cookie": "api=bd58ejva9ir43dlmo5r4k68je3; RES=hopqce0mvmi4dgku3vtck21htq",
        "referer": "https://alpine-club-of-canada.checkfront.com/reserve/?inline=1&category_id=13&item_id=50&options=category_select&style=color%3A%20000&provider=droplet&ssl=1&src=https%3A%2F%2Fwww.alpineclubofcanada.ca&1707023791364",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest",
    }

    logging.info(f"Checking availability for Scott Duncan Hut on {date_to_check}")

    # Send the GET request
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Check availability from the calendar_data
        availability = data.get("calendar_data", {})
        is_available = availability.get(date_formatted, 0) == 1

        if is_available:
            logging.info(f"The Scott Duncan Hut is available on {date_to_check}.")

            subject = f"Scott Duncan Hut Availability Alert {date_to_check}"
            message = (
                f"The Scott Duncan Hut is available on {date_to_check}!\n\n"
                f"Book here: https://alpine-club-of-canada.checkfront.com/reserve/?category_id=20,21"
            )
            send_email(subject, message)
        else:
            logging.info(f"The Scott Duncan Hut is not available on {date_to_check}.")

    else:
        logging.error(f"Failed to retrieve data: {response.status_code}")


if __name__ == "__main__":
    check_scott_duncan_hut_availability("2024-03-14")
