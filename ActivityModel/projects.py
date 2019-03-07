# -*- coding:utf-8 -*-
"""
 @time    : 2019/3/3 19:43
 @desc    : project.html的url类
 @Author  : Sorke
 @Email   : sorker0129@hotmail.com
"""

import time
import json
from django.shortcuts import render, redirect
from AutoActivity.mysqldeal import siteServices


def projects(request):
    try:
        site_ip_session = request.session['site_ip']
        site_ip_cookies = request.COOKIES.get('site_ip')
        if site_ip_session == site_ip_cookies:  # 存在session和cookies相等
            time_data_new, test_services_list = siteServices(request)
            return render(request, 'projects.html',
                          {'time_data_new': time_data_new, 'test_services_list': test_services_list})
        else:
            return redirect('/?msg=未设置域名和服务器内容')
    except KeyError:
        return redirect('/?msg=未设置域名和服务器内容')
