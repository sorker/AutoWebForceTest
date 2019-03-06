# -*- coding:utf-8 -*-
"""
 @time    : 2019/3/6 20:42
 @desc    : 所有数据库操作并返回处理后的数据类
 @Author  : Sorke
 @Email   : sorker0129@hotmail.com
"""
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AutoWebForceTest.settings')
django.setup()

import json
from AutoActivity.services import sshConnect, sshClose, allTask
from ActivityModel.models import TestService, SiteServices


def siteServices(request):
    """service.py和projects.py的数据库操作"""
    site_ip = request.session['site_ip']
    service_ip = request.session['service_ip']
    service_username = request.session['service_username']
    service_pwd = request.session['service_pwd']
    service_port = request.session['service_port']
    time_data_new = newTestServices(site_ip, service_ip, service_username, service_pwd, service_port)
    test_services_list = allTestServices(site_ip)
    return time_data_new, test_services_list


def newTestServices(site_ip, service_ip, service_username, service_pwd, service_port):
    """service.py和projects.py的数据库操作"""
    # # 获取最新的系统数据并写入数据库
    service = sshConnect(service_ip, service_username, service_pwd, service_port)
    args = allTask(service)
    TestService.objects.create(site_ip=site_ip, time_data=str(args))
    sshClose(service)  # 关闭ssh的时机不对

    # 返回最新数据
    test_services = TestService.objects.filter(site_ip=site_ip).order_by('id').reverse()[:1].values()
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


def allTestServices(site_ip):
    """service.py和projects.py的数据库操作"""
    # 返回最新的30条数据
    test_services = TestService.objects.filter(site_ip=site_ip).order_by('id').reverse()[:30].values()
    len(test_services)
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


if __name__ == '__main__':
    # print(allTestServices('23'))
    print(siteServices('http://zwu.hustoj.com/', '192.168.94.133'))
