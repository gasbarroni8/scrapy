# -*- coding: utf-8 -*-
import scrapy
from scrapy_item_example.items import ScrapyItemExampleItem

class SampleItemExampleSpider(scrapy.Spider):
    name = 'sample_item_example'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com']

    def parse(self, response):
        authors = response.xpath('//*[@itemprop="author"]/text()').getall()

        item = ScrapyItemExampleItem()
        item["authors"] = authors
        return item
