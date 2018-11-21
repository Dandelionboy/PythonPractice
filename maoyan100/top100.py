# -*- coding: utf-8 -*-
# @Time    : 2017/11/2 17:06
# @Author  : Puhao
# @File    : spider.py
# @Software: PyCharm
import os
from _md5 import md5
from multiprocessing.pool import Pool
from pathlib import Path

import requests
from requests.exceptions import RequestException
import re
import json



def get_onepage(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            print(response.status_code)
    except RequestException:
        return None


def main(page):
    url = "http://maoyan.com/board/4?offset=" + str(page)
    html = get_onepage(url)
    dir=create_dir("image")
    for item in parse_onepge(html):
        print(item)
        # 保存到文件
        write_txt(item)
        # 下载文件
        down_image(dir,item['image'])


def parse_onepge(html):
    pattern = re.compile(
        '<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?title="(.*?)".*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>',
        re.S)
    data = re.findall(pattern, html)
    for item in data:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2],
            'actor': item[3].strip()[3:],
            'time': item[4].strip()[5:],
            'score': item[5] + item[6]
        }


def write_txt(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + "\n")
        f.close()


def create_dir(name):
    # 在当前位置创建一个dir，或者自己制定'D:\spider\jiepai
    dir = Path(name)
    if not dir.exists():
        dir.mkdir()
    return dir


def down_image(save_dir, url):
    print("正在下载" + url)
    try:
        res = requests.get(url)
        if res.status_code == 200:
            save_image(save_dir, res.content)
        return None

    except:
        print("下载异常")


def save_image(dir, content):
    file_path = '{0}/{1}.{2}'.format(dir, md5(content).hexdigest(), 'jpg')
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write(content)


if __name__ == '__main__':
    pool = Pool()
    pool.map(main, [i * 10 for i in range(10)])
    pool.close()
    pool.join()

