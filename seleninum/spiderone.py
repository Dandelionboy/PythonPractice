from selenium import webdriver

from selenium.webdriver.chrome.options import  Options
import time
#调入键盘操作
from  selenium.webdriver.common.keys import Keys

browser=webdriver.PhantomJS(executable_path=r'D:\phantomjs-2.1.1-windows\bin\phantomjs.exe')
browser.get("https://www.qiushibaike.com/history/439204489f84cc5105ec18a67c2bca93/")
ti=browser.find_element_by_id("highlight").text
btn=browser.find_element_by_class_name("random")
btn.click()

print(browser.title)
#browser.save_screenshot("qiushi1.png")
