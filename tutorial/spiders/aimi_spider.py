# -*- coding: utf-8 -*-

import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor


class DoubanSpider(CrawlSpider):
    name = 'aimi'
    allowed_domains = [
        '123.57.90.151'
    ]
    start_urls = [
        'http://123.57.90.151:8088/aimihealth2/main/index'
    ]
    rules = (
        Rule(LinkExtractor(allow=('/main/index',)),
             callback='parse_item',
             follow=False),
    )

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': '123.57.90.151:8088',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }

    def start_requests(self):
        print('==========================start_requests')
        return [
            scrapy.Request(
                'http://123.57.90.151:8088/aimihealth2/',
                meta={'cookiejar': 1},
                headers=self.headers,
                callback=self.logged_in
            )
        ]

    def logged_in(self, response):
        print('==========================logged_in')
        return [
            scrapy.FormRequest.from_response(
                response,
                meta={'cookiejar': response.meta['cookiejar']},
                headers=self.headers,
                formdata={
                    'KEYDATA': 'admin,fh,1',
                    'tm': '1509614617118'
                },
                callback=self.logged_end,
                dont_filter=True
            )
        ]

    def logged_end(self, response):
        print("-------------------logged_end")
        for url in self.start_urls:
            yield self.make_requests_from_url(url)


    def parse_item(self, response):
        print('======================parse_item')
        for a in response.xpath('//span[@class="menu-text"]'):
            print(a.xpath('text()').extract())
