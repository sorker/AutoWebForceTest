# -*- coding:utf-8 -*-
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))   # 当前文件夹目录
DATA_DIR = os.path.join(BASE_DIR, 'data')               # 当前文件夹目录下的date目录
IMG_DIR = os.path.join(DATA_DIR, 'img')                 # 当前文件夹目录下的img目录
LONG_DATE = 999999999999999                             # 默认长整型

NODELIST = [
    {"host": "127.0.0.1", "port": "4444", "browserName": "chrome"},
]   # 分布式地址

SERVICE_PORT = {
    'default': {'port': '22'}
}

