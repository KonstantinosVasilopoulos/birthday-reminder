# ntfy notification logic
import os

import requests
import logging


def send_birthday_notification(name: str) -> None:
    """ Sends a birthday notification via ntfy. """
    ntfy_topic = os.environ['NTFY_TOPIC']
    requests.post(
        f'https://ntfy.sh/{ntfy_topic}',
        data=f'It\'s {name}\'s birthday today!',
        headers={'Title': 'Birthday Reminder'}
    )
    logging.info(f'Sent reminder for {name}')


def send_upcoming_birthday_notification(name: str, days: int) -> None:
    """ Sends an upcoming birthday notification via ntfy. """
    ntfy_topic = os.environ['NTFY_TOPIC']
    requests.post(
        f'https://ntfy.sh/{ntfy_topic}',
        data=f'{name}\'s birthday is in {days} days!',
        headers={'Title': 'Upcoming Birthday Reminder'}
    )
    logging.info(f'Sent upcoming reminder for {name} ({days} days away)')


def send_nameday_notification(names: list[str]) -> None:
    """ Sends a name day notification via ntfy. """
    ntfy_topic = os.environ['NTFY_TOPIC']
    names_str = ', '.join(names)
    requests.post(
        f'https://ntfy.sh/{ntfy_topic}',
        data=f'Today is the name day of {names_str}!',
        headers={'Title': 'Name Day Reminder'}
    )
    logging.info(f'Sent name day reminder for {names_str}')
