# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import WeiXinItem


class WxspiderSpider(CrawlSpider):
    name = 'wxspider'
    allowed_domains = ['wxapp-union.com']
    start_urls = ['http://wxapp-union.com/']

    rules = (
        Rule(LinkExtractor(allow=r'.*?mod=list&catid=2&page=\d'), follow=True),
        Rule(LinkExtractor(allow=r'.*?article.*?html'), callback='parse_detail', follow=False)
    )

    def parse_detail(self, response):
        title = response.xpath('//h1[@class="ph"]/text()').get()
        weixinItem = WeiXinItem(title=title)
        yield weixinItem
    # def parse_item(self, response):
    #     i = {}
    #     #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
    #     #i['name'] = response.xpath('//div[@id="name"]').extract()
    #     #i['description'] = response.xpath('//div[@id="description"]').extract()
    #     return i
