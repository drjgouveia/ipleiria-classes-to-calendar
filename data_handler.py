import re
import json

import pytz
from ics import Calendar, Event
from datetime import datetime, timedelta


def convert_date_to_current_week(date):
    given_date = datetime.strptime(date.replace(" +0000", ""), "%B %d, %Y %H:%M:%S")
    today = datetime.utcnow()
    day_of_week = given_date.weekday()
    date_in_current_week = given_date + timedelta(days=abs(given_date.date() - today.date()).days + (day_of_week - today.weekday()))
    date_in_current_week = date_in_current_week - timedelta(hours=1)  # this is to correct for the timezone difference
    if date_in_current_week < today:
        date_in_current_week = date_in_current_week + timedelta(days=7)

    return date_in_current_week


def convert_to_events(json_data):
    cal = Calendar()
    for item in json_data:
        try:
            event = Event()
            event.name = item["Text"]
            event.begin = convert_date_to_current_week(item["Start"])
            event.end = convert_date_to_current_week(item["End"])
            event.description = ""
            event.location = ""
            cal.events.add(event)
        except Exception as e:
            print(e)

    return cal


def extract_json_from_request_data(data):
    try:
        pattern = r'c\.events\s*=\s*(\[[^\]]+\])'
        matches = re.search(pattern, data)
        if matches:
            json_data = matches.group(1)
            parsed_data = json.loads(json_data)
            return parsed_data
        else:
            return None
    except Exception as e:
        print(e)
        return None
