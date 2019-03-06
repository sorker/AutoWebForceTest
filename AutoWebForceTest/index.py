# -*- coding:utf-8 -*-
"""
 @time    : 2019/3/3 19:43
 @desc    : this is a desc
 @Author  : Sorke
 @Email   : sorker0129@hotmail.com
"""
import django
import os
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AutoWebForceTest.settings')
django.setup()

from ActivityModel.models import TestService, SiteServices
from AutoActivity.services import sshConnect
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators import csrf


def index(request):
    return render(request, 'index.html')


def index_site(request):
    message = 'success'
    request.encoding = 'utf-8'
    if request.method == 'POST':
        site_ip = request.POST['site_ip']
        service_info = request.POST['service_info'].split(';')
        if len(service_info) != 4:
            message = '格式错误,例:192.168.94.133;root;123456;22'
        else:
            service_ip = service_info[0]
            service_username = service_info[1]
            service_pwd = service_info[2]
            service_port = service_info[3]
            sshC = sshConnect(service_ip, service_username, service_pwd, service_port)
            if not sshC:
                message = '无法连接服务器,请检查'
            else:
                try:
                    code = requests.get(site_ip).status_code
                    if code == 200:
                        SiteServices.objects.create(site_ip=site_ip, service_ip=service_ip,
                                                    service_username=service_username, service_pwd=service_pwd,
                                                    service_port=service_port)
                        request.set_cookie({'site_ip': site_ip, 'service_ip': service_ip,
                                                'service_username': service_username, 'service_pwd': service_pwd,
                                                'service_port': service_port})
                except Exception:
                    message = '域名错误,例:http://zwu.hustoj.com/'
    else:
        message = '没有收到你的来电'
    return JsonResponse({'message': message})


if __name__ == '__main__':
    site_ip = 'http://zwu.hustoj.com'
    print(requests.get('http://zwu.hustoj.com').status_code)
    SiteServices.objects.create(site_ip=site_ip)
