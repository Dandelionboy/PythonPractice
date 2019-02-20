# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
from urllib import request

class BmwPipeline(object):
    #这是传统的方式来下载
    def __init__(self):
        # 拿到当前文件的上级目录
        self.images_psth = os.path.join(os.path.dirname(os.path.dirname(__file__)), "images")
        # D:/Python_project/SpiderDemo/bmw\images
        if not os.path.exists(self.images_psth):
            os.mkdir(self.images_psth)

    def process_item(self, item, spider):
        category = item['category']
        urls = item['urls']
        category_path=os.path.join(self.images_psth,category)
        if not  os.path.exists(category_path):
            os.mkdir(category_path)
        for url in urls:
            image_name=url.split("_")[-1]
            request.urlretrieve(url,os.path.join(category_path,image_name))

        return item

    def openspider(self, response):

        pass

    def closespider(self, resopnse):
        pass
