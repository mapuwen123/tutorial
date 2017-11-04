# -*- coding: utf-8 -*-

import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule, Request
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.http import HtmlResponse


class DoubanSpider(CrawlSpider):
    name = 'github'
    allowed_domains = [
        'github.com'
    ]
    start_urls = [
        'https://github.com/settings/profile'
    ]
    rules = (
        Rule(LinkExtractor(allow=('/settings/profile',)),
             callback='parse_item',
             follow=True),
    )

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'github.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }

    def start_requests(self):
        print('==========================start_requests')
        return [
            Request(
                'https://github.com/login',
                meta={'cookiejar': 1},
                headers=self.headers,
                callback=self.logged_in
            )
        ]

    def logged_in(self, response):
        print('==========================logged_in')
        authenticity_token = response.xpath('//input[@name="authenticity_token"]/@value').extract()[0]
        print("-------------------", authenticity_token)
        return [
            scrapy.FormRequest.from_response(
                response,
                meta={'cookiejar': response.meta['cookiejar']},
                headers=self.headers,
                formdata={
                    'commit': 'Sign in',
                    'utf8': '✓',
                    'authenticity_token': authenticity_token,
                    'login': 'mapuwen@163.com',
                    'password': '495299188ma'
                },
                callback=self.logged_end
            )
        ]

    def logged_end(self, response):
        print("-------------------logged_end")
        for url in self.start_urls:
            # 因为我们上面定义了Rule，所以只需要简单的生成初始爬取Request即可
            yield Request(
                url,
                meta={'cookiejar': response.meta['cookiejar']},
                headers=self.headers,
                dont_filter=True
            )

    def parse_item(self, response):
        print('======================parse_item')
        title = response.xpath('//input[@id="user_profile_name"]/@value').extract()
        print('======================parse_item---', title)

    def _requests_to_follow(self, response):
        # """cookiejar更新"""
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
