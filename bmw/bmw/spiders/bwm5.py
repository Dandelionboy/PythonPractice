# -*- coding: utf-8 -*-
import os

import scrapy

from ..settings import IMAGES_STORE
from ..items import BmwItem
# 爬取宝马五系的图片
from scrapy.pipelines.images import ImagesPipeline


class Bwm5Spider(scrapy.Spider):
    name = 'bwm5'
    allowed_domains = ['car.autohome.com.cn']
    start_urls = ['https://car.autohome.com.cn/pic/series/65.html']

    def parse(self, response):
        uiboxs = response.xpath("//div[@class='uibox']")[1:]
        for uibox in uiboxs:
            category = uibox.xpath(".//div[@class='uibox-title']//a/text()").get()
            urls = uibox.xpath(".//ul/li/a/img/@src").getall()
            # for url in urls:
            #     url=response.urljoin(url)
            #     print(url)
            urls = list(map(lambda url: response.urljoin(url), urls))
            item = BmwItem(category=category, image_urls=urls)
            yield item


class Bmw5ImagePipe(ImagesPipeline):
    def get_media_requests(self, item, info):
        # 这通过该方法把所有的request拿出来，并设置到request,方便下面取
        request_objs = super(Bmw5ImagePipe, self).get_media_requests(item, info)
        for obj in request_objs:
            obj.item = item
        return request_objs

    def file_path(self, request, response=None, info=None):
        # 图片将要被存储的时候调用，来获取存储图片的位置
        path = super(Bmw5ImagePipe, self).file_path(request, response, info)
        category = request.item.get('category')
        images_store = IMAGES_STORE
        category_path = os.path.join(images_store, category)
        if not os.path.exists(category_path):
            os.mkdir(category_path)
        image_name = path.replace("full/", "")
        image_path = os.path.join(category_path, image_name)
        return image_path
