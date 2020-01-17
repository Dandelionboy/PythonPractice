# -*- coding: utf-8 -*-
import scrapy
from ..items import GushiItem


class Gushi1Spider(scrapy.Spider):
    # 爬虫的名字，名字要唯一
    name = 'gushi1'
    allowed_domains = ['gushiwen.org']

    base_url = "https://so.gushiwen.org"
    start_urls = ['https://so.gushiwen.org/shiwen/default_0AA1.aspx']

    def parse(self, response):
        print("=========>")
        # 这里的p[1]，是p在cont类下的第二个元素，所以是p[1]
        contents = response.xpath("//div[@class='left']//div[@class='sons']")
        for item in contents:
            title = item.xpath(".//div[@class='cont']/p[1]/a/b/text()").extract_first()
            content = item.xpath('.//div/div[@class="contson"]//text() | .//div/div[@class="contson"]/p//text()').extract()
            gushi_item = GushiItem(title=title, content=content)
            print(gushi_item)
            yield gushi_item
        next_page = response.xpath("//a[@class='amore']/@href").extract()
        if not next_page:
            print("没有了")
            return
        else:
            yield scrapy.Request(self.base_url + next_page[0], callback=self.parse)

        print("<========")
