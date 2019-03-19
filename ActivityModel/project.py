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

from django.shortcuts import render, redirect
from AutoActivity.mysqldeal import getProcesssPart, getForceTimeDict, getLoginProblemDict, \
    getSeachAccountDict


def analytice(request):
    try:
        site_ip_session = request.session['site_ip']
        site_ip_cookies = request.COOKIES.get('site_ip')
        if site_ip_session == site_ip_cookies:  # 存在session和cookies相等
            processs_part = getProcesssPart(site_ip_session)
            force_time = getForceTimeDict(site_ip_session)
            login_problem = getLoginProblemDict(site_ip_session)
            sign_login_acc = getSeachAccountDict(site_ip_session)
            return render(request, 'projects/analytics.html',
                          {'sign_login_acc': sign_login_acc, 'processs_part': processs_part,
                           'force_time': force_time, 'login_problem': login_problem})
        else:
            return redirect('/?msg=未设置域名')
    except Exception:
        return redirect('/?msg=未设置域名')



def export(request):
    return render(request, 'projects/export.html')


def reports(request):
    try:
        site_ip_session = request.session['site_ip']
        site_ip_cookies = request.COOKIES.get('site_ip')
        if site_ip_session == site_ip_cookies:  # 存在session和cookies相等
            processs_part = getProcesssPart(site_ip_session)
            force_time = getForceTimeDict(site_ip_session)
            login_problem = getLoginProblemDict(site_ip_session)
            sign_login_acc = getSeachAccountDict(site_ip_session)
            return render(request, 'projects/reports.html',
                          {'sign_login_acc': sign_login_acc, 'processs_part': processs_part,
                           'force_time': force_time, 'login_problem': login_problem})
        else:
            return redirect('/?msg=未设置域名')
    except Exception:
        return redirect('/?msg=未设置域名')
