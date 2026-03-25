# Azure Table Storage interactions
import os
import datetime

from azure.data.tables import TableServiceClient


def _get_table_client():
    storage_connection_string = os.environ['STORAGE_CONNECTION_STRING']
    return TableServiceClient.from_connection_string(storage_connection_string).get_table_client('birthdays')


def get_birthdays_today(today: datetime.date) -> list:
    """ Queries the Azure Storage Account's table to retrieve the people whose birthday is today. """
    table_client = _get_table_client()

    month = f'{today.month:02d}'
    entities = table_client.query_entities(f"PartitionKey eq '{month}'")
    birthdays_today = [e for e in entities if e['Birthday'].month == today.month and e['Birthday'].day == today.day]

    table_client.close()
    return birthdays_today


def get_all_birthdays() -> list:
    """ Queries the Azure Storage Account's table to retrieve all birthday records. """
    table_client = _get_table_client()
    entities = list(table_client.list_entities())
    table_client.close()
    return sorted(entities, key=lambda e: (e['Birthday'].month, e['Birthday'].day))


def get_birthdays_in_days(today: datetime.date, days: int) -> list:
    """ Queries the Azure Storage Account's table to retrieve people whose birthday is in exactly `days` days. """
    table_client = _get_table_client()
    target = today + datetime.timedelta(days=days)

    month = f'{target.month:02d}'
    entities = table_client.query_entities(f"PartitionKey eq '{month}'")
    upcoming = [e for e in entities if e['Birthday'].month == target.month and e['Birthday'].day == target.day]

    table_client.close()
    return upcoming
