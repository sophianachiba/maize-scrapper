# -*- coding: utf-8 -*-
import scrapy


class SparksocialsfSpider(scrapy.Spider):
    name = "sparksocialsf"
    allowed_domains = ["sparksocialsf.com/schedule"]
    start_urls = (
        'http://www.sparksocialsf.com/schedule/',
    )

    def parse(self, response):
        pass
