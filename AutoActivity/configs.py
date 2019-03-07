# -*- coding:utf-8 -*-
"""
 @time    : 2019/2/20 13:12
 @desc    : 基础配置文档
 @Author  : Sorke
 @Email   : sorker0129@hotmail.com
"""
import os
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities as DC

BASE_DIR = os.path.dirname(os.path.abspath(__file__))   # 当前文件夹目录
DATA_DIR = os.path.join(BASE_DIR, 'data')               # 当前文件夹目录下的date目录
IMG_DIR = os.path.join(DATA_DIR, 'img')                 # 当前文件夹目录下的img目录
LOG_DIR = os.path.join(DATA_DIR, 'log')
LONG_DATE = 9                         # 默认长整型

NODELIST = [
    {"host": "127.0.0.1:4444/wd/hub", "DesiredCapabilities": DC.CHROME},  # 分布式节点的地址、自动化端口、运行的浏览器驱动
    {"host": "127.0.0.1:5555/wd/hub", "DesiredCapabilities": DC.FIREFOX},
    # {"host": "192.168.0.110:4444", "browserName": "chrome"},
]   # 分布式地址

SERVICES = [
    {'hostname': '192.168.0.110', 'username': 'root', 'password': '123456', 'port': '22'}   # 访问linux的ip，端口，用户名以及密码
]


