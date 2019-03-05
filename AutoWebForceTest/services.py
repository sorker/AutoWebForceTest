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
from ActivityModel.models import TestService, SiteServices
from django.shortcuts import render
from AutoActivity.services import sshConnect, sshClose, allTask
from django.http import JsonResponse


def services(request):
    time_data_new, test_services_list = siteServices()
    return render(request, 'services.html', {'time_data_new': time_data_new, 'test_services_list': test_services_list})


def services_ajax(request):
    time_data_new, test_services_list = siteServices()
    # print(test_services_list)
    return JsonResponse({'time_data_new': time_data_new, 'test_services_list': test_services_list})


def siteServices():
    site_services = SiteServices.objects.filter(service_ip='192.168.94.133').order_by('id').reverse()[:1].values()
    for site_service in site_services:
        service_ip = site_service.get('service_ip')
        service_username = site_service.get('service_username')
        service_pwd = site_service.get('service_pwd')
        service_port = site_service.get('service_port')
        use_datetime = site_service.get('use_datetime')
        time_data_new = newTestServices(service_ip, service_username, service_pwd, service_port)
        test_services_list = allTestServices(service_ip)
    return time_data_new,test_services_list


def newTestServices(service_ip, service_username, service_pwd, service_port):
    # # 获取最新的系统数据并写入数据库
    service = sshConnect(service_ip, service_username, service_pwd, service_port)
    args = allTask(service)
    TestService.objects.create(site_ip=service_ip, time_data=str(args))
    sshClose(service)

    # 返回最新数据
    test_services = TestService.objects.filter(site_ip=service_ip).order_by('id').reverse()[:1].values()
    # print(test_services)
    time_data_new = {}
    for test_service in test_services:
        id = test_service.get('id')
        site_ip = test_service.get('site_ip')
        time_data = json.loads(test_service.get('time_data').replace('\'', '\"'))
        datetime = test_service.get('datetime')
        time_data_new.update({"id": id, "site_ip": site_ip})
        time_data_new.update(time_data)
        time_data_new.update({"datetime": datetime})
    return time_data_new


def allTestServices(service_ip):
    # 返回最新的30条数据
    test_services = TestService.objects.filter(site_ip=service_ip).order_by('id').reverse()[:30].values()
    test_services_list = []
    for test_service in test_services:
        time_data_new = {}
        id = test_service.get('id')
        site_ip = test_service.get('site_ip')
        time_data = json.loads(test_service.get('time_data').replace('\'', '\"'))
        datetime = test_service.get('datetime')
        time_data_new.update({"id": id, "site_ip": site_ip})
        time_data_new.update(time_data)
        time_data_new.update({"datetime": datetime})
        test_services_list.append(time_data_new)
    return test_services_list


if __name__ == "__main__":
    # print(newTestServices())
    print(siteServices())