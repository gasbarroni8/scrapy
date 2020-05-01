# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request

class BooksSpider(Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com']

    def parse(self, response):
        books = response.xpath('//h3/a/@href').getall()
        for book in books:
            abs_url = response.urljoin(book)
            yield Request(abs_url, callback=self.parse_book)

        # next page
        next_page_url = response.xpath('//a[text()="next"]/@href').get()
        abs_next_page_url = response.urljoin(next_page_url)
        yield Request(abs_next_page_url)

    def parse_book(self, response):
        titie = response.xpath('//h1/text()').get()
        price = response.xpath('//*[@class="price_color"]/text()').get()

        img_url = response.xpath('.//img/@src').get()
        img_url = img_url.replace("../..", "http://books.toscrape.com/")

        rating = response.xpath('//*[contains(@class, "star-rating")]/@class').get()
        rating = rating.replace("star-rating ", "")

        description = response.xpath('//*[@id="product_description"]/following-sibling::p/text()').get()

        upc = response.xpath('//th[text()="UPC"]/following-sibling::td/text()').get()
        product_type = response.xpath('//th[text()="Product Type"]/following-sibling::td/text()').get()
        price_without_tax = response.xpath('//th[text()="Price (excl. tax)"]/following-sibling::td/text()').get()
        price_with_tax = response.xpath('//th[text()="Price (incl. tax)"]/following-sibling::td/text()').get()
        tax = response.xpath('//th[text()="Tax"]/following-sibling::td/text()').get()
        availability = response.xpath('//th[text()="Availability"]/following-sibling::td/text()').get()
        number_of_reviews = response.xpath('//th[text()="Number of reviews"]/following-sibling::td/text()').get()

        yield {
            "titie" : titie,
            "price" : price,
            "img_url" : img_url,
            "rating" : rating,
            "description" : description,
            "upc" : upc,
            "product_type" : product_type,
            "price_without_tax" : price_without_tax,
            "price_with_tax" : price_with_tax,
            "tax" : tax,
            "availability" : availability,
            "number_of_reviews" : number_of_reviews
        }

