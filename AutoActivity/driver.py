# -*- coding:utf-8 -*-
from selenium.webdriver import Remote
from selenium import webdriver
from AutoActivity import configs

NODELIST = configs.NODELIST


def browser(host, port, browserName):
    """
    :param host: 127.0.0.1
    :param post: 22
    :param browserName: chrome
    :return: 返回浏览器驱动
    """
    # driver = webdriver.Chrome()
    driverRemote = Remote(command_executor='http://' + host + ':' + port + '/wd/hub',
                          desired_capabilities={'browserName': browserName},
                          browser_profile=None,
                          )
    return driverRemote


if __name__ == '__main__':
    for node in NODELIST:
        host = node.get('host')
        post = node.get('post')
        browserName = node.get('browserName')
        driver = browser(host, post, browserName)
        driver.get('http://www.baidu.com')
        driver.quit()
