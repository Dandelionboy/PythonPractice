# 要获取详情中的图集，在首页列表页中取到文章的详情连接，在详情连接中的js变量中获取图片集。ajax
import re
import json
import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup


# 获取首页的数据返回


def get_page_index(offset, keyword):
    data = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': '20',
        'cur_tab': 3,  # 表示图集,
        'from': 'gallery'
    }
    url = 'https://www.toutiao.com/search_content/?' + urlencode(data)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print("状态码错误")
    except:
        print("读取异常")


# 获取每个连接的文章html
def get_page_content(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            print("详情状态码错误")
    except:
        print("详情读取异常")


def main():
    # 获取首页数据返回
    html = get_page_index(0, "街拍")
    # 解析html数据并循环遍历文章url
    for url in parse_page_index(html):
        # 获取详情的信息
        html_detail = get_page_content(url)
        if html_detail:
            parse_page_detail(html_detail, url)



# 解析每页数据中的文章连接
def parse_page_index(html):
    try:
        data = json.loads(html)
        if data and 'data' in data.keys():
            for item in data.get("data"):
                yield item.get("article_url")
    except:
        print("获取文章连接失败")


def parse_page_detail(html, url):
    soup = BeautifulSoup(html, 'lxml')
    title = soup.select("title")[0].get_text()
    print(title)
    # image_pttern = re.compile(r"gallery: JSON.parse[(](.*?)[)],\n", re.S)
    # result = re.search(image_pttern, html)
    # print(result)
    # if result:
    #     result = result.group(1).replace("\\", "")
    #
    #     # try:
    #     #     image_data = json.loads(result)
    #     #     if image_data and 'sub_images' in image_data.keys():
    #     #         sub_images = image_data.get("sub_images")
    #     #         img_urls = [item.get("url") for item in sub_images]
    #     #         return {
    #     #             'title': title,
    #     #             'url': url,
    #     #             'images': img_urls
    #     #         }
    #     #
    #     # except:
    #     #     print("图片url出错")

if __name__ == '__main__':
    main()
