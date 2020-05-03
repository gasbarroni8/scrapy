# -*- coding: utf-8 -*-
from scrapy import Spider
import json

class TweetsSpider(Spider):
    name = 'tweets'
    allowed_domains = ['trumptwitterarchive.com']

    base = "http://www.trumptwitterarchive.com/data/realdonaldtrump/"
    start_urls = []
    for i in range(2009, 2021, 1):
        url = base + str(i) + ".json"
        start_urls.append(url)
    

    def parse(self, response):
        jsonresponse = json.loads(response.body)

        for tweet in jsonresponse:

            yield {
                "id_str": tweet["id_str"],
                "text": tweet["text"],
                "created_at": tweet["created_at"],
                "retweet_count": tweet["retweet_count"],
                "in_reply_to_user_id_str": tweet["in_reply_to_user_id_str"],
                "favorite_count": tweet["favorite_count"],
                "is_retweet": tweet["is_retweet"]
            }