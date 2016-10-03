# -*- coding: utf-8 -*-
import scrapy
import street_food.tools.somastreatfoodpark_tools as tools
from street_food.items import StreetFoodDatTimeItem
# import requests
# import street_food.tools.basic_tools as basic_tools
from scrapy import Request


class SomastreatfoodparkSpider(scrapy.Spider):
    name = "somastreatfoodpark"
    allowed_domains = ["www.somastreatfoodpark.com/"]

    def start_requests(self):
        url = 'http://www.somastreatfoodpark.com/'

        yield Request(url, callback=self.parse_lunch_vendors)
        yield Request(url, callback=self.parse_dinner_vendors,
                      dont_filter=True)

    def __init__(self, *pargs, **kwargs):
        scrapy.Spider.__init__(self, *pargs, **kwargs)

        # url = "http://yumbli.herokuapp.com/api/v1/allkitchens/?format=json"
        # self.maize_vendors = requests.get(url).json()

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

            lunch_item = StreetFoodDatTimeItem()

            vendor_name = tools.get_vendor_name(vendor)

            lunch_item['VendorName'] = vendor_name
            lunch_item['address'] = address
            lunch_item['latitude'] = '37.769782'
            lunch_item['longitude'] = '-122.411848'
            lunch_item['start_datetime'] = start_dtime
            lunch_item['end_datetime'] = end_dtime

            # lunch_item['maize_id'] = basic_tools.maize_api_search(
            #                                    self.maize_vendors,
            #                                                      vendor_name)

            yield lunch_item

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

            dinner_item = StreetFoodDatTimeItem()

            vendor_name = tools.get_vendor_name(vendor)

            dinner_item['VendorName'] = vendor_name
            dinner_item['address'] = address
            dinner_item['latitude'] = '37.769782'
            dinner_item['longitude'] = '-122.411848'
            dinner_item['start_datetime'] = start_dtime
            dinner_item['end_datetime'] = end_dtime

            # dinner_item['maize_id'] = basic_tools.maize_api_search(
            # self.maize_vendors,
            #                                                vendor_name)

            yield dinner_item
