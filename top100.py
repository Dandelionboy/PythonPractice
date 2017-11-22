# -*- coding: utf-8 -*-
# @Time    : 2017/11/2 17:06
# @Author  : Puhao
# @File    : spider.py
# @Software: PyCharm
#===========================导入相应的库.猫眼电影top100
import requests
import urllib.request
import re
from multiprocessing import Pool
import json
from requests.exceptions import RequestException
#=========================定义请求
def get_onepage(url):
    try:
        respose = urllib.request.urlopen(url)
        respo = respose.read().decode('utf-8')
        return respo
    except RequestException:
        return None
#=========================主方法
def main(page):
    url = "http://maoyan.com/board/4?offset=" + str(page)
    html = get_onepage(url)
    for item in parse_onepge(html):
        print(item)
        write_txt(item)
==========注释 r.S
'''re.I：忽略大小写
re.L：表示特殊字符集 \w, \W, \b, \B, \s, \S 依赖于当前环境
re.M：多行模式
re.S：' . '并且包括换行符在内的任意字符（注意：' . '不包括换行符） .html存在行
re.U： 表示特殊字符集 \w, \W, \b, \B, \d, \D, \s, \S 依赖于 Unicode 字符属性数据库'''
# 一下分布匹配 排名，图片 ，标题，主演，上映时间，评分
#=====================正则匹配
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
            'actor': item[3],
            'time': item[4],
            'score': item[5] + item[6]
        }
#=====================写入文件
def write_txt(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + "\n")
        f.close()
#============线程池执行
if __name__ == '__main__':
    pool = Pool()
    pool.map(main, [i * 10 for i in range(10)])
    pool.close()
    pool.join()
