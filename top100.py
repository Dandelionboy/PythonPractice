# -*- coding: utf-8 -*-
# @Time    : 2017/11/2 17:06
# @Author  : Puhao
# @File    : spider.py
# @Software: PyCharm
#===========================������Ӧ�Ŀ�.è�۵�Ӱtop100
import requests
import urllib.request
import re
from multiprocessing import Pool
import json
from requests.exceptions import RequestException
#=========================��������
def get_onepage(url):
    try:
        respose = urllib.request.urlopen(url)
        respo = respose.read().decode('utf-8')
        return respo
    except RequestException:
        return None
#=========================������
def main(page):
    url = "http://maoyan.com/board/4?offset=" + str(page)
    html = get_onepage(url)
    for item in parse_onepge(html):
        print(item)
        write_txt(item)

'''re.I�����Դ�Сд
re.L����ʾ�����ַ��� \w, \W, \b, \B, \s, \S �����ڵ�ǰ����
re.M������ģʽ
re.S��' . '���Ұ������з����ڵ������ַ���ע�⣺' . '���������з��� .html������
re.U�� ��ʾ�����ַ��� \w, \W, \b, \B, \d, \D, \s, \S ������ Unicode �ַ��������ݿ�'''
# һ�·ֲ�ƥ�� ������ͼƬ �����⣬���ݣ���ӳʱ�䣬����
#=====================����ƥ��
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
#=====================д���ļ�
def write_txt(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + "\n")
        f.close()
#============�̳߳�ִ��
if __name__ == '__main__':
    pool = Pool()
    pool.map(main, [i * 10 for i in range(10)])
    pool.close()
    pool.join()
