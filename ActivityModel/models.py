# -*- coding: UTF-8 -*-
from django.db import models

# Create your models here.


class UserLogin(models.Model):
    id = models.IntegerField(primary_key=True)
    site = models.CharField(u'被测试的站点', max_length=20)
    username = models.CharField(u'已测试的用户名', max_length=20)
    password = models.CharField(u'已测试的密码', max_length=20)
    test_sign = models.IntegerField(u'测试注册成功')
    test_login = models.IntegerField(u'测试是否可登录')


class LoginProblem(models.Model):
    id = models.IntegerField(primary_key=True)
    site = models.CharField(u'被测试的站点', max_length=20)
    username = models.CharField(u'已测试的用户名', max_length=20)
    password = models.CharField(u'已测试的密码', max_length=20)
    test_times = models.IntegerField(u'测试次数')
    problem_id = models.IntegerField(u'问题id')
    problem_status = models.SmallIntegerField(u'问题运行状态')
    problem_res = models.CharField(u'问题运行结果', max_length=100)


class ProcesssPart(models.Model):
    id = models.IntegerField(primary_key=True)
    test_id = models.IntegerField(u'被测试账号的id')
    main_process = models.CharField(u'主进程，节点名', max_length=20)
    strecondary_process = models.CharField(u'副进程，控制台名', max_length=20)
    from_process = models.CharField(u'从进程，进程名', max_length=20)
    site = models.CharField(u'被测试的站点', max_length=20)


class TestService(models.Model):
    id = models.IntegerField(primary_key=True)
    site_ip = models.CharField(u'被测试的站点', max_length=20)
    time_data = models.CharField(u'获取的服务器状态', max_length=150)


def __str__(self):
    return self.username
