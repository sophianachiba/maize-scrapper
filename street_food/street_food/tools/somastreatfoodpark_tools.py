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
        vendor_name = response.xpath(name_xp).extract_first().strip()
    except IndexError:
        return "null"

    return vendor_name


def make_start_time(raw_time, cur_time):
    time = raw_time.split("-")[0].strip()
    vendor_stime = datetime.strptime(time, "%I%p")
    cur_time = cur_time.replace(hour=vendor_stime.hour,
                                minute=vendor_stime.minute,
                                second=0, microsecond=0)

    return str(cur_time)


def make_end_time(raw_time, cur_time):
    time = raw_time.split("-")[1].strip()
    vendor_etime = datetime.strptime(time, "%I%p")
    cur_time = cur_time.replace(hour=vendor_etime.hour,
                                minute=vendor_etime.minute,
                                second=0, microsecond=0)

    return str(cur_time)


def get_time(response, dinner=False):
    tz = pytz.timezone("US/Pacific")
    cur_time = datetime.now(tz=tz)

    time_xp = '//*[@id="block-yui_3_17_2_29_1430949198032_11012"]/div'
    time_block = response.xpath(time_xp)

    if cur_time.weekday() in range(5):

        if dinner:
            raw_time = time_block.xpath(".//p/text()").extract()[1]
            raw_time = re.sub(r':', '', raw_time)
            raw_time = raw_time[6:]
        else:
            raw_time = time_block.xpath(".//p/text()").extract()[0]
            raw_time = re.sub(r':', '', raw_time)
            raw_time = raw_time[6:]

        start_time = make_start_time(raw_time, cur_time)
        end_time = make_end_time(raw_time, cur_time)

    elif cur_time.weekday() == 5:
        raw_time = time_block.xpath(".//p/text()").extract()[2]
        raw_time = re.sub(r':', '', raw_time)
        raw_time = raw_time[17:]

        start_time = make_start_time(raw_time, cur_time)
        end_time = make_end_time(raw_time, cur_time)

    elif cur_time.weekday() == 6:
        raw_time = time_block.xpath(".//p/text()").extract()[3]
        raw_time = re.sub(r':', '', raw_time)
        raw_time = raw_time[6:]

        start_time = make_start_time(raw_time, cur_time)
        end_time = make_end_time(raw_time, cur_time)

    return start_time, end_time
