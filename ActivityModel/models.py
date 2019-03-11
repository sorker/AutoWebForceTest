# -*- coding: UTF-8 -*-
from django.db import models

# Create your models here.


class UserLogin(models.Model):
    site_ip = models.CharField(u'被测试的站点', max_length=100)
    username = models.CharField(u'已测试的用户名', max_length=100)
    password = models.CharField(u'已测试的密码', max_length=100)
    test_sign = models.IntegerField(u'测试注册成功')
    test_login = models.IntegerField(u'登录次数')

    def __str__(self):
        return str(self.id)


class LoginProblem(models.Model):
    site_ip = models.CharField(u'被测试的站点', max_length=80)
    username = models.CharField(u'已测试的用户名', max_length=100)
    password = models.CharField(u'已测试的密码', max_length=100)
    login_status = models.IntegerField(u'登录状态')
    problem_id = models.IntegerField(u'问题id', default=1000)
    problem_res = models.CharField(u'问题运行结果', max_length=200)
    start_end_time = models.IntegerField(u'测试用时')
    datetime = models.DateTimeField(u'完成时间', auto_now=True)

    def __str__(self):
        return str(self.id)


class ProcesssPart(models.Model):
    main_process = models.CharField(u'主进程，节点名', max_length=100)
    strecondary_process = models.CharField(u'副进程，控制台名', max_length=100)
    from_process = models.CharField(u'从进程，进程名', max_length=100)
    start_end_time = models.IntegerField(u'测试用时')
    site_ip = models.CharField(u'被测试的站点', max_length=100)

    def __str__(self):
        return str(self.site_ip)


class TestService(models.Model):
    site_ip = models.CharField(u'被测试的站点', max_length=80)
    time_data = models.CharField(u'获取的服务器状态', max_length=255)
    datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.site_ip)


class SiteServices(models.Model):
    site_ip = models.CharField(u'被测试的站点', max_length=80)
    service_ip = models.CharField(u'服务器ip', max_length=100)
    service_username = models.CharField(u'服务器用户名', max_length=100)
    service_pwd = models.CharField(u'服务器密码', max_length=100)  # 60分钟后删除
    service_port = models.CharField(u'服务器端口', max_length=100)
    use_datetime = models.DateTimeField(u'获取时间', auto_now=True)

    def __str__(self):
        return str(self.site_ip)


class ForceTime(models.Model):
    site_ip = models.CharField(u'被测试的站点', max_length=80)
    username = models.CharField(u'已测试的用户名', max_length=100)
    password = models.CharField(u'已测试的密码', max_length=100)
    login_status = models.IntegerField(u'登录状态')
    urls_len = models.IntegerField(u'测试的网站数量')
    start_end_time = models.IntegerField(u'测试用时')

    def __str__(self):
        return str(self.site_ip)


class FilePath(models.Model):
    site_ip = models.CharField(u'被测试的站点', max_length=80)
    process_name = models.CharField(u'程序名', max_length=20)
    filename = models.CharField(u'文件名', max_length=100)
    file_path = models.CharField(u'文件地址', max_length=100)
    use_datetime = models.DateTimeField(u'生成时间', auto_now=True)

    def __str__(self):
        return str(self.site_ip)

