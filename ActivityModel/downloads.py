# -*- coding:utf-8 -*-
"""
 @time    : 2019/2/20 15:32
 @desc    : 返回downloads.html的类
 @Author  : Sorke
 @Email   : sorker0129@hotmail.com
"""
from django.shortcuts import render, redirect
from django.http import FileResponse, JsonResponse
from AutoActivity.mysqldeal import getFilePath


def downloads(request):
    try:
        site_ip_session = request.session['site_ip']
        site_ip_cookies = request.COOKIES.get('site_ip')
        if site_ip_session == site_ip_cookies:  # 存在session和cookies相等
            file_path = getFilePath(site_ip=site_ip_session)
            return render(request, 'downloads.html', {'file_path': file_path})
        else:
            return redirect('/?msg=未设置域名')
    except Exception:
        return redirect('/?msg=未设置域名')


def file_down(request):
    try:
        file_path = request.GET['file_path']
        file = open(file_path, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="' + str(file_path.split('_')[-1]) + '"'
        return response
    except Exception:
        site_ip_session = request.session['site_ip']
        file_path = getFilePath(site_ip=site_ip_session)
        return render(request, 'downloads.html', {'file_path': file_path, 'message': '文件获取失败请检查网络问题'})
