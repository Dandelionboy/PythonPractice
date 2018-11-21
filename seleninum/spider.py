# selenium爬取淘宝美食
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as Ec
from selenium import webdriver

borswer = webdriver.Chrome()
wait = WebDriverWait(borswer, 10)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}

def search():
    borswer.get("https://www.jd.com/")
    # 判断是否加载成功，加载是要耗时的
    try:

        inputE = wait.until(Ec.presence_of_element_located(By.CSS_SELECTOR, "#key"))
        submitE = wait.until(Ec.element_to_be_clickable(By.CSS_SELECTOR, "#search-2014 > div > button > i"))

        inputE.send_keys("美食")
        submitE.click()
    except:
        print("读取失败")


def main():
    search()


if __name__ == '__main__':
    main()
