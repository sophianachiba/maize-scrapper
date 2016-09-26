# -*- coding: utf-8 -*-
import scrapy
import street_food.tools.somastreatfoodpark_tools as tools
from street_food.items import StreetFoodDatTimeItem
import requests
import street_food.tools.basic_tools as basic_tools


class SomastreatfoodparkSpider(scrapy.Spider):
    name = "somastreatfoodpark"
    allowed_domains = ["www.somastreatfoodpark.com/"]
    start_urls = (
        'http://www.somastreatfoodpark.com/',
    )

    def __init__(self, *pargs, **kwargs):
        scrapy.Spider.__init__(self, *pargs, **kwargs)

        url = "http://yumbli.herokuapp.com/api/v1/allkitchens/?format=json"
        self.maize_vendors = requests.get(url).json()

    def parse(self, response):
        address = tools.get_address(response)

        # ---- Lunch time vendors ---- #
        lvendors_xp = '//h2[contains(text(), "Today\'s Lunch Time Vendors")]'
        lunch_vendors = response.xpath(lvendors_xp)

        # Time.
        lvendors_time = "./following-sibling::h3/text()"
        lunch_vendors_time = lunch_vendors.xpath(lvendors_time).extract_first()
        start_dtime, end_dtime = tools.parse_time(lunch_vendors_time)

        # Vendors list block.
        vblock_xp = './parent::div/parent::div/following-sibling::div'
        vendors_block = lunch_vendors.xpath(vblock_xp)[0]
        vlist_xp = ".//div[contains(@class, 'summary-item\n')]"
        for vendor in vendors_block.xpath(vlist_xp):

            lunch_item = StreetFoodDatTimeItem()

            vendor_name = tools.get_vendor_name(vendor)

            lunch_item['VendorName'] = vendor_name
            lunch_item['address'] = address
            lunch_item['latitude'] = '37.76957'
            lunch_item['longitude'] = '-122.409792'
            lunch_item['start_datetime'] = start_dtime
            lunch_item['end_datetime'] = end_dtime

            lunch_item['maize_id'] = basic_tools.maize_api_search(self.maize_vendors,
                                                                  vendor_name)

            yield lunch_item

        # ---- Dinner time vendors ---- #
        tvendors_xp = '//h2[contains(text(), "Tonight\'s Dinner Time Vendors")]'
        tn_vendors = response.xpath(tvendors_xp)

        # Time.
        tvendors_time = "./following-sibling::h3/text()"
        tn_vendors_time = tn_vendors.xpath(tvendors_time).extract_first()
        start_dtime, end_dtime = tools.parse_time(tn_vendors_time)

        # Vendors list block.
        vblock_xp = './parent::div/parent::div/following-sibling::div'
        vendors_block = tn_vendors.xpath(vblock_xp)[0]

        vlist_xp = ".//div[contains(@class, 'summary-item\n')]"
        for vendor in vendors_block.xpath(vlist_xp):

            dinner_item = StreetFoodDatTimeItem()

            vendor_name = tools.get_vendor_name(vendor)

            dinner_item['VendorName'] = vendor_name
            dinner_item['address'] = address
            dinner_item['latitude'] = '37.76957'
            dinner_item['longitude'] = '-122.409792'
            dinner_item['start_datetime'] = start_dtime
            dinner_item['end_datetime'] = end_dtime

            dinner_item['maize_id'] = basic_tools.maize_api_search(self.maize_vendors,
                                                            vendor_name)

            yield dinner_item
