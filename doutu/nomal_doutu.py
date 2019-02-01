####同步的方式来来获取图片
import requests
# 下载图片很方便
from urllib import request
from lxml import etree
import  datetime
import re
# os有个自带分割后缀名
import os


def parse_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        text = response.text
        html = etree.HTML(text)
        # 过滤gif
        imgs = html.xpath("//div[@class='page-content text-center']//img[@class!='gif']")
        for img in imgs:
            # get来获取属性
            img_url = img.get('data-original')
            img_name = img.get('alt')
            img_name=re.sub(r"[\?？\.。，！!…]","",img_name)
            # img_tag = img.get('src')
            # suffix = os.path.splitext(img_url)[1]
            filename = img_name + ".jpg"
            print(filename)
            request.urlretrieve(img_url, 'images/' + filename)
    except:
        print("加载失败")


def main():
    for x in range(1, 101):
        print(x)
        url = "http://www.doutula.com/photo/list/?page={}".format(x)
        parse_page(url)


if __name__ == '__main__':
    start_time=datetime.datetime.now()
    main()
    endtime=datetime.datetime.now()
    # 可视化打印
    print("耗时-----"+str(endtime-start_time)+"秒----")

