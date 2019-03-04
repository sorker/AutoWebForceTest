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
    test_services = testServices()
    return render(request, 'services.html', {'test_services': test_services})


def testServices():
    # service = sshConnect('192.168.94.133', 'root', '123456', '22')
    # time_sl = 0
    # while time_sl <= 10:
    #     args = allTask(service)
    #     print(args)
    #     TestService.objects.create(site_ip='192.168.94.133', time_data=str(args))
    #     time.sleep(5)
    #     time_sl += 5
    # sshClose(service)
    test_services = TestService.objects.values()
    test_services_list = []
    # print(test_services)
    for test_service in test_services:
        id = test_service.get('id')
        site_ip = test_service.get('site_ip')
        time_data = json.loads(test_service.get('time_data').replace('\'', '\"'))
        datetime = test_service.get('datetime')
        time_data.update({"id": id, "site_ip": site_ip, "datetime": datetime})
        test_services_list.append(time_data)
    return test_services_list



if __name__ == "__main__":
    testServices()
