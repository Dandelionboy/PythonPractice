# selenium爬取淘宝美食
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as Ec
from selenium import webdriver

# 显示等待，指定一个等待条件，和一个最长等待时间，程序会判断在等待时间内条件是否满足，如果满足则返回，如果不满足会继续等待，超过时间就会抛出异常
borswer = webdriver.Chrome()
wait = WebDriverWait(borswer, 15)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}

def search():
    borswer.get("https://www.jd.com/")
    # 判断是否加载成功，加载是要耗时的
    try:
        # 也可用find_element_by_id等来获取
        # element_to_be_clickable元素可点击，
        # presence_of_element_located 元素加载
        # 更多查看https://www.cnblogs.com/themost/p/6900852.html
        inputE = wait.until(Ec.presence_of_element_located(By.CSS_SELECTOR, "#key"))
        submitE = wait.until(Ec.element_to_be_clickable(By.CSS_SELECTOR, "#search > div > div.form > button"))
        inputE.send_keys("美食")
        submitE.click()
        # allPage = wait.until(Ec.presence_of_element_located(By.CSS_SELECTOR, "#J_bottomPage > span.p-skip > em:nth-child(1) > b"))
        #
        # return  allPage.text
    except Exception as e:
        print(e.args)


def next_page(page_num):
    try:
        inputE = wait.until(Ec.presence_of_element_located(By.CSS_SELECTOR, "#J_bottomPage > span.p-skip > input"))
        submitE = wait.until(Ec.element_to_be_clickable(By.CSS_SELECTOR, "#J_bottomPage > span.p-skip > a"))
        inputE.clear()
        inputE.send_keys(page_num)
        submitE.click()
        #如果发生异常可能导致数据与页面的胡乱，加下面的判定
        # wait.until(Ec.text_to_be_present_in_element(By.CSS_SELECTOR, "#J_bottomPage > span.p-num > a.curr"),
        #            str(page_num))
    except:
        next_page(page_num)


def main():
    search()

    # for i in range(2,5):
    #     next_page(i)


if __name__ == '__main__':
    main()
