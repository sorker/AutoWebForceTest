# -*- coding:utf-8 -*-
"""
 @time    : 2019/2/20 13:12
 @desc    : 浏览器驱动
 @Author  : Sorke
 @Email   : sorker0129@hotmail.com
"""
from selenium.webdriver import Remote
from selenium import webdriver
from AutoActivity import configs
import time

NODELIST = configs.NODELIST


def browser(host, DesiredCapabilities):
    """
    :param host: 127.0.0.1
    :param post: 22
    :param browserName: chrome
    :return: 返回浏览器驱动
    """
    # driver = webdriver.Chrome()
    driverRemote = Remote(command_executor='http://' + host,
                          desired_capabilities=DesiredCapabilities
                          )
    return driverRemote


if __name__ == '__main__':
    # alltask.windowsMasterNode()
    # alltask.windowsNode()
    # time.sleep(10)
    for node in NODELIST:
        print('123')
        host = node.get('host')
        browserName = node.get('DesiredCapabilities')
        driver = browser(host, browserName)
        driver.get('http://www.baidu.com')
        driver.quit()
