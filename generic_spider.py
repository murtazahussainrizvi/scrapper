# generic_spider.py

import scrapy

class GenericSpider(scrapy.Spider):
    name = 'generic_spider'

    def start_requests(self):
        url = self.url
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        # Your scraping logic here
        pass

        