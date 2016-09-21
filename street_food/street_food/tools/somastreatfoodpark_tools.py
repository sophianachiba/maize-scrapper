import bs4
import pytz
from datetime import datetime
import re


def get_address(response):
    address_xp = "//strong[contains(text(), 'Location')]/parent::p"
    try:
        raw_location = response.xpath(address_xp).extract()[0]

        soup = bs4.BeautifulSoup(raw_location, "lxml")
        address = soup.get_text(strip=True, separator=' ')
    except IndexError:
        address = "null"

    return address


def get_vendor_name(response):
    try:
        name_xp = ".//div[@class='summary-title']/a/text()"
        vendor_name = response.xpath(name_xp).extract_first()
    except IndexError:
        return "null"

    return vendor_name


def make_start_time(raw_time, cur_time):
    vendor_stime = datetime.strptime(raw_time.split("-")[0], "%I:%M%p")
    cur_time = cur_time.replace(hour=vendor_stime.hour,
                                minute=vendor_stime.minute)

    return str(cur_time)


def make_end_time(raw_time, cur_time):
    vendor_etime = datetime.strptime(raw_time.split("-")[1], "%I:%M%p")
    cur_time = cur_time.replace(hour=vendor_etime.hour,
                                minute=vendor_etime.minute)

    return str(cur_time)


def parse_time(raw_time):
    workdays = raw_time.split("/")[0].strip()[16:]
    workdays = re.sub(r'\s', '', workdays)

    saturday = raw_time.split("/")[1].split("|")[0].strip()[10:]
    saturday = re.sub(r'\s', '', saturday)

    sunday = raw_time.split("/")[1].split("|")[1].strip()[8:]
    sunday = re.sub(r'\s', '', sunday)

    tz = pytz.timezone("US/Pacific")
    cur_time = datetime.now(tz=tz)

    if cur_time.weekday() in range(5):
        start_time = make_start_time(workdays, cur_time)
        end_time = make_end_time(workdays, cur_time)

    elif cur_time.weekday() == 5:
        start_time = make_start_time(saturday, cur_time)
        end_time = make_end_time(saturday, cur_time)

    elif cur_time.weekday() == 6:
        start_time = make_start_time(sunday, cur_time)
        end_time = make_end_time(sunday, cur_time)

    return start_time, end_time
