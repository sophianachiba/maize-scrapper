# -*- coding: utf-8 -*-
import scrapy
import street_food.tools.somastreatfoodpark_tools as tools
from street_food.items import StreetFoodDatTimeItem


class SomastreatfoodparkSpider(scrapy.Spider):
    name = "somastreatfoodpark"
    allowed_domains = ["www.somastreatfoodpark.com/"]
    start_urls = (
        'http://www.somastreatfoodpark.com/',
    )

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

            item = StreetFoodDatTimeItem()

            vendor_name = tools.get_vendor_name(vendor)

            item['VendorName'] = vendor_name
            item['address'] = address
            item['latitude'] = '37.76957'
            item['longitude'] = '-122.409792'
            item['start_datetime'] = start_dtime
            item['end_datetime'] = end_dtime

            yield item
