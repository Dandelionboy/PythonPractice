# 声明浏览器对象，并访问界面

from selenium import webdriver
browser=webdriver.Chrome()
url = 'https://www.zhihu.com/explore'
browser.implicitly_wait(15)
browser.get(url)
btn_text = browser.find_element_by_class_name('zu-top-add-question')
print(btn_text.text)
input=browser.find_element_by_class_name("zu-top-search-input")
input.send_keys("Python自动化")
search=browser.find_element_by_class_name("zu-top-search-button")
search.click()




