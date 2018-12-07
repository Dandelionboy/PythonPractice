from selenium import webdriver
from lxml import etree
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

"""
爬取boss直聘上的 python招聘下的详情中的hr的头像，其他详情信息雷同，自己可爬取
用while true.循环每页，直到异常产生表示爬取页数完全，（本来想找到下一页按钮，但是不知道好多页
所以粗暴的来解决）
"""
class BossSpider(object):
    def __init__(self):
        self.url = "https://www.zhipin.com/c101270100/?query=python&page={}&ka=page-next"
        self.browser = webdriver.Chrome()
        self.page = 1

    def run(self):
        while True:
            try:
                self.browser.get(self.url.format(self.page))
                content = self.browser.page_source
                self.parse_page(content)
            except Exception as e:
                print("没有更多数据啦")
                print(e)
                break

    def parse_page(self, source):
        htmlEle = etree.HTML(source)
        detail_links = htmlEle.xpath("//div[@class='info-primary']//a/@href")
        base_url = 'https://www.zhipin.com'
        for index, link in enumerate(detail_links):
            if index == 1:
                link = base_url + link
                self.request_detail(link)
                break

    def request_detail(self, url):
        # 请求详情数据,打开新窗口
        self.browser.execute_script("window.open('{}')".format(url))
        self.browser.switch_to.window(self.browser.window_handles[1])
        content = self.browser.page_source
        self.parse_detail(content)
        # 关闭详情，切换到列表页
        self.browser.close()
        self.browser.switch_to.window(self.browser.window_handles[0])
        time.sleep(2)

    def parse_detail(self, source):
        htmlEle = etree.HTML(source)
        icon = htmlEle.xpath('//div[@class="detail-figure"]/img/@src')[0]
        print(icon)
        self.page += 1


if __name__ == '__main__':
    spider = BossSpider()
    spider.run()
