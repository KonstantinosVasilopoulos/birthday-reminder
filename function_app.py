# Azure Function entry point
import os
import datetime

import azure.functions as func
import logging

import shared.namedays as namedays
import shared.notifier as notifier
import shared.storage as storage

app = func.FunctionApp()


@app.timer_trigger(schedule='0 30 7 * * *', arg_name='timer', run_on_startup=False)
def birthday_reminder(timer: func.TimerRequest) -> None:
    today = datetime.date.today()
    logging.info(f'Executing birthday_reminder function for {today}')

    birthdays_today = storage.get_birthdays_today(today)
    logging.debug(f'Found {len(birthdays_today)} birthday(s) today')
    for birthday in birthdays_today:
        notifier.send_birthday_notification(birthday['Name'])

    upcoming_reminder_days = int(os.environ['UPCOMING_REMINDER_DAYS'])
    upcoming_birthdays = storage.get_birthdays_in_days(today, upcoming_reminder_days)
    logging.debug(f'Found {len(upcoming_birthdays)} birthday(s) in {upcoming_reminder_days} days')
    for birthday in upcoming_birthdays:
        notifier.send_upcoming_birthday_notification(birthday['Name'], upcoming_reminder_days)

    names_today = namedays.get_namedays_today(today)
    logging.debug(f'Found {len(names_today)} name day(s) today')
    if names_today:
        notifier.send_nameday_notification(names_today)

    notifications_sent = len(birthdays_today) + len(upcoming_birthdays) + len(names_today)
    logging.info(f'Finished execution; sent {notifications_sent} notifications')
