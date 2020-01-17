# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import JsonItemExporter


class GushiPipeline(object):
    def __init__(self):
        self.fp = open('duanzi.json', 'wb')
        self.exporter = JsonItemExporter(self.fp, ensure_ascii=False, encoding='utf8')
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def open_spider(self, spider):
        print("开始爬取")

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        print("爬取完成")


class WeiXinPline(object):
    def __init__(self):
        self.fp = open('news.json', 'wb')
        self.exporter = JsonItemExporter(self.fp, ensure_ascii=False, encoding='utf8')
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def open_spider(self, spider):
        print("新闻开始爬取")

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        print("新闻爬取完成")
