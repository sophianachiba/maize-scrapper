import json


def get_vendor_schedule(resp):
    schedule_xpath = '//*[@id="super-container"]/div/div/div[2]/div[2]\
                      /div[1]/table'
    schedule = resp.xpath(schedule_xpath)

    if not schedule:
        return None  # Vendor don't have schedule, skip it.

    schedule_buff = list()

    for schedule_row in schedule.xpath('.//tr'):
        # Getting work day
        day = schedule_row.xpath('.//th/text()').extract()[0]

        # Getting work hours.
        open_hour = schedule_row.xpath('.//td[1]/span[1]/text()').extract()
        close_hour = schedule_row.xpath('.//td[1]/span[2]/text()').extract()

        # If have open hours.
        if open_hour and close_hour:
            item_address = "{} {} - {}".format(day, open_hour[0],
                                               close_hour[0])
        # If close for this day.
        else:
            item_address = "{}: closed".format(day)

        schedule_buff.append(item_address)

    schedule_buff = str.join("; ", schedule_buff)

    return schedule_buff


def get_vendor_name(resp):
    name_xpath = '//*[@id="wrap"]/div[3]/div/div[1]/div/div[2]/div[1]\
                  /div[1]/h1/text()'
    vendor_name = resp.xpath(name_xpath).extract()[0].strip()

    return vendor_name


def get_vendor_address(resp):
    street_addr_path = '//*[@id="wrap"]/div[3]/div/div[1]/div/div[3]/div[1]\
                        /div/div[2]/ul/li[1]/div/strong/address/span[1]/text()'
    city_addr_path = '//*[@id="wrap"]/div[3]/div/div[1]/div/div[3]/div[1]\
                      /div/div[2]/ul/li[1]/div/strong/address/span[2]/text()'

    street = resp.xpath(street_addr_path).extract()[0].strip()
    city = resp.xpath(city_addr_path).extract()[0].strip()

    address = "{}/{}".format(street, city)

    return address


def get_vendor_geolocation(resp):
    location_xpath = '//*[@id="wrap"]/div[3]/div/div[1]/div/div[3]/div[1]\
                      /div/div[1]/div/@data-map-state'
    location = resp.xpath(location_xpath).extract()[0]
    map_data = json.loads(location)

    latitude = map_data['center']['latitude']
    longitude = map_data['center']['longitude']

    geolocation = "{} {}".format(latitude, longitude)

    return geolocation


def get_vendor_phone(resp):
    phone_xpath = './/span[@class="biz-phone"]/text()'
    phone = resp.xpath(phone_xpath).extract()
    if phone:
        phone = phone[0].strip()
        return phone

    return ""


def get_vendor_website(resp):
    website_xpath = './/span[@class="biz-website"]/a/text()'
    website = resp.xpath(website_xpath).extract()
    if website:
        website = website[0].strip()
        return website

    return ""
