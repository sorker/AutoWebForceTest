from django.test import TestCase
import django
import os
from selenium import webdriver
import time
import json
from urllib import request
from http import cookiejar


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AutoWebForceTest.settings')
django.setup()

from ActivityModel.models import TestService
from AutoActivity.services import sshConnect, sshClose, allTask


if __name__ in "__main__":
    cookie = cookiejar.CookieJar()
    # 利用urllib.request库的HTTPCookieProcessor对象来创建cookie处理器,也就CookieHandler
    handler = request.HTTPCookieProcessor(cookie)
    # 通过CookieHandler创建opener
    opener = request.build_opener(handler)
    # 此处的open方法打开网页
    response = opener.open('http://192.168.255.19/0.htm')
    for item in cookie:
        print(item)
        print('Name = %s' % item.name)
        print('Value = %s' % item.value)
    print(cookie)
    # service = sshConnect('192.168.94.133', 'root', '123456', '22')
    # time_sl = 0
    # while time_sl <= 10:
    #     args = allTask(service)
    #     print(args)
    #     TestService.objects.create(site_ip='192.168.94.133', time_data=str(args))
    #     time.sleep(5)
    #     time_sl += 5
    # sshClose(service)
    # test_services = TestService.objects.values()
    # for test_service in test_services:
    #     b = test_service.get('time_data').replace('\'', '\"')
    #     print(b)
    #     a = json.loads(b)
    #     print("=", a)
    #     print(type(a))
