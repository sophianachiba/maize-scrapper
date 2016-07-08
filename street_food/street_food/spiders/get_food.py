# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from street_food.items import StreetFoodItem

# VendorName, address, geolocation, schedule, phone number*, email address* *:if possible.


class GetFoodSpider(scrapy.Spider):
    name = "get-food"
    allowed_domains = ["yelp.com"]
    start_urls = (
        'http://www.yelp.com/search?find_loc=San+Francisco&start=0&cflt=streetvendors',
        # 'http://www.yelp.com/search?find_loc=San+Francisco&start=10&cflt=streetvendors',
        # 'http://www.yelp.com/search?find_loc=San+Francisco&start=20&cflt=streetvendors'
    )

    base_url = "http://www.yelp.com"

    def parse(self, response):
        vendor_path = '//*[@id="super-container"]/div/div[2]/div[1]/div/div[4]/ul[2]/li[@class="regular-search-result"]'

        for vendor_root in response.xpath(vendor_path):

            vendor_url = vendor_root.xpath('.//a[@class="biz-name js-analytics-click"]/@href').extract()[0]
            vendor_url = self.base_url + vendor_url

            yield Request(vendor_url, callback=self.parse_vendor)

    def parse_vendor(self, response):

        # Skip vendor if there is no schedule.

        item = StreetFoodItem()
        name_path = '//*[@id="wrap"]/div[3]/div/div[1]/div/div[2]/div[1]/div[1]/h1/text()'
        street_path = '//*[@id="wrap"]/div[3]/div/div[1]/div/div[3]/div[1]/div/div[2]/ul/li[1]/div/strong/address/span[1]/text()'

        vendor_name = response.xpath(name_path).extract()[0].strip()
        street = response.xpath(street_path).extract()[0].strip()

        item['VendorName'] = vendor_name
        item['address'] = street

        yield item
