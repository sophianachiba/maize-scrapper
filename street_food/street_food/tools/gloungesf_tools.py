from pytz import timezone
from datetime import datetime

tz = timezone("US/Pacific")


def gf_start_time():
    dt = datetime.now(tz=tz)
    dt = dt.replace(hour=11, minute=0, second=0, microsecond=0)
    return str(dt)


def gf_end_time():
    dt = datetime.now(tz=tz)
    dt = dt.replace(hour=14, minute=0, second=0, microsecond=0)
    return str(dt)
