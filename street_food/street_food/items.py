# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# VendorName, address, geolocation, schedule, phone number*, email address* *:if possible.


class StreetFoodItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    VendorName = scrapy.Field()
    address = scrapy.Field()
    geolocation = scrapy.Field()
    schedule = scrapy.Field()
    phone = scrapy.Field()
    # email = scrapy.Field()
    website = scrapy.Field()


class StreetFoodDatTimeItem(scrapy.Item):
    VendorName = scrapy.Field()
    address = scrapy.Field()
    geolocation = scrapy.Field()

    start_datetime = scrapy.Field()
    end_datetime = scrapy.Field()
