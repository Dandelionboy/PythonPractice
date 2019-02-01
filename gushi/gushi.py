import requests
import re

url = 'https://www.gushiwen.org/default_{}.aspx'


def parse_page(page):
    try:
        response = requests.get(url.format(page))
        if response.status_code == 200:

            text = response.text
            titles = re.findall(r'<div class="sons">.*?<b>(.*?)</b>', text, re.DOTALL)
            caodai = re.findall(r'<p class="source"><a.*?>(.*?)</a>', text, re.DOTALL)
            auth = re.findall(r'<p class="source"><a.*?/span><a.*?>(.*?)</a>', text, re.DOTALL)
            contents = re.findall(r'<div class="contson" .*?>(.*?)</div>', text, re.DOTALL)
            parse_content = []
            for x in contents:
                p = re.sub(r'<.*?>', "", x).strip()
                parse_content.append(p)
                # 这里是进行数据清洗
            pomes = []
            for valus in zip(titles, caodai, auth, parse_content):
                pome = {}
                pome['title'] = valus[0]
                pome['year'] = valus[1]
                pome['auther'] = valus[2]
                pome['content'] = valus[3]
                pomes.append(pome)
            for x in pomes:
                print(x)
        else:
            print(response.status_code)
    except Exception as err:
        print(err.args)


def main():
    for i in range(11):
        parse_page(i)


if __name__ == '__main__':
    main()
