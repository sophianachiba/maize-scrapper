# -*- coding: utf-8 -*-
from __future__ import division
import scrapy
from scrapy import Request
from street_food.items import StreetFoodItem, StreetFoodDatTimeItem
from street_food.spiders import tools
import json
from urllib import urlopen
import random


class GetFoodOffTheGrid(scrapy.Spider):
    name = "offthegrid"
    allowed_domains = ["offthegridmarkets.com", "offthegrid.com"]

    start_urls = [
        'https://offthegrid.com/otg-api/passthrough/markets.json/?latitude=37.7749295&longitude=-122.41941550000001&sort-order=distance-asc'
    ]

    custom_settings = {
        "ITEM_PIPELINES": {
            "street_food.pipelines.ApiUploader": 10,
        }
    }

    def parse(self, response):
        ''' Parse list of markets '''

        markets = json.loads(response.text)

        market_url = "https://offthegrid.com/otg-api/passthrough/markets/{}.json/"

        # Get list of markets in San Francisco.
        for market in [market for market in markets["Markets"]]:
            market = market['Market']

            market_id = market['id']

            yield Request(market_url.format(market_id),
                          callback=self.parse_market)

    def parse_market(self, response):
        ''' Parse a market '''

        # load Maize Vendors.
        maizeresp = urlopen('http://yumbli.herokuapp.com/api/v1/allkitchens/?format=json')
        vendors = json.loads(maizeresp.read().decode('utf8'))
        maizevendors = {}
        for v in vendors:
           maizevendors[v['name'].lower()] = v['id']


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

        # Parse market events.
        for event in market_events:

            start_datetime, end_datetime = tools.get_start_end_datetime(event['Event'])

            item['start_datetime'] = start_datetime
            item['end_datetime'] = end_datetime

            # Parse vendors of event.
            for vendor in event['Vendors']:
                vendor_name = vendor['name']
                item['VendorName'] = vendor_name
                randlongpos = random.randint(-150, 150) / 1000000
                randlatpos = random.randint(-200, 200) / 1000000
                item['latitude'] = abs(float(market_latitude)) + randlatpos
                # abs then *-1 b/c off the grid has some wrong values
                item['longitude'] = abs(float(market_longitude))*-1 + randlongpos
                if vendor_name and vendor_name.lower() in maizevendors.keys() :
                    item['maize_status'] = 'found'
                    item['maize_id'] = maizevendors[vendor_name.lower()]
                else:
                    item['maize_status'] = 'not found'
                    item['maize_id'] = 'n/a'

                yield item
