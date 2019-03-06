# -*- coding:utf-8 -*-
"""
 @time    : 2019/3/3 19:45
 @desc    : servces.html的url类
 @Author  : Sorke
 @Email   : sorker0129@hotmail.com
"""

import time
from  AutoActivity.mysqldeal import siteServices
from django.shortcuts import render
from django.http import JsonResponse


def services(request):
    site_ip_session = request.session['site_ip']
    site_ip_cookies = request.COOKIES.get('site_ip')
    if site_ip_session == site_ip_cookies:  # 存在session和cookies相等
        time_data_new, test_services_list = siteServices(request)
        print(time_data_new, test_services_list )
        return render(request, 'services.html',
                      {'time_data_new': time_data_new, 'test_services_list': test_services_list})
    else:
        msg = '未设置域名和服务器内容'
        return render(request, 'index.html', {'msg': msg})


def services_ajax(request):
    site_ip = request.session['site_ip']
    service_ip = request.session['service_ip']
    time_data_new, test_services_list = siteServices(request)
    # print(test_services_list)
    return JsonResponse({'time_data_new': time_data_new, 'test_services_list': test_services_list})

