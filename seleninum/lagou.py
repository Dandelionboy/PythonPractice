from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from lxml import etree
"""
流程：1.打开当前页，获取每个链接。循环获取每个链接中的详情内容
2.完毕之后，点击下一页，重复1

"""
class LanGou(object):
    def __init__(self):
        self.marks=[]
        self.broswer=webdriver.Chrome()
        self.broswer.implicitly_wait(20)
        #该地址就是网址实际地址，不用在network寻找
        self.url="https://www.lagou.com/jobs/list_python?city=%E5%85%A8%E5%9B%BD&cl=false&fromSearch=true&labelWords=&suginput="
    def run(self):
        #循环遍历每一页，最好睡几秒
        self.broswer.get(self.url)
        while True:

            #page_source相当于源代码啦
            source=self.broswer.page_source
            self.parse_one_page(source)
            #上面是爬取完一页
            #进行下一页,翻页
            #第三部，请求完第一页，进入第二页，知道不能点击
            next_page_btn =self.broswer.find_element_by_xpath("//div[@class='pager_container']/span[last()]")
            if "pager_next_disabled" in next_page_btn.get_attribute("class"):
                break
            else:
                print("page")
                next_page_btn.click()
            time.sleep(2)

   #第一步，请求界面，
    def parse_one_page(self,sourse):
        htmlEle=etree.HTML(sourse)
        #1页有多少个职位就有好多连接
        links=htmlEle.xpath("//a[@class='position_link']/@href")
        for detail_url in links:
            self.request_detail(detail_url)
            time.sleep(2)

   #第二步，循环请求详情界面数据，窗口切换，关闭，切换到列表页
    def request_detail(self,url):
        #需要打开新的界面，在详情页中没有下一页按钮
        #self.broswer.get(url=url)
        self.broswer.execute_script("window.open('{}')".format(url))
        self.broswer.switch_to.window(self.broswer.window_handles[1])
        source=self.broswer.page_source
        self.parse_detail(source)
        #关闭当前详情页面,切换到列表页
        self.broswer.close()
        self.broswer.switch_to.window(self.broswer.window_handles[0])

#注意L使用显示等待，xpath解析，不需要写最后的text(),是获取不到的，一般解析需要text()
    def parse_detail(self,source):
        htmlEle = etree.HTML(source)
        compony = htmlEle.xpath("//dl[@class='job_company']/dt//h2/text()")[0].strip()
        xinshui = htmlEle.xpath("//span[@class='salary']/text()")[0]
        desc = "\n".join(htmlEle.xpath("//dd[@class='job_bt']//p/text()"))  # 获取该类下的所有段落的文本
        mark = {
            'compony': compony.strip(),
            'xinshui': xinshui.strip(),
            'desc': desc
        }
        self.marks.append(mark)
        print("*" * 20)
        print(mark)



if __name__ == '__main__':
    spider=LanGou()
    spider.run()
