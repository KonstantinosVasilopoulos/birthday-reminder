import datetime
import os
import sys

from dotenv import load_dotenv
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import shared.storage as storage

app = FastAPI()
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), 'templates'))


def days_until_birthday(birthday: datetime.datetime) -> int:
    today = datetime.date.today()
    next_birthday = birthday.replace(year=today.year).date()
    if next_birthday < today:
        next_birthday = next_birthday.replace(year=today.year + 1)
    return (next_birthday - today).days


@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    birthdays = storage.get_all_birthdays()
    for b in birthdays:
        b['days_until'] = days_until_birthday(b['Birthday'])
    return templates.TemplateResponse('index.html', {'request': request, 'birthdays': birthdays})


@app.post('/birthdays')
async def create_birthday(name: str = Form(...), birthday: str = Form(...)):
    date = datetime.datetime.strptime(birthday, '%Y-%m-%d')
    table_client = storage._get_table_client()
    table_client.upsert_entity({
        'PartitionKey': f'{date.month:02d}',
        'RowKey': name.lower().replace(' ', '-'),
        'Name': name,
        'Birthday': date,
    })
    table_client.close()
    return RedirectResponse('/', status_code=303)


@app.post('/birthdays/delete')
async def delete_birthday(partition_key: str = Form(...), row_key: str = Form(...)):
    table_client = storage._get_table_client()
    table_client.delete_entity(partition_key=partition_key, row_key=row_key)
    table_client.close()
    return RedirectResponse('/', status_code=303)
