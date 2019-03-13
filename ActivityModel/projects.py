# -*- coding:utf-8 -*-
"""
 @time    : 2019/3/3 19:43
 @desc    : project.html的url类
 @Author  : Sorke
 @Email   : sorker0129@hotmail.com
"""
import os
import requests
from AutoActivity.processtask import signProcess, loginProcess, problemTaskProcess, froceTestProcess
from AutoActivity.datadeal import excleProduce
from django.http import JsonResponse
from AutoActivity import configs
from django.shortcuts import render, redirect
from AutoActivity.mysqldeal import getTestServices, getSignSuccessNum, getLoginSuccessNum, getForcrTimeNum, \
    getallTestServices, getSeachAccountList, getLoginProblemList, getForceTimeList, setFilePath

DATA_DIR = configs.DATA_DIR


def projects(request):
    try:
        site_ip_session = request.session['site_ip']
        site_ip_cookies = request.COOKIES.get('site_ip')
        if site_ip_session == site_ip_cookies:  # 存在session和cookies相等
            test_services_list = getallTestServices(site_ip_cookies)
            time_data_new = getTestServices(request)
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
    if not os.path.isfile(os.path.join(DATA_DIR, filename)) or num == 0:
        message = signProcess(url=site, filename=filename, num=num)
        count = getSignSuccessNum('http://' + site.split('/')[2] + '/')
        message = message + ':' + count + '个用户注册成功'
        if '文件生成错误' in message:
            os.remove(os.path.join(DATA_DIR, filename))
    else:
        message = '文件已存在，请重命名,若继续请将num设置为0或修改文件名'
    return JsonResponse({'message': message})


def test_login(request):
    filename = request.GET['filename'] + '.xls'
    site = request.GET['site']
    if not os.path.isfile(os.path.join(DATA_DIR, filename)):
        message = '文件不存在，请注册或上传文件'
    else:
        try:
            code = requests.get(site).status_code
            if code == 200:
                message = loginProcess(url=site, filename=filename)
                count = getLoginSuccessNum('http://' + site.split('/')[2] + '/')
                message = message + ':' + count
            else:
                message = '无法连接目标地址'
        except Exception:
            message = '登录地址错误'
    return JsonResponse({'message': message})


def test_upload(request):
    filename = ''
    upload_file = request.FILES.get("local_file", None)  # 获取上传的文件，如果没有文件，则默认为None
    if not upload_file:
        message = '没有选中任何文件'
    elif 'xls' not in upload_file.name:
        message = '必须是excle文件'
    elif os.path.isfile(os.path.join(DATA_DIR, upload_file.name)):
        message = '文件已存在，请重命名后上'
    else:
        file_path = os.path.join(DATA_DIR, upload_file.name)
        destination = open(file_path, 'wb+')  # 打开特定的文件进行二进制的写操作
        for chunk in upload_file.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()
        filename = upload_file.name.split('.')[0]
        setFilePath(site_ip=request.session['site_ip'], process_name='上传文件', filename=(filename + '.xls'),
                    file_path=file_path)
        message = '上传完成，直接注册使用请把num设置为0'
    return JsonResponse({'message': message, 'filename': filename})


def test_problem(request):
    filename = request.GET['filename'] + '.xls'
    if not os.path.isfile(os.path.join(DATA_DIR, filename)):
        message = '文件不存在，请注册或上传文件'
    else:
        message = problemTaskProcess(filename=filename)
    return JsonResponse({'message': message})


def test_force(request):
    deep = int(request.GET['deep'])
    site = request.GET['site']
    filename = request.GET['filename'] + '.xls'
    if not os.path.isfile(os.path.join(DATA_DIR, filename)):
        message = '文件不存在，请注册或上传文件'
    else:
        try:
            code = requests.get(site).status_code
            if code == 200:
                message = froceTestProcess(deep=deep, login_url=site, filename=filename)
                count = getForcrTimeNum('http://' + site.split('/')[2] + '/')
                message = message + ':同时有' + count + '个用户被测试'
            else:
                message = '无法连接目标地址'
        except Exception:
            message = '登录地址错误'
    return JsonResponse({'message': message})


def file_generation(request):
    process_name = request.GET['process_name'];
    if process_name == 'sign_process':
        excleProduce(r'http://zwu.hustoj.com/', '注册程序', ['id', '网址', '用户名', '密码', '是否注册', '是否登录'],
                     list(getSeachAccountList('http://zwu.hustoj.com/')))
    elif process_name == 'login_process':
        excleProduce(r'http://zwu.hustoj.com/', '登录程序', ['id', '网址', '用户名', '密码', '是否注册', '是否登录'],
                     list(getSeachAccountList('http://zwu.hustoj.com/')))
    elif process_name == 'problem_process':
        excleProduce(r'http://zwu.hustoj.com/', '问题程序',
                     ['id', '被测试的站点', '用户名', '密码', '登录状态', '问题id', '问题运行结果', '测试用时', '完成时间'],
                     list(getLoginProblemList('http://zwu.hustoj.com/')))
    elif process_name == 'force_process':
        excleProduce(r'http://zwu.hustoj.com/', '压力程序', ['id', '被测试的站点', '用户名', '密码', '登录状态', '网站数量', '测试用时', '完成时间'],
                     list(getForceTimeList('http://zwu.hustoj.com/')))
    return JsonResponse({'message': '生成成功'})
