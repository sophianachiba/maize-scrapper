import scrapy
from scrapy import Request
import json
from street_food.items import StreetFoodDatTimeItem
import street_food.tools.basic_tools as basic_tools
from street_food.tools.gloungesf_tools import gf_start_time, gf_end_time


class Foodeaze(scrapy.Spider):
    name = "foodeaze"
    api_url = "https://graph.facebook.com/Foodeaze/feed?access_token={}"

    custom_settings = {
        "ITEM_PIPELINES": {
            "street_food.pipelines.ApiUploader": 10,
        }
    }

    def __init__(self):
        super(Foodeaze, self).__init__()

        self.maize_vendors = None
        self.api_key = None

    def start_requests(self):
        self.maize_vendors = basic_tools.get_maize_vendors()
        self.api_key = self.settings.get("FB_API_KEY")

        return [Request(self.api_url.format(self.api_key),
                callback=self.parse)]

    def parse(self, response):
        data = json.loads(response.body)
        last_post = data['data'][1]['message']

        for vendor in self.maize_vendors:
            vname = vendor['name']
            if vname.lower() in last_post.lower():
                yield self.make_item(vname)

    def make_item(self, vendor_name):
        item = StreetFoodDatTimeItem()
        item['VendorName'] = vendor_name
        item['address'] = "350 2nd street San Francisco, CA"
        item['latitude'] = basic_tools.mix_location('37.784487')
        item['longitude'] = basic_tools.mix_location('-122.396100')
        item['start_datetime'] = gf_start_time()
        item['end_datetime'] = gf_end_time()
        item['maize_id'] = basic_tools.maize_api_search(self.maize_vendors,
                                                        vendor_name)
        return item
