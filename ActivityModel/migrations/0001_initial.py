# Generated by Django 2.2b1 on 2019-03-01 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LoginProblem',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('site', models.CharField(max_length=20, verbose_name='被测试的站点')),
                ('username', models.CharField(max_length=20, verbose_name='已测试的用户名')),
                ('password', models.CharField(max_length=20, verbose_name='已测试的密码')),
                ('test_times', models.IntegerField(verbose_name='测试次数')),
                ('problem_id', models.IntegerField(verbose_name='问题id')),
                ('problem_status', models.SmallIntegerField(verbose_name='问题运行状态')),
                ('problem_res', models.CharField(max_length=100, verbose_name='问题运行结果')),
            ],
        ),
        migrations.CreateModel(
            name='ProcesssPart',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('test_id', models.IntegerField(verbose_name='被测试账号的id')),
                ('main_process', models.CharField(max_length=20, verbose_name='主进程，节点名')),
                ('strecondary_process', models.CharField(max_length=20, verbose_name='副进程，控制台名')),
                ('from_process', models.CharField(max_length=20, verbose_name='从进程，进程名')),
                ('site', models.CharField(max_length=20, verbose_name='被测试的站点')),
            ],
        ),
        migrations.CreateModel(
            name='TestService',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('site_ip', models.CharField(max_length=20, verbose_name='被测试的站点')),
                ('time_data', models.CharField(max_length=150, verbose_name='获取的服务器状态')),
            ],
        ),
        migrations.CreateModel(
            name='UserLogin',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('site', models.CharField(max_length=20, verbose_name='被测试的站点')),
                ('username', models.CharField(max_length=20, verbose_name='已测试的用户名')),
                ('password', models.CharField(max_length=20, verbose_name='已测试的密码')),
                ('test_sign', models.IntegerField(verbose_name='测试注册成功')),
                ('test_login', models.IntegerField(verbose_name='测试是否可登录')),
            ],
        ),
    ]
