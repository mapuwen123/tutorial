# -*- coding: utf-8 -*-

import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule, Request
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.http import HtmlResponse


class DoubanSpider(CrawlSpider):
    name = 'douban'
    allowed_domains = [
        'www.douban.com',
    ]
    start_urls = [
        "http://118.31.33.39:3400/admin",
    ]
    rules = (
        Rule(LinkExtractor(allow=('',)),
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
        'Host': '118.31.33.39:3400',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }

    def start_requests(self):
        print('==========================start_requests')
        return [
            scrapy.Request(
                'https://accounts.douban.com/login',
                meta={'cookiejar': 1},
                headers=self.headers,
                callback=self.logged_in,
            )
        ]

    def logged_in(self, response):
        print('==========================logged_in')
        title = response.xpath('//title/text()').extract()
        print('======================logged_in---', title)
        return [
            scrapy.FormRequest.from_response(
                response,
                meta={'cookiejar': response.meta['cookiejar']},
                headers=self.headers,
                formdata={
                    'source': 'None',
                    'redir': 'https://www.douban.com/',
                    'form_email': 'mapuwen@outlook.com',
                    'form_password': '495299188ma'
                },
                callback=self.logged_end,
                dont_filter=True
            )
        ]
        # return [
        #     scrapy.FormRequest.from_response(
        #         response,
        #         meta={'cookiejar': response.meta['cookiejar']},
        #         headers=self.headers,
        #         formdata={
        #             'csrfmiddlewaretoken': csrfmiddlewaretoken,
        #             'username': 'admin',
        #             'password': 'admin'
        #         },
        #         callback=self.logged_end,
        #         dont_filter=True
        #     )
        # ]

    def logged_end(self, response):
        print("-------------------logged_end")
        title = response.xpath('//title/text()').extract()
        print('======================logged_end---', title)
        # for url in self.start_urls:
        # print("-------------------logged_end", url)
        yield Request(
            'http://118.31.33.39:3400/admin/',
            meta={'cookiejar': response.meta['cookiejar']},
            headers=self.headers,
            callback=self.parse_item,
            dont_filter=True
        )

    def parse_item(self, response):
        title = response.xpath('//title/text()').extract()
        print('======================parse_item---', title)

    def _requests_to_follow(self, response):
        """cookiejar更新"""
        print('------------------------_requests_to_follow')
        if not isinstance(response, HtmlResponse):
            return
        seen = set()
        for n, rule in enumerate(self._rules):
            links = [l for l in rule.link_extractor.extract_links(response) if l not in seen]
            if links and rule.process_links:
                links = rule.process_links(links)
            for link in links:
                seen.add(link)
                r = Request(url=link.url, callback=self._response_downloaded)
                # 重写
                r.meta.update(rule=n, link_text=link.text, cookiejar=response.meta['cookiejar'])
                yield rule.process_request(r)
