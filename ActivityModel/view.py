# -*- coding:utf-8 -*-
"""
 @time    : 2019/3/4 16:38
 @desc    : 学习测试是使用html的url类
 @Author  : Sorke
 @Email   : sorker0129@hotmail.com
"""

import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AutoWebForceTest.settings')
django.setup()

from ActivityModel.models import TestService
from django.shortcuts import render


def gauge(request):
    return render(request, 'example/gauge.html')


def tooltip(request):
    return  render(request, 'base/tooltip-view.html')
