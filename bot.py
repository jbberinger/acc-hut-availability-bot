import logging
import os

import requests
import smtplib
from datetime import datetime
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from requests.exceptions import HTTPError, RequestException

load_dotenv()

logging.basicConfig(
    filename="hut_availability.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
RECIPIENT_EMAIL = os.environ.get("RECIPIENT_EMAIL")

huts = {
    "SCOTT_DUNCAN_HUT": {
        "name": "Scott Duncan Hut",
        "url": "https://alpine-club-of-canada.checkfront.com/reserve/inventory/?inline=1&header=hide&options=category_select&src=https%3A%2F%2Fwww.alpineclubofcanada.ca&style=color%3A%20000&filter_item_id=50&filter_category_id=13&ssl=1&provider=droplet&filter_item_id=50&customer_id=&original_start_date=&original_end_date=&date={date}&language=&cacheable=1&view=&category_id=13&start_date={date}&end_date={date}&cf-month={cf_month}01&tags%5B%5D=",
        "headers": {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9,fr;q=0.8,es;q=0.7,en-GB;q=0.6,co;q=0.5",
            "cookie": "api=bd58ejva9ir43dlmo5r4k68je3; RES=hopqce0mvmi4dgku3vtck21htq",
            "referer": "https://alpine-club-of-canada.checkfront.com/reserve/?inline=1&category_id=13&item_id=50&options=category_select&style=color%3A%20000&provider=droplet&ssl=1&src=https%3A%2F%2Fwww.alpineclubofcanada.ca&1707023791364",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest",
        },
        "booking_link": "https://alpine-club-of-canada.checkfront.com/reserve/?category_id=20,21",
    }
}


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


def check_hut_availability(hut, target_date):
    """
    Check the availability of a specified hut on a targeted date.

    The following was derived from the "copy cURL" command in Chrome on the ACC
    website when checking the availability of huts.

    The website uses Checkfront to manage the availability of the huts, and their API
    appears to work when provided with the correct headers.
    """
    # Convert the date to YYYYMMDD format for the availability check
    date_formatted = datetime.strptime(target_date, "%Y-%m-%d").strftime("%Y%m%d")

    # Format the date for 'cf-month'
    cf_month = date_formatted[:6] + "01"

    url_template = hut["url"]
    headers = hut["headers"]
    booking_link = hut["booking_link"]
    hut_name = hut["name"]

    url = url_template.format(date=date_formatted, cf_month=cf_month)

    logging.info(f"Checking availability for {hut_name} on {target_date}")

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()

        availability = data.get("calendar_data", {})
        is_available = availability.get(date_formatted, 0) == 1

        if is_available:
            logging.info(f"The {hut_name} is available on {target_date}.")

            subject = f"ACC Hut Availability Bot Alert for {target_date}"
            message = (
                f"The {hut_name} is available on {target_date}!\n\n"
                f"Book here: {booking_link}"
            )
            send_email(subject, message)
        else:
            logging.info(f"The {hut_name} is not available on {target_date}.")

    except HTTPError as e:
        logging.error(
            f"HTTP error occurred: {e} - while checking {hut_name} on {target_date}"
        )
    except RequestException as e:
        logging.error(
            f"Network error occurred: {e} - while checking {hut_name} on {target_date}"
        )
    except Exception as e:
        logging.error(
            f"An error occurred: {e} - while checking {hut_name} on {target_date}"
        )


if __name__ == "__main__":
    hut = huts["SCOTT_DUNCAN_HUT"]
    target_date = "2024-03-14"
    check_hut_availability(hut, target_date)
