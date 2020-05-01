# -*- coding: utf-8 -*-
import scrapy


class JobsSpider(scrapy.Spider):
    name = 'jobs'
    allowed_domains = ['newyork.craigslist.org']
    start_urls = ['https://newyork.craigslist.org/d/jobs/search/jjj']

    def parse(self, response):
        listings = response.xpath('//*[@class="result-row"]')
        for listing in listings:
            date = listing.xpath('.//*[@class="result-date"]/@datetime').get()
            link = listing.xpath('.//a[@class="result-title hdrlnk"]/@href').get()
            text = listing.xpath('.//a[@class="result-title hdrlnk"]/text()').get()

            yield scrapy.Request(link,
                                 callback=self.parse_listing,
                                 meta={
                                     "date": date,
                                     "link": link,
                                     "text": text
                                 })

        next_page_url = response.xpath('//*[@class="button next"]/@href').get()
        if next_page_url:
            abs_next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(abs_next_page_url, callback=self.parse)

    def parse_listing(self, response):
        date = response.meta["date"]
        link = response.meta["link"]
        text = response.meta["text"]

        conpensation = response.xpath('//*[@class="attrgroup"]/span[1]/b/text()').get()
        type = response.xpath('//*[@class="attrgroup"]/span[2]/b/text()').get()
        images = response.xpath('//*[@id="thumbs"]//@src').getall()
        images = [image.replace("50x50c", "650x450") for image in images]

        address = response.xpath('//*[@id="postingbody"]/text()').getall()

        yield {
            "date": date,
            "link": link,
            "text": text,
            "conpensation": conpensation,
            "type": type,
            "images": images,
            "address": address
        }
