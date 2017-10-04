import requests
from dateutil import parser
from pytz import timezone
from datetime import datetime


def get_geolocation(addr, app_id, app_code):
    if not addr:
        return None, None

    resp = requests.get("""https://geocoder.cit.api.here.com/6.2/geocode.json?\
searchtext={addr}&app_id={app_id}&app_code={app_code}""".format(addr=addr, app_id=app_id, app_code=app_code)).json()

    try:

        # {u'Latitude': 37.2928228, u'Longitude': -121.8741757}
        resp = resp['Response']['View'][0]['Result'][0]['Location']

        lat = resp['DisplayPosition']['Latitude']
        long = resp['DisplayPosition']['Longitude']

        return lat, long

    except (KeyError, IndexError):
        pass

    return None, None


def get_new_events(resp):
    tz = timezone("US/Pacific")
    cur_time = datetime.now(tz=tz)

    events = list()

    for event in resp['data']:
        event_end_time = parser.parse(event['end_time'])

        if event_end_time > cur_time:
            events.append(event)

    return events
