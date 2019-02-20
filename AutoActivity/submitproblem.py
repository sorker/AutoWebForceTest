# -*- coding:utf-8 -*-
"""
 @time    : 2019/2/20 15:32
 @desc    : this is a desc
 @Author  : Sorke
 @Email   : sorker0129@hotmail.com
"""
from selenium import webdriver
from AutoActivity import loginorsign
from AutoActivity import driver
from AutoActivity import configs

NODELIST = configs.NODELIST[0]


def problem_test(driver, problem_id='1000'):
    """
    网站问题页面提交
    :param driver: 浏览器驱动
    :param problem_id: 问题地址，默认1000。区间[1000-1653]
    :return:
    """
    driver.get('http://zwu.hustoj.com/problem.php?id=' + problem_id)
    username = driver.find_element_by_id('profile')
    if username.text == '登录':
        loginorsign.login(driver=driver, user='test', pwd='123456')
        problem_test(driver)


if __name__ == "__main__":
    driver = driver.browser(NODELIST.get('host'), NODELIST.get('port'), NODELIST.get('browserName'))
    problem_test(driver)
