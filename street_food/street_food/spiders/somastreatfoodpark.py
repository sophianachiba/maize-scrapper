# -*- coding: utf-8 -*-
import scrapy
import street_food.tools.somastreatfoodpark_tools as tools
from street_food.items import StreetFoodDatTimeItem
import street_food.tools.basic_tools as basic_tools
from scrapy import Request


class SomastreatfoodparkSpider(scrapy.Spider):
    name = "somastreatfoodpark"
    allowed_domains = ["www.somastreatfoodpark.com/"]

    custom_settings = {
        "ITEM_PIPELINES": {
            # "street_food.pipelines.ApiUploader": 10,
        }
    }

    def start_requests(self):
        url = 'http://www.somastreatfoodpark.com/'

        yield Request(url, callback=self.parse_lunch_vendors)
        yield Request(url, callback=self.parse_dinner_vendors,
                      dont_filter=True)

    def __init__(self, *pargs, **kwargs):
        scrapy.Spider.__init__(self, *pargs, **kwargs)

        self.maize_vendors = basic_tools.get_maize_vendors()

    def parse_lunch_vendors(self, response):
        address = tools.get_address(response)

        # ---- Lunch time vendors ---- #
        vendors_xp = '//h2[contains(text(), "Today\'s Lunch Time Vendors")]'
        vendors = response.xpath(vendors_xp)

        start_dtime, end_dtime = tools.get_time(response)

        # Vendors list block.
        vblock_xp = './parent::div/parent::div/following-sibling::div'
        vendors_block = vendors.xpath(vblock_xp)[0]
        vlist_xp = ".//div[contains(@class, 'summary-item\n')]"
        for vendor in vendors_block.xpath(vlist_xp):

            item = StreetFoodDatTimeItem()

            vendor_name = tools.get_vendor_name(vendor)

            item['VendorName'] = vendor_name
            item['address'] = address
            item['latitude'] = basic_tools.mix_location('37.769782')
            item['longitude'] = basic_tools.mix_location('-122.411848')
            item['start_datetime'] = start_dtime
            item['end_datetime'] = end_dtime

            item['maize_id'] = basic_tools.maize_api_search(self.maize_vendors,
                                                            vendor_name)
            yield item

    def parse_dinner_vendors(self, response):

        # ---- Dinner time vendors ---- #
        address = tools.get_address(response)

        vendors_xp = '//h2[contains(text(), "Tonight\'s Dinner Time Vendors")]'
        vendors = response.xpath(vendors_xp)

        start_dtime, end_dtime = tools.get_time(response, dinner=True)

        # Vendors list block.
        vblock_xp = './parent::div/parent::div/following-sibling::div'
        vendors_block = vendors.xpath(vblock_xp)[0]

        vlist_xp = ".//div[contains(@class, 'summary-item\n')]"
        for vendor in vendors_block.xpath(vlist_xp):

            item = StreetFoodDatTimeItem()

            vendor_name = tools.get_vendor_name(vendor)

            item['VendorName'] = vendor_name
            item['address'] = address
            item['latitude'] = basic_tools.mix_location('37.769782')
            item['longitude'] = basic_tools.mix_location('-122.411848')
            item['start_datetime'] = start_dtime
            item['end_datetime'] = end_dtime

            item['maize_id'] = basic_tools.maize_api_search(self.maize_vendors,
                                                            vendor_name)
            yield item
