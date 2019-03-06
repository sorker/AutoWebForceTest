# -*- coding:utf-8 -*-
"""
 @time    : 2019/3/6 10:59
 @desc    : project文件夹下html文件的url类
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


def analytice(request):
    site_ip_session = request.session['site_ip']
    site_ip_cookies = request.COOKIES.get('site_ip')
    print(site_ip_cookies, site_ip_session)
    return render(request, 'projects/analytics.html')


def export(request):
    return render(request, 'projects/export.html')


def report(request):
    return render(request, 'projects/reports.html')
