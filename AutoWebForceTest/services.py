# -*- coding:utf-8 -*-
"""
 @time    : 2019/3/3 19:45
 @desc    : this is a desc
 @Author  : Sorke
 @Email   : sorker0129@hotmail.com
"""
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AutoWebForceTest.settings')
django.setup()

import time
import json
from ActivityModel.models import TestService
from django.shortcuts import render
from AutoActivity.services import sshConnect, sshClose, allTask


def services(request):
    time_data_new = newTestServices()
    # print(time_data_new.get('UsedM') / time_data_new.get('TotalM'))
    test_services_list = allTestServices()
    # print(test_services_list)
    return render(request, 'services.html', {'time_data_new': time_data_new, 'test_services_list': test_services_list})


def newTestServices():
    # # 获取最新的系统数据并写入数据库
    service = sshConnect('192.168.94.133', 'root', '123456', '22')
    args = allTask(service)
    TestService.objects.create(site_ip='192.168.94.133', time_data=str(args))
    sshClose(service)

    # 返回最新数据
    test_services = TestService.objects.filter(site_ip='192.168.94.133').order_by('id').reverse()[:1].values()
    print(test_services)
    time_data_new = {}
    for test_service in test_services:
        id = test_service.get('id')
        site_ip = test_service.get('site_ip')
        time_data = json.loads(test_service.get('time_data').replace('\'', '\"'))
        datetime = test_service.get('datetime')
        time_data_new.update({"id": id, "site_ip": site_ip, "datetime": datetime})
        time_data_new.update(time_data)
    return time_data_new


def allTestServices():
    count = TestService.objects.count()
    # if count - 50 >= 0:
    test_services = TestService.objects.filter(site_ip='192.168.94.133').order_by('id').reverse()[:30].values()
    # else:
        # test_services = TestService.objects.filter(site_ip='192.168.94.133')[:count].values()
    test_services_list = []
    for test_service in test_services:
        time_data_new = {}
        id = test_service.get('id')
        site_ip = test_service.get('site_ip')
        time_data = json.loads(test_service.get('time_data').replace('\'', '\"'))
        datetime = test_service.get('datetime')
        time_data_new.update({"id": id, "site_ip": site_ip, "datetime": datetime})
        time_data_new.update(time_data)
        test_services_list.append(time_data_new)
    return test_services_list


if __name__ == "__main__":
    # print(newTestServices())
    print(allTestServices())
