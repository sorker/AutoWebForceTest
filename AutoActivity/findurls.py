# -*- coding:utf-8 -*-
import requests
import time
from selenium import webdriver


# 获取一个页面下的地址
def site_urls(driver, url):
    """mysite: http://www.baidu.com/"""
    mysite = url.split('/')[2]  # 获取站点的域名
    driver.get(url)  # 打开页面
    new_urls = []  # 本页的所有地址
    useful_urls = []  # 本页所有有用的地址
    for link in driver.find_elements_by_tag_name('a'):
        new_urls.append(link.get_attribute('href'))  # 获取页面中所有的url
    for new_url in new_urls:
        if new_url is None:
            continue
        if new_url.find(mysite):                         # 判断是否是本站点的url
            if requests.get(new_url).status_code == 200:  # 判断地址是否有用
                useful_urls.append(new_url)
    return useful_urls


def all_urls_deep(driver, url, deep):
    urls = [url]  # 所有页面集合
    deeps = [0]
    for i, k in enumerate(urls):
        if deeps[i] < deep:
            for new_url in site_urls(driver, k):  # 遍历得到的页面url
                if new_url not in urls:  # 判断地址是否重复
                    urls.append(new_url)
                    deeps.append(deeps[i] + 1)
            deeps[i] += 1
        #     u_ds = {k: deeps[i]}
        # print(u_ds)  # 打印已遍历深度
    end = time.time()
    return urls

if __name__ in '__main':
    print(site_urls(driver=webdriver.Chrome(), url='http://zwu.hustoj.com/'))
    print(all_urls_deep(driver=webdriver.Chrome(), url='http://zwu.hustoj.com/discuss3/thread.php?tid=28', deep=2))
