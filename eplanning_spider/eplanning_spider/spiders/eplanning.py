# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request, FormRequest


class EplanningSpider(Spider):
    name = 'eplanning'
    allowed_domains = ['eplanning.ie']
    start_urls = (
        'http://www.eplanning.ie/',
    )

    def parse(self, response):
        urls = response.xpath('//a/@href').extract()
        for url in urls:
            if '#' == url:
                pass
            else:
                yield Request(url, callback=self.parse_application)

    def parse_application(self, response):
        app_url = response.xpath(
            '//*[@class="glyphicon glyphicon-inbox btn-lg"]/following-sibling::a/@href').get()
        yield Request(response.urljoin(app_url), callback=self.parse_form)


    def parse_form(self, response):
        yield FormRequest.from_response(response,
                                        formdata={'RdoTimeLimit': '35'},
                                        dont_filter=True,
                                        formxpath='(//form)[2]',
                                        callback=self.parse_pages)

    def parse_pages(self, response):
        application_urls = response.xpath('//td/a/@href').getall()
        for url in application_urls:
            url = response.urljoin(url)
            yield Request(url, callback=self.parse_items)

        next_page_url = response.xpath('//*[@rel="next"]/@href').get()
        absolute_next_page_url = response.urljoin(next_page_url)
        yield Request(absolute_next_page_url, callback=self.parse_pages)

    def parse_items(self, response):
        agent_btn = response.xpath('//*[@value="Agents"]/@style').get()
        if 'display: inline;  visibility: visible;' in agent_btn:
            name = response.xpath('//tr[th="Name :"]/td/text()').get()
            address_first = response.xpath('//tr[th="Address :"]/td/text()').getall()
            address_second = response.xpath('//tr[th="Address :"]/following-sibling::tr/td/text()').getall()[0:3]
            address = address_first + address_second
            phone = response.xpath('//tr[th="Phone :"]/td/text()').get()
            fax = response.xpath('//tr[th="Fax :"]/td/text()').get()
            email = response.xpath('//tr[th="e-mail :"]/td/a/text()').get()
            url = response.url

            yield {'name': name,
                   'address': address,
                   'phone': phone,
                   'fax': fax,
                   'email': email,
                   'url': url}
        else:
            self.logger.info('Agent button not found on page, passing invalid url.')
