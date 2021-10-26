import datetime
from flask import abort
from ..util import constants 

def format_date(date):
    # return date.strftime("%b %d %Y %H:%M:%S")
    return date.strftime("%d %b, %Y")

def to_date(date):
    try:
        return datetime.datetime.strptime(date, constants.BASIC_DATE_FORMAT).date()
    except Exception as e:
        print(e)
        abort(400)

def add_wrapper(data):
    return {'items': data, 'total': len(data)}

def get_last_month(delay):
    today = datetime.date.today() - datetime.timedelta(days=delay)
    first = today.replace(day=1)
    return first - datetime.timedelta(days=1)