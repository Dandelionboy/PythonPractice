# -*- coding: utf-8 -*-
# @Time    : 2017/11/2 17:06
# @Author  : Puhao
# @File    : spider.py
# @Software: PyCharm

from multiprocessing.pool import Pool

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
    for item in parse_onepge(html):
        print(item)
        write_txt(item)


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


if __name__ == '__main__':
    pool = Pool()
    pool.map(main, [i * 10 for i in range(10)])
    pool.close()
    pool.join()

