# -*- coding:utf-8 -*-
"""
 @time    : 2019/2/20 15:32
 @desc    : 返回about.html的类
 @Author  : Sorke
 @Email   : sorker0129@hotmail.com
"""
from django.shortcuts import render


def about(request):
    return render(request, 'about.html')
