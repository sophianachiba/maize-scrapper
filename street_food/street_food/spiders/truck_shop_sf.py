import scrapy
from scrapy import Request
import json
from street_food.items import StreetFoodDatTimeItem
import street_food.tools.basic_tools as basic_tools
from street_food.tools.truck_stop_sf_tools import get_post_events
# from pprint import pprint


class TruckStopSf(scrapy.Spider):
    name = "truck-stop-sf"
    api_url = "https://graph.facebook.com/183085105085965/\
posts?access_token={}"

    custom_settings = {
        "ITEM_PIPELINES": {
            "street_food.pipelines.ApiUploader": 10,
        }
    }

    def __init__(self, api_key):
        self.maize_vendors = basic_tools.get_maize_vendors()
        self.api_key = api_key

    @classmethod
    def from_crawler(cls, crawler):
        api_key = crawler.settings.get("FB_API_KEY")
        return cls(api_key)

    def start_requests(self):
        return [Request(self.api_url.format(self.api_key),
                callback=self.parse)]

    def parse(self, response):
        data = json.loads(response.body)

        for post in data['data']:
            post_events = get_post_events(post['message'],
                                          post['created_time'])

            for vendor in self.maize_vendors:
                vname = vendor['name']
                for event in post_events:
                    if vname.lower() in event['event_text'].lower():
                        vdate = event['event_date']
                        yield self.make_item(vname, vdate)

    def make_item(self, vendor_name, vendor_date):

        start_time = vendor_date.replace(hour=11)
        end_time = vendor_date.replace(hour=14)

        item = StreetFoodDatTimeItem()
        item['VendorName'] = vendor_name
        item['address'] = "450 Mission St San Francisco, CA"
        item['latitude'] = basic_tools.mix_location('37.79021200')
        item['longitude'] = basic_tools.mix_location('-122.39725000')
        item['start_datetime'] = str(start_time)
        item['end_datetime'] = str(end_time)
        item['maize_id'] = basic_tools.maize_api_search(self.maize_vendors,
                                                        vendor_name)
        return item
