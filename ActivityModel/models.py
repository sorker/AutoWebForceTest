# -*- coding: UTF-8 -*-
from django.db import models

# Create your models here.


class UserTest(models.Model):
    username = models.CharField(u'已测试的用户名', max_length=20)
    password = models.CharField(u'已测试的密码', max_length=20)
    test_pass = models.IntegerField(u'测试是否通过')


def __str__(self):
    return self.username
