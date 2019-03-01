# -*- coding: UTF-8 -*-
from django.contrib import admin
from .models import UserLogin, LoginProblem, TestService, ProcesssPart


# Register your models here.
admin.site.register(UserLogin)
admin.site.register(LoginProblem)
admin.site.register(TestService)
admin.site.register(ProcesssPart)
