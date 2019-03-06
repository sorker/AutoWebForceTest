# -*- coding: UTF-8 -*-
from django.db import models

# Create your models here.


class UserLogin(models.Model):
    id = models.AutoField(primary_key=True)
    site_ip = models.CharField(u'被测试的站点', max_length=100)
    username = models.CharField(u'已测试的用户名', max_length=100)
    password = models.CharField(u'已测试的密码', max_length=100)
    test_sign = models.IntegerField(u'测试注册成功')
    test_login = models.IntegerField(u'测试是否可登录')

    def __str__(self):
        return str(self.id)


class LoginProblem(models.Model):
    id = models.AutoField(primary_key=True)
    site_ip = models.CharField(u'被测试的站点', max_length=80)
    username = models.CharField(u'已测试的用户名', max_length=100)
    password = models.CharField(u'已测试的密码', max_length=100)
    test_times = models.IntegerField(u'测试次数')
    problem_id = models.IntegerField(u'问题id')
    problem_status = models.SmallIntegerField(u'问题运行状态')
    problem_res = models.CharField(u'问题运行结果', max_length=100)

    def __str__(self):
        return str(self.id)


class ProcesssPart(models.Model):
    id = models.AutoField(primary_key=True)
    test_id = models.IntegerField(u'被测试账号的id')
    main_process = models.CharField(u'主进程，节点名', max_length=100)
    strecondary_process = models.CharField(u'副进程，控制台名', max_length=100)
    from_process = models.CharField(u'从进程，进程名', max_length=100)
    site_ip = models.CharField(u'被测试的站点', max_length=100)

    def __str__(self):
        return str(self.site_ip)


class TestService(models.Model):
    id = models.AutoField(primary_key=True)
    site_ip = models.CharField(u'被测试的站点', max_length=80)
    time_data = models.CharField(u'获取的服务器状态', max_length=255)
    datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.site_ip)

class SiteServices(models.Model):
    id = models.AutoField(primary_key=True)
    site_ip = models.CharField(u'被测试的站点', max_length=80)
    service_ip = models.CharField(u'服务器ip', max_length=100)
    service_username = models.CharField(u'服务器用户名', max_length=100)
    service_pwd = models.CharField(u'服务器密码', max_length=100)  # 60分钟后删除
    service_port = models.CharField(u'服务器端口', max_length=100)
    use_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.site_ip)
