import scrapy
from scrapy import Request
import json
from street_food.items import StreetFoodDatTimeItem
import street_food.tools.basic_tools as basic_tools

from street_food.tools.mvblfeast_tools import get_geolocation, get_new_events

import logging

class Mvblfeast(scrapy.Spider):
    name = "mvblfeast"
    fb_api_url = "https://graph.facebook.com/MVBLfeast/events?access_token={}"

    custom_settings = {
        "ITEM_PIPELINES": {
            "street_food.pipelines.ApiUploader": 10,
        }
    }

    def __init__(self, *pargs, **kwargs):
        self.maize_vendors = basic_tools.get_maize_vendors()

        self.fb_api_key = kwargs['fb_api_key']
        self.here_app_id = kwargs['here_app_id']
        self.here_app_code = kwargs['here_app_code']

    @classmethod
    def from_crawler(cls, crawler):
        args = {
            "fb_api_key": crawler.settings.get("FB_API_KEY"),
            "here_app_id": crawler.settings.get("HERE_APP_ID"),
            "here_app_code": crawler.settings.get("HERE_APP_CODE")
        }
        return cls(**args)

    def start_requests(self):
        return [Request(self.fb_api_url.format(self.fb_api_key),
                callback=self.parse)]

    def parse(self, response):
        data = json.loads(response.body)
        # last_event = data['data'][0]
        # desc = last_event['description']

        events = get_new_events(data)

        for event in events:
            desc = event['description']

            for vendor in self.maize_vendors:
                vname = vendor['name']
                if vname.lower() in desc.lower():
                    yield self.make_item(vname, event)

    def make_item(self, vendor_name, last_event):
        event_location = last_event.get("place").get('location', {})

        if 'longitude' in event_location and 'latitude' in event_location:
            latitude = event_location['latitude']
            longitude = event_location['longitude']

        else:
            address = last_event.get("place").get("name")

            latitude, longitude = get_geolocation(address,
                                              self.here_app_id,
                                              self.here_app_code)

        item = StreetFoodDatTimeItem()
        item['VendorName'] = vendor_name
        item['address'] = address
        item['latitude'] = basic_tools.mix_location(latitude)
        item['longitude'] = basic_tools.mix_location(longitude)
        item['start_datetime'] = last_event.get('start_time')
        item['end_datetime'] = last_event.get('end_time')
        item['maize_id'] = basic_tools.maize_api_search(self.maize_vendors,
                                                        vendor_name)
        return item
