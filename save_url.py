from selenium import webdriver
import win32api
import win32con
import time


def save_url(url):
    browser.get(url)
    print(browser.title)
    if browser.title == '阳光宽频网':
        return
    time.sleep(2)
    # 按下ctrl+s
    win32api.keybd_event(0x11, 0, 0, 0)
    win32api.keybd_event(0x53, 0, 0, 0)
    win32api.keybd_event(0x53, 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(0x11, 0, win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(1)
    # 按下回车
    win32api.keybd_event(0x0D, 0, 0, 0)
    win32api.keybd_event(0x0D, 0, win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(5)


# 　浏览器打开网页
option_path = "user-data-dir=C:/Users/K/AppData/Local/Google/Chrome/User Data"
option = webdriver.ChromeOptions()
option.add_argument(option_path)
browser = webdriver.Chrome(chrome_options=option)
browser.maximize_window()

f = open('final_url')
url_list = f.readlines()
for url in url_list:
    save_url(url)

browser.close()
