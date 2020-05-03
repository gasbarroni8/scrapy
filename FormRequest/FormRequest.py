scrapy shell "https://www.hkexnews.hk/sdw/search/searchsdw.aspx"

from scrapy.http import FormRequest, Request


data = {
    "__EVENTTARGET": "btnSearch",
    "__VIEWSTATE": response.xpath('//*[@name="__VIEWSTATE"]/@value').get(),
    "__VIEWSTATEGENERATOR": response.xpath('//*[@name="__VIEWSTATEGENERATOR"]/@value').get(),
    "today": "20200503",
    "sortBy": "shareholding",
    "sortDirection": "desc",
    "txtShareholdingDate": "2019/05/03",
    "txtStockCode": "00001"
}

page = FormRequest('https://www.hkexnews.hk/sdw/search/searchsdw.aspx',
                   formdata=data)