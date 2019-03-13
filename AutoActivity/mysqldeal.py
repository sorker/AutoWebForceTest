# -*- coding:utf-8 -*-
"""
 @time    : 2019/3/6 20:42
 @desc    : 所有数据库操作并返回处理后的数据类
 @Author  : Sorke
 @Email   : sorker0129@hotmail.com
"""
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AutoWebForceTest.settings')
django.setup()

import json
from AutoActivity.services import sshConnect, sshClose, allTask
from ActivityModel.models import TestService, UserLogin, SiteServices, ProcesssPart, LoginProblem, ForceTime, FilePath


# 获取服务器状态并写入数据库，再返回前十条的值
def getTestServices(request):
    """service.py和projects.py的数据库操作"""
    site_ip = request.session['site_ip']
    service_ip = request.session['service_ip']
    service_username = request.session['service_username']
    service_pwd = request.session['service_pwd']
    service_port = request.session['service_port']
    time_data_new = getsetnewTestServices(site_ip, service_ip, service_username, service_pwd, service_port)
    return time_data_new


def getsetnewTestServices(site_ip, service_ip, service_username, service_pwd, service_port):
    """service.py和projects.py的数据库操作"""
    # # 获取最新的系统数据并写入数据库
    service = sshConnect(service_ip, service_username, service_pwd, service_port)
    args = allTask(service)
    TestService.objects.create(site_ip=site_ip, time_data=str(args))
    sshClose(service)  # 关闭ssh的时机不对

    # 返回最新数据
    test_services = TestService.objects.filter(site_ip=site_ip).order_by('id').reverse()[:1].values()
    # print(test_services)
    time_data_new = {}
    for test_service in test_services:
        id = test_service.get('id')
        site_ip = test_service.get('site_ip')
        time_data = json.loads(test_service.get('time_data').replace('\'', '\"'))
        datetime = test_service.get('datetime')
        time_data_new.update({"id": id, "site_ip": site_ip})
        time_data_new.update(time_data)
        time_data_new.update({"datetime": datetime})
    return time_data_new


def getTenTestServicesList(site_ip):
    """service.py和projects.py的数据库操作"""
    # 返回最新的30条数据
    test_services = TestService.objects.filter(site_ip=site_ip).order_by('id').reverse().values()
    len(test_services)
    test_services_list = []
    for test_service in test_services:
        time_data_new = {}
        id = test_service.get('id')
        site_ip = test_service.get('site_ip')
        time_data = json.loads(test_service.get('time_data').replace('\'', '\"'))
        datetime = test_service.get('datetime')
        time_data_new.update({"id": id, "site_ip": site_ip})
        time_data_new.update(time_data)
        time_data_new.update({"datetime": datetime})
        test_services_list.append(time_data_new)
    return test_services_list


def getallTestServicesList(site_ip):
    """service.py和projects.py的数据库操作"""
    # 返回最新的30条数据
    test_services = TestService.objects.filter(site_ip=site_ip).values()
    len(test_services)
    test_services_list = []
    for test_service in test_services:
        time_data_new = []
        id = test_service.get('id')
        site_ip = test_service.get('site_ip')
        time_data = json.loads(test_service.get('time_data').replace('\'', '\"'))
        datetime = test_service.get('datetime')
        time_data_new.append(id)
        time_data_new.append(site_ip)
        # print(time_data)
        for k,v in time_data.items():
            time_data_new.append(v)
        time_data_new.append(datetime)
        test_services_list.append(time_data_new)
    # print(test_services_list)
    return test_services_list


# 把服务器账号密码写入数据库
def setSiteServices(site_ip, service_ip, service_username, service_pwd, service_port):
    SiteServices.objects.create(site_ip=site_ip, service_ip=service_ip,
                                service_username=service_username, service_pwd=service_pwd,
                                service_port=service_port)


# 把网站账号密码写入数据库
def setSignAccout(site_ip, username, password, test_sign, test_login):
    try:
        signacc = UserLogin.objects.get(site_ip=site_ip, username=username, password=password)
        signacc.test_sign = test_sign
        signacc.test_login = test_login
        signacc.save()
    except UserLogin.DoesNotExist:
        UserLogin.objects.create(site_ip=site_ip, username=username, password=password, test_sign=test_sign,
                                 test_login=test_login)


# 获取成功注册的账号数量
def getSignSuccessNum(site_ip):
    num = UserLogin.objects.filter(site_ip=site_ip, test_sign=1).count()
    return str(num)


# 把网站账号密码写入数据库
def setLoginAccout(site_ip, username, password, test_login):
    try:
        loginacc = UserLogin.objects.get(site_ip=site_ip, username=username, password=password)
        loginacc.test_login += test_login
        loginacc.save()
    except UserLogin.DoesNotExist:
        UserLogin.objects.create(site_ip=site_ip, username=username, password=password, test_sign=0,
                                 test_login=1)


# 获取成功登录的账号数量
def getLoginSuccessNum(site_ip):
    num = UserLogin.objects.filter(site_ip=site_ip).exclude(test_login=0).count()
    return str(num)


# 获取所有可以登录的账号
def getSeachAccountList(site_ip):
    allAccount = UserLogin.objects.filter(site_ip=site_ip).exclude(test_login=0).values_list()
    return allAccount


def getSeachAccountDict(site_ip):
    allAccount = UserLogin.objects.filter(site_ip=site_ip).exclude(test_login=0).values()
    return allAccount


# 写入分布式进程名和运行时间
def setProcesssPart(main_process, strecondary_process, from_process, site_ip, start_end_time):
    ProcesssPart.objects.create(main_process=main_process, strecondary_process=strecondary_process,
                                from_process=from_process, site_ip=site_ip, start_end_time=start_end_time)


# 写入分布式进程名和运行时间
def getProcesssPart(site_ip):
    processs_part = ProcesssPart.objects.filter(site_ip=site_ip).values()
    return processs_part


# 写入问题程序信息
def setLoginProblem(site_ip, username, password, login_status, problem_id, problem_res, start_end_time):
    LoginProblem.objects.create(site_ip=site_ip, username=username, password=password, login_status=login_status,
                                problem_id=problem_id, problem_res=problem_res, start_end_time=start_end_time)


# 获取网站问题测试信息
def getLoginProblemList(site_ip):
    login_problem = LoginProblem.objects.filter(site_ip=site_ip).values_list()
    return login_problem


def getLoginProblemDict(site_ip):
    login_problem = LoginProblem.objects.filter(site_ip=site_ip).values()
    return login_problem


# 写入压力程序信息
def setForceTime(site_ip, username, password, login_status, urls_len, start_end_time):
    ForceTime.objects.create(site_ip=site_ip, username=username, password=password, login_status=login_status,
                             urls_len=urls_len, start_end_time=start_end_time)


# 获取网站压力测试信息
def getForceTimeList(site_ip):
    force_time = ForceTime.objects.filter(site_ip=site_ip).values_list()
    return force_time


def getForceTimeDict(site_ip):
    force_time = ForceTime.objects.filter(site_ip=site_ip).values()
    return force_time


#  获取成功运行压力程序的用户数
def getForcrTimeNum(site_ip):
    num = ForceTime.objects.filter(site_ip=site_ip, login_status=1).count()
    return str(num)


# 写入文件地址
def setFilePath(site_ip, process_name, filename, file_path):
    FilePath.objects.create(site_ip=site_ip, process_name=process_name, filename=filename, file_path=file_path)


def getFilePath(site_ip):
    file_path = FilePath.objects.filter(site_ip=site_ip).values()
    return file_path


if __name__ == '__main__':
    # print(allTestServices('23'))
    # print(sqltestServices('http://zwu.hustoj.com/', '192.168.94.133'))
    getallTestServicesList('http://zwu.hustoj.com/')

