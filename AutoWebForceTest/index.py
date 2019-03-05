# -*- coding:utf-8 -*-
"""
 @time    : 2019/3/3 19:43
 @desc    : this is a desc
 @Author  : Sorke
 @Email   : sorker0129@hotmail.com
"""
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AutoWebForceTest.settings')
django.setup()

from ActivityModel.models import TestService
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators import csrf


def index(request):
    return render(request, 'index.html')


def index_site(request):
    request.encoding = 'utf-8'
    if request.method == 'POST':
        site_ip = request.POST['site_ip']
        print(site_ip)
        service_info = request.POST['service_info'].sqlit(';')
        for service in service_info:
            print(service)
    else:
        site_ip = '1'
    return JsonResponse({'site_ip': site_ip})
