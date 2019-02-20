####异步的方式来来获取图片
"""
目标加载100页，并下载
1，我们要拿到100个url地址
2.我们要拿到很多的图片img地址
我们生成2个队列，page_queue,img_queue
生成者线程，生产 图片imgurl
消费者线程，根据图片url下载
"""
# 逻辑,
import requests
from queue import Queue
# 下载图片很方便
from urllib import request
from lxml import etree
import datetime
import re
import threading
# os有个自带分割后缀名
import os

#生产图片地址
class Producer(threading.Thread):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"
    }

    # 因为传值，重写初始化函数init，同时保留父类的参数, *args, **kwargs可表示传任意参数
    def __init__(self, page_queue, img_queue, *args, **kwargs):
        super(Producer, self).__init__(*args, **kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue

    def run(self):
        while True:
            # page_队列都空了的话，就说明取完了，get之后就删除了这条数据
            if self.page_queue.empty():
                print("page队列为空了")
                break
            url = self.page_queue.get()
            self.parse_page(url)

    def parse_page(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            text = response.text
            html = etree.HTML(text)
            # 过滤gif
            imgs = html.xpath("//div[@class='page-content text-center']//img[@class!='gif']")
            for img in imgs:
                # get来获取属性
                img_url = img.get('data-original')
                img_name = img.get('alt')
                img_name = re.sub(r"[\?？\.。，！!…*]", "", img_name)
                # img_tag = img.get('src')
                # suffix = os.path.splitext(img_url)[1]
                filename = img_name + ".jpg"
                # 把图片的地址，图片名称加到 图片url队列之中
                self.img_queue.put((img_url, filename))
        except:
            print("加载失败")


class Constumer(threading.Thread):
    def __init__(self, page_queue, img_queue, *args, **kwargs):
        super(Constumer, self).__init__(*args, **kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue


    def run(self):
        while True:
            #在队列还没空的情况下
            if self.img_queue.empty() and self.page_queue.empty():
                break
            # 从imgurl队列中获取保存好的图片的url和图片的名称
            img_url, filename = self.img_queue.get()
            print(filename)
            request.urlretrieve(img_url, 'images/' + filename)


def main():
    #给100个队列，表示对100页进行异步解析
    page_queue = Queue(100)  # 下载两页，就给2个队列
    #创建1000个图片下载的队列
    img_queue = Queue(1000)  # 图片url的队列
    # 爬取100页
    for x in range(1, 100):
        url = "http://www.doutula.com/photo/list/?page={}".format(x)
        page_queue.put(url)
    # 同步就是1个人来做这些事，现在是5个生产者，5个消费者来帮着生产
    for x in range(5):
        t = Producer(page_queue, img_queue)
        t.start()
    for x in range(5):
        t = Constumer(page_queue, img_queue)
        t.start()


if __name__ == '__main__':
    start_time = datetime.datetime.now()
    main()
    endtime = datetime.datetime.now()
    # 可视化打印
    print("耗时-----" + str(endtime - start_time) + "秒----")
