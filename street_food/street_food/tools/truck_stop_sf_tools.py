import re
from dateutil import parser
from pytz import timezone
from datetime import datetime


def clean_row(row):
    row = re.sub(r'\n|\(|\)', ' ', row)
    row = re.sub(r'\s+', ' ', row)
    row = row.strip()

    return row


def get_post_events(post):
    tz = timezone("US/Pacific")
    events = list()

    rows = re.split(r"(\(\d+/\d+)", post)

    for i, row in enumerate(rows):
        row = clean_row(row)
        try:
            event_date = parser.parse(row)  # Exception!
            event_date = tz.localize(event_date)

            if (event_date.date() >= datetime.now(tz=tz).date() and
               event_date.date().month - datetime.now(tz=tz).date().month <= 2):

                event_text = rows[i + 1]
                event_text = clean_row(event_text)

                events.append(dict(event_date=event_date,
                                   event_text=event_text))
        except ValueError:
            pass

    return events
