# -*- coding: utf-8 -*-
import scrapy


class TableSpider(scrapy.Spider):
    name = 'table'
    allowed_domains = ['ja.wikipedia.org']
    start_urls = ['https://ja.wikipedia.org/wiki/%E9%83%BD%E9%81%93%E5%BA%9C%E7%9C%8C%E3%81%AE%E4%BA%BA%E5%8F%A3%E4%B8%80%E8%A6%A7']

    def parse(self, response):
        table = response.xpath('//table[contains(@class, "wikitable sortable")]')[0]
        trs = table.xpath('.//tr')[3:]
        for tr in trs:
            rank = tr.xpath('.//th/text()').get().strip()
            pref = tr.xpath('.//td/a/text()').get().strip()
            y2015 = tr.xpath('.//td[2]/text()').get().strip()
            y2010 = tr.xpath('.//td[3]/text()').get().strip()
            y2005 = tr.xpath('.//td[4]/text()').get().strip()
            y1995 = tr.xpath('.//td[5]/text()').get().strip()
            y1970 = tr.xpath('.//td[6]/text()').get().strip()
            y1945 = tr.xpath('.//td[7]/text()').get().strip()
            y1920 = tr.xpath('.//td[8]/text()').get().strip()

            yield {
                "rank": rank,
                "pref": pref,
                "y2015": y2015,
                "y2010": y2010,
                "y2005": y2005,
                "y1995": y1995,
                "y1970": y1970,
                "y1945": y1945,
                "y1920": y1920
            }

