# -*- coding: UTF-8 -*-
from django.contrib import admin
from .models import UserLogin, LoginProblem, TestService, ProcesssPart, SiteServices, ForceTime, FilePath


# Register your models here.
class UserLoginAdmin(admin.ModelAdmin):
    list_display = ('site_ip', 'username', 'password', 'test_sign', 'test_login')


class LoginProblemAdmin(admin.ModelAdmin):
    list_display = (
    'site_ip', 'username', 'password', 'login_status', 'problem_id', 'problem_res', 'start_end_time', 'datetime')


class TestServiceAdmin(admin.ModelAdmin):
    list_display = ('site_ip', 'time_data', 'datetime')


class ProcesssPartAdmin(admin.ModelAdmin):
    list_display = ('main_process', 'strecondary_process', 'from_process', 'start_end_time', 'site_ip')


class SiteServicesAdmin(admin.ModelAdmin):
    list_display = ('site_ip', 'service_ip', 'service_username', 'service_pwd', 'service_port', 'use_datetime')


class ForceTimeAdmin(admin.ModelAdmin):
    list_display = ('site_ip', 'username', 'password', 'login_status', 'urls_len', 'start_end_time')


class FilePathAdmin(admin.ModelAdmin):
    list_display = ('site_ip', 'process_name', 'filename', 'file_path', 'use_datetime')


admin.site.register(UserLogin, UserLoginAdmin)
admin.site.register(LoginProblem, LoginProblemAdmin)
admin.site.register(TestService, TestServiceAdmin)
admin.site.register(ProcesssPart, ProcesssPartAdmin)
admin.site.register(SiteServices, SiteServicesAdmin)
admin.site.register(ForceTime, ForceTimeAdmin)
admin.site.register(FilePath, FilePathAdmin)
