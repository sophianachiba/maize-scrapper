import scrapy
from scrapy import Request
from street_food.spiders import tools
from street_food.items import StreetFoodItem


class GetFoodYelpCom(scrapy.Spider):
    name = "get-food-yelp"
    allowed_domains = ["yelp.com"]
    base_url = "http://www.yelp.com"

    pages_count = 20    # How much pages to crawl??

    url_pattern = 'http://www.yelp.com/search?find_loc=San+Francisco&start={start}&cflt=streetvendors'

    # Generate urls for crawler, 'pi' is "page index"
    start_urls = (lambda url_pattern=url_pattern, pages_count=pages_count:
                  [url_pattern.format(start=pi) for pi in
                   range(0, pages_count * 10, 10)])()

    def parse(self, response):
        ''' Parse every vendor in search results '''

        vendor_path = '//*[@id="super-container"]/div/div[2]/div[1]/div/div[4]/ul[2]/li[@class="regular-search-result"]'

        for vendor_root in response.xpath(vendor_path):

            vendor_url = vendor_root.xpath('.//a[@class="biz-name js-analytics-click"]/@href').extract()[0]
            vendor_url = self.base_url + vendor_url

            yield Request(vendor_url, callback=self.parse_vendor)

    def parse_vendor(self, response):
        ''' Parse specific vendor '''

        item = StreetFoodItem()

        # Getting shedule, if there is no shedule, skip this item.
        schedule = tools.get_vendor_schedule(response)
        if not schedule:
            self.logger.info("There is no schedule in this vendor, skip it...")
            return
        else:
            item['schedule'] = schedule

        # Getting vendor's name.
        item['VendorName'] = tools.get_vendor_name(response)

        # Getting address.
        item['address'] = tools.get_vendor_address(response)

        # Getting geolocation.
        item['geolocation'] = tools.get_vendor_geolocation(response)

        # Getting phone number.
        item['phone'] = tools.get_vendor_phone(response)

        # Getting website
        item['website'] = tools.get_vendor_website(response)

        yield item
