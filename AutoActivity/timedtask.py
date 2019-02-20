# -*- coding:utf-8 -*-
"""
 @time    : 2019/2/20 13:12
 @desc    : this is a desc
 @Author  : Sorke
 @Email   : sorker0129@hotmail.com
"""

import time, os
from AutoActivity import services


def roll_back(step=60, stoptime=(time.time()+600)):
    hostname = '192.168.0.114'
    username = 'root'
    password = '123456'
    service = services.sshConnect(hostname, username, password)
    while True:
        # 执行方法，函数
        ServiceInfo = services.allTask(service)
        print(ServiceInfo)
        time.sleep(step)
        end = time.time()
        if end >= stoptime:
            break


if __name__ == '__main__':
    roll_back(5)
