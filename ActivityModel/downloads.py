# -*- coding:utf-8 -*-
"""
 @time    : 2019/2/20 15:32
 @desc    : 返回downloads.html的类
 @Author  : Sorke
 @Email   : sorker0129@hotmail.com
"""
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AutoWebForceTest.settings')
django.setup()

from ActivityModel.models import TestService
from django.shortcuts import render


def downloads(request):
    return render(request, 'downloads.html')