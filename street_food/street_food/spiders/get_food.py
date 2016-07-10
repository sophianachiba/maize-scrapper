# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from street_food.items import StreetFoodItem, StreetFoodDatTimeItem
from street_food.spiders import tools
import json


class GetFoodYelpCom(scrapy.Spider):
    name = "get-food-yelp"
    allowed_domains = ["yelp.com"]
    base_url = "http://www.yelp.com"

    pages_count = 20    # How much pages to crawl??

    url_pattern = 'http://www.yelp.com/search?find_loc=San+Francisco&start={start}&cflt=streetvendors'

    # Generate urls for crawler, 'pi' is "page index"
    start_urls = (lambda url_pattern=url_pattern, pages_count=pages_count:
                  [url_pattern.format(start=pi) for pi in
                   range(0, pages_count * 10, 10)])()

    def parse(self, response):
        ''' Parse every vendor in search results '''

        vendor_path = '//*[@id="super-container"]/div/div[2]/div[1]/div/div[4]/ul[2]/li[@class="regular-search-result"]'

        for vendor_root in response.xpath(vendor_path):

            vendor_url = vendor_root.xpath('.//a[@class="biz-name js-analytics-click"]/@href').extract()[0]
            vendor_url = self.base_url + vendor_url

            yield Request(vendor_url, callback=self.parse_vendor)

    def parse_vendor(self, response):
        ''' Parse specific vendor '''

        item = StreetFoodItem()

        # Getting shedule, if there is no shedule, skip this item.
        schedule = tools.get_vendor_schedule(response)
        if not schedule:
            self.logger.info("There is no schedule in this vendor, skip it...")
            return
        else:
            item['schedule'] = schedule

        # Getting vendor's name.
        item['VendorName'] = tools.get_vendor_name(response)

        # Getting address.
        item['address'] = tools.get_vendor_address(response)

        # Getting geolocation.
        item['geolocation'] = tools.get_vendor_geolocation(response)

        # Getting phone number.
        item['phone'] = tools.get_vendor_phone(response)

        # Getting website
        item['website'] = tools.get_vendor_website(response)

        yield item


class GetFoodOffTheGrid(scrapy.Spider):
    name = "get-food-offthegrid"
    allowed_domains = ["offthegridmarkets.com", "offthegrid.com"]

    start_urls = [
        'https://offthegrid.com/otg-api/passthrough/markets.json/?latitude=37.7749295&longitude=-122.41941550000001&sort-order=distance-asc'
    ]

    def parse(self, response):
        ''' Parse list of markets '''

        markets = json.loads(response.text)

        market_url = "https://offthegrid.com/otg-api/passthrough/markets/{}.json/"

        # Get list of markets in San Francisco.
        for market in [market for market in markets["Markets"]
                       if market["Market"]["city"] == "San Francisco"]:
            market = market['Market']

            market_id = market['id']

            yield Request(market_url.format(market_id),
                          callback=self.parse_market)

    def parse_market(self, response):
        ''' Parse a market '''

        item = StreetFoodDatTimeItem()

        market = json.loads(response.text)
        market_detail = market["MarketDetail"]["Market"]["Market"]
        market_events = market["MarketDetail"]["Events"]

        # Market Address.
        market_address = market_detail["address"].strip()
        market_city = market_detail["city"].strip()
        full_address = "{} {}".format(market_address, market_city)

        # Market location.
        market_latitude = market_detail['latitude']
        market_longitude = market_detail['longitude']
        geolocation = "{} {}".format(market_latitude, market_longitude)

        # Add data to item.
        item['address'] = full_address
        item['geolocation'] = geolocation

        # Parse market events.
        for event in market_events:
            event_date = "{}.{}".format(event['Event']['month_day'],
                                        event['Event']['year'])

            start_hour = event['Event']['hours'].split("-")[0]
            end_hour = event['Event']['hours'].split("-")[-1]

            start_datetime = "{} {}{}".format(event_date, start_hour,
                                              "-")
            end_datetime = "{} {}{}".format(event_date, end_hour,
                                            event['Event']['am_pm'].lower())

            item['start_datetime'] = start_datetime
            item['end_datetime'] = end_datetime

            # Parse vendors of event.
            for vendor in event['Vendors']:
                vendor_name = vendor['name']

                item['VendorName'] = vendor_name

                yield item
