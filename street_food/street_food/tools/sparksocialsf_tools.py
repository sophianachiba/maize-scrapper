import bs4
import pytz
from datetime import datetime

import re
import logging

logger = logging.getLogger()
time_re = re.compile(r'(.*)-\s*([^\s]*).*')

def get_vendor_name(response):
    try:
        name_xp = ".//a[@class='summary-title-link']/text()"
        name = response.xpath(name_xp).extract()[0]
    except IndexError:
        name = None

    return name


def get_address(response):
    try:
        addr_xp = "//h2[contains(text(), 'Location')]/following-sibling::p"
        address = response.xpath(addr_xp).extract()[0]

        soup = bs4.BeautifulSoup(address, "lxml")
        address = soup.get_text(strip=True, separator=' ')

    except IndexError:
        address = None

    return address


def make_start_time(raw_time, cur_time):
    logging.debug("Raw time: {}".format(raw_time))

    time_re_match = time_re.match(raw_time)

    if not time_re_match:
        return ""

    time = time_re_match.group(1).strip() + "m"

    logging.debug("Start time: {}".format(time))

    # time = raw_time.split("-")[0].strip() + "m"
    vendor_stime = datetime.strptime(time, "%I:%M%p")
    cur_time = cur_time.replace(hour=vendor_stime.hour,
                                minute=vendor_stime.minute,
                                second=0, microsecond=0)
    return str(cur_time)


def make_end_time(raw_time, cur_time):

    time_re_match = time_re.match(raw_time)

    if not time_re_match:
        return ""

    time = time_re_match.group(2).strip() + "m"

    logging.debug("End time: {}".format(time))

    # time = raw_time.split("-")[1].strip() + "m"
    vendor_stime = datetime.strptime(time, "%I:%M%p")
    cur_time = cur_time.replace(hour=vendor_stime.hour,
                                minute=vendor_stime.minute,
                                second=0, microsecond=0)
    print("CURTIME", cur_time)
    return str(cur_time)


def get_time(response, dinner=False):
    tz = pytz.timezone("US/Pacific")
    cur_time = datetime.now(tz=tz)

    if cur_time.weekday() in range(5):
        time_xp = "//h2[contains(text(), 'Weekdays')]/following-sibling::p/text()"
        if dinner:
            raw_time = response.xpath(time_xp).extract()[1]
            start_time = make_start_time(raw_time, cur_time)
            end_time = make_end_time(raw_time, cur_time)
        else:
            raw_time = response.xpath(time_xp).extract()[0]
            start_time = make_start_time(raw_time, cur_time)
            end_time = make_end_time(raw_time, cur_time)

    elif cur_time.weekday() == 5:
        time_xp = "//h2[contains(text(), 'Weekends')]/following-sibling::p/text()"
        raw_time = response.xpath(time_xp).extract()[0]
        start_time = make_start_time(raw_time, cur_time)
        end_time = make_end_time(raw_time, cur_time)

    elif cur_time.weekday() == 6:
        time_xp = "//h2[contains(text(), 'Weekends')]/following-sibling::p/text()"
        raw_time = response.xpath(time_xp).extract()[1]
        start_time = make_start_time(raw_time, cur_time)
        end_time = make_end_time(raw_time, cur_time)

    else:
        start_time = end_time = None

    return start_time, end_time
