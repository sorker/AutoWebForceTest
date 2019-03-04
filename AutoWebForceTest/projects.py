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


def projects(request):
    return render(request, 'projects/projects.html')
