# -*- coding:utf-8 -*-
"""
 @time    : 2019/3/3 19:43
 @desc    : project.html的url类
 @Author  : Sorke
 @Email   : sorker0129@hotmail.com
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AutoWebForceTest.settings')
django.setup()

from ActivityModel.models import UserLogin
from django.shortcuts import render, redirect
from AutoActivity.mysqldeal import getTestServices
from AutoActivity.processtask import signProcess
from django.http import JsonResponse
from AutoActivity import configs

DATA_DIR = configs.DATA_DIR


def projects(request):
    try:
        site_ip_session = request.session['site_ip']
        site_ip_cookies = request.COOKIES.get('site_ip')
        if site_ip_session == site_ip_cookies:  # 存在session和cookies相等
            time_data_new, test_services_list = getTestServices(request)
            return render(request, 'projects.html',
                          {'time_data_new': time_data_new, 'test_services_list': test_services_list})
        else:
            return redirect('/?msg=未设置域名和服务器内容')
    except KeyError:
        return redirect('/?msg=未设置域名和服务器内容')


def test_sign(request):
    filename = request.GET['filename'] + '.xls'
    site = request.GET['site']
    num = int(request.GET['num'])
    print(filename)
    if not os.path.isfile(os.path.join(DATA_DIR, filename)):
        message = signProcess(url=site, filename=filename, num=num)
        count = UserLogin.objects.filter(site_ip=site, test_sign=1).count()
        message = message + ':' + count
        if '文件生成错误' in message:
            os.remove(os.path.join(DATA_DIR, filename))
    else:
        message = '文件已存在，请重命名'
    print(message)
    return JsonResponse({'message': message})
