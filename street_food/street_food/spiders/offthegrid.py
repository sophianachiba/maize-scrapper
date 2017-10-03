# -*- coding: utf-8 -*-
from __future__ import division

import logging
import datetime
import scrapy
from scrapy import Request
# from street_food.items import StreetFoodItem, StreetFoodDatTimeItem
from street_food.items import StreetFoodDatTimeItem
from street_food.spiders import tools
import json
from urllib import urlopen
# import random
from street_food.tools import basic_tools


class GetFoodOffTheGrid(scrapy.Spider):
    name = "offthegrid"
    allowed_domains = ["offthegridmarkets.com", "offthegrid.com", "api.infrastruckture.com"]

    #     start_urls = [
    # #        'https://offthegrid.com/otg-api/passthrough/markets.json/?latitude=37.7749295&longitude=-122.41941550000001&sort-order=distance-asc'
    #         'https://api.infrastruckture.com/locations?latitude=37.7749295&longitude=-122.41941550000001&sort-order=distance-asc&radius=10'
    #     ]

    custom_settings = {
        "ITEM_PIPELINES": {
            "street_food.pipelines.ApiUploader": 10,
        }
    }

    authorization_header = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJJbmZyYXN0cnVja3R1cmUiLCJpYXQiOjE1MDU0MTQ4ODYsImV4cCI6MTUwODAwNjg4NiwiYXVkIjoiaW5mcmFzdHJ1Y2t0dXJlLmNvbSIsInN1YiI6Ijc3NjczZTUxLWIxY2UtNDg2OS05Yjg0LWQyZDQ0YmMxMzFhNCIsIm9yZyI6ImZrSFZzSnA4ZmtxTEo0VllnMkxZeUN1SFJMRGQ5TTBOQzArVGl0MVBjcDlFOHpmcSIsImp0aSI6InB1YmxpYy1hcGkifQ.lvYfPWszTo52DB9gGziHQ928Kp9TnGu - fRAhcneYEj4"

    def start_requests(self):
        urls = [
            "https://api.infrastruckture.com/locations?latitude=37.7749295&longitude=-122.41941550000001&radius=10"
        ]

        for url in urls:
            yield Request(url=url, headers={
                'authorization': GetFoodOffTheGrid.authorization_header,
                'Referer': 'https://offthegrid.com'
            })

    def parse(self, response):
        ''' Parse list of markets '''

        if response.status == 400:
            return

        markets = json.loads(response.text)

        if markets['status'] != 'success':
            return

        market_url = "https://api.infrastruckture.com/events?locationId={}&dateTo={}&dateFrom={}"

        # Get list of markets in San Francisco.
        for market in markets['data']['locations']:
            market_id = market['id']

            assert 'address1' in market

            yield Request(url=market_url.format(
                market_id,
                '%i' % basic_tools.get_date_millis(datetime.datetime.now() + datetime.timedelta(days=7)),
                '%i' % basic_tools.get_date_millis(datetime.datetime.now()),
            ),
                callback=self.parse_market,
                headers={
                    'authorization': GetFoodOffTheGrid.authorization_header,
                    'Referer': 'https://offthegrid.com'
                },
                meta={'market': market}
            )

    def parse_market(self, response):
        ''' Parse a market '''

        # Load market detail from meta
        market_detail = response.meta['market']

        # Load market data from response
        market_data = json.loads(response.text)

        # Load market events from response
        market_events = market_data['data']['events']

        # Parse market events.
        for event in market_events:

            event_url = 'https://api.infrastruckture.com/events/{}'

            yield Request(url=event_url.format(event['id']),
                callback=self.parse_event,
                headers={
                    'authorization': GetFoodOffTheGrid.authorization_header,
                    'Referer': 'https://offthegrid.com'
                },
                meta={'market_detail': market_detail, 'event': event}
            )


    def parse_event(self, response):

        # Load event data from response
        event = json.loads(response.text)
        event_detail = event['data']['event']

        event_vendors = event_detail['services']

        # load Maize Vendors.
        maizeresp = urlopen('http://yumbli.herokuapp.com/api/v1/allkitchens/?format=json')
        vendors = json.loads(maizeresp.read().decode('utf8'))
        maizevendors = {}
        for v in vendors:
            maizevendors[v['name'].lower()] = v['id']

        # Market details
        market_detail = response.meta['market_detail']

        if market_detail["address1"] is None:
            market_detail["address1"] = ""

        if market_detail["address2"] is None:
            market_detail["address2"] = ""

        # Build market full address
        market_address = market_detail["address1"].strip() + market_detail["address2"].strip()
        market_city = market_detail["city"].strip()
        full_address = "{} {}".format(market_address, market_city)

        # Market location.
        market_latitude = market_detail['latitude']
        market_longitude = market_detail['longitude']
        # geolocation = "{} {}".format(market_latitude, market_longitude)

        # Add data to item.
        item = StreetFoodDatTimeItem()
        item['address'] = full_address
        
        # start_datetime, end_datetime = tools.get_start_end_datetime(event['Event'])
        start_datetime = event_detail['startTime']
        end_datetime = event_detail['endTime']

        item['start_datetime'] = start_datetime
        item['end_datetime'] = end_datetime

        # Parse vendors of event.
        for vendor in event_vendors:
            vendor_name = vendor['vendor']['name']
            item['VendorName'] = vendor_name
            # randlongpos = random.randint(-150, 150) / 1000000
            # randlatpos = random.randint(-200, 200) / 1000000

            # item['latitude'] = abs(float(market_latitude)) + randlatpos
            # abs then *-1 b/c off the grid has some wrong values
            # item['longitude'] = abs(float(market_longitude))*-1 + randlongpos

            item['latitude'] = basic_tools.mix_location(market_latitude)
            item['longitude'] = basic_tools.mix_location(market_longitude)

            if vendor_name and vendor_name.lower() in maizevendors.keys():
                item['maize_status'] = 'found'
                item['maize_id'] = maizevendors[vendor_name.lower()]
            else:
                item['maize_status'] = 'not found'
                item['maize_id'] = 'n/a'

            yield item