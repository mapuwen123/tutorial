# -*- coding: utf-8 -*-

from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule

from tutorial.items import TutorialItem


class TiebaSpider(CrawlSpider):
    name = "tieba"
    allowed_domains = ["tieba.baidu.com"]
    start_urls = [
        "http://tieba.baidu.com/f?kw=%E4%BD%B3%E6%9C%A8%E6%96%AF&ie=utf-8&pn=0",
    ]
    rules = (
        Rule(LinkExtractor(allow=('pn=\d+',)),
             callback='parse_item',
             follow=True),
    )

    def parse_item(self, response):
        for a in response.xpath('//a[@class="j_th_tit "]'):
            item = TutorialItem()
            item['title'] = a.xpath('text()').extract()
            item['link'] = a.xpath('@href').extract()
            yield item
