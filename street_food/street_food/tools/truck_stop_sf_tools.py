import re
from dateutil import parser
from pytz import timezone
from datetime import datetime


def clean_row(row):
    row = re.sub(r'\n|\(|\)', ' ', row)
    row = re.sub(r'\s+', ' ', row)
    row = row.strip()

    return row


def get_post_events(post, post_time):
    tz = timezone("US/Pacific")
    events = list()

    # We don't have year in messages, so I take year
    # from post timestamp.
    post_year = parser.parse(post_time).year

    rows = re.split(r"(\(\d+/\d+)", post)

    for i, row in enumerate(rows):
        row = clean_row(row)
        try:
            event_date = parser.parse(row)  # Exception!
            event_date = tz.localize(event_date)
            event_date = event_date.replace(year=post_year)

            if event_date.date() >= datetime.now(tz=tz).date():
                event_text = rows[i + 1]
                event_text = clean_row(event_text)

                events.append(dict(event_date=event_date,
                                   event_text=event_text))
        except ValueError:
            pass

    return events
