# 声明浏览器对象，并访问界面
#
from selenium import webdriver
browser=webdriver.Chrome()
url = 'https://www.jd.com/'
browser.implicitly_wait(15)
browser.get(url)
# btn_text = browser.find_element_by_class_name('zu-top-add-question')
# print(btn_text.text)
# input=browser.find_element_by_class_name("zu-top-search-input")
# input.send_keys("Python自动化")
# search=browser.find_element_by_class_name("zu-top-search-button")
# search.click()
search_tv=browser.find_element_by_id("key")
search_tv.send_keys("美食")
btn_search=browser.find_element_by_class_name("button")
btn_search.click()






