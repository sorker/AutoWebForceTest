# -*- coding:utf-8 -*-
"""
 @time    : 2019/3/6 10:59
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


def analytice(request):
    return render(request, 'projects/analytics.html')


def export(request):
    return render(request, 'projects/export.html')


def report(request):
    return render(request, 'projects/reports.html')
