# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from street_food.items import StreetFoodDatTimeItem
import street_food.tools.sparksocialsf_tools as tools


class SparksocialsfSpider(scrapy.Spider):
    name = "sparksocialsf"
    allowed_domains = ["sparksocialsf.com"]

    def start_requests(self):
        url = 'http://www.sparksocialsf.com/schedule/'

        yield Request(url, callback=self.parse_lunch_vendors)
        yield Request(url, callback=self.parse_dinner_vendors,
                      dont_filter=True)

    def parse_lunch_vendors(self, response):
        address = tools.get_address(response)
        start_dtime, end_dtime = tools.get_time(response)

        vendors_node_xp = "//h2[contains(text(), 'Lunch Shift')]/\
parent::div/parent::div/following-sibling::div"

        vendors = response.xpath(vendors_node_xp)[0]

        for node in vendors.xpath(".//a[@class='summary-title-link']/text()"):
            item = StreetFoodDatTimeItem()

            item['VendorName'] = node.extract()
            item['address'] = address
            item['latitude'] = '37.770775'
            item['longitude'] = '-122.391588'
            item['start_datetime'] = start_dtime
            item['end_datetime'] = end_dtime

            yield item

    def parse_dinner_vendors(self, response):
        address = tools.get_address(response)
        start_dtime, end_dtime = tools.get_time(response, dinner=True)

        vendors_node_xp = "//h2[contains(text(), 'Dinner Shift')]/\
parent::div/parent::div/following-sibling::div"

        vendors = response.xpath(vendors_node_xp)[0]

        for node in vendors.xpath(".//a[@class='summary-title-link']/text()"):
            item = StreetFoodDatTimeItem()

            item['VendorName'] = node.extract()
            item['address'] = address
            item['latitude'] = '37.770775'
            item['longitude'] = '-122.391588'
            item['start_datetime'] = start_dtime
            item['end_datetime'] = end_dtime

            yield item
