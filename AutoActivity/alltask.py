# -*- coding:utf-8 -*-
"""
 @time    : 2019/2/20 13:12
 @desc    : 多线程测试
 @Author  : Sorke
 @Email   : sorker0129@hotmail.com
"""
import django, os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AutoWebForceTest.settings')
django.setup()

import multiprocessing
from AutoActivity import configs, submitproblem, services, driverremote, loginorsign, datadeal
from AutoActivity.myexception.loginError import loginError, problemError, signError
from selenium.webdriver import Remote
from selenium import webdriver
from ActivityModel.models import UserLogin, LoginProblem, TestService, ProcesssPart

SERVICES = configs.SERVICES[0]
NODELIST = configs.NODELIST


def windowsMasterNode():
    print('start hub')
    result = os.popen('java -jar ../selenium-server-standalone-3.141.59.jar -role hub')
    return result


def windowsNode():
    print('start node')
    result = os.popen('java -jar ../selenium-server-standalone-3.141.59.jar -role node -port 5555')
    return result


def problem(nodelist, user, pwd, i, MP):
    login_status = ''
    print('主进程', MP, '下的问题执行程序', i, '开始运行')
    driver = driverremote.browser(nodelist.get('host'), nodelist.get('DesiredCapabilities'))
    url = 'http://zwu.hustoj.com/loginpage.php'
    try:
        login = loginorsign.login(driver, url, user, pwd)
        if login in 'login: success':
            message = submitproblem.problem_test(driver)
            if '获取结果超时' in message:
                raise problemError(message)
            print(message)
        else:
            raise loginError(login)
    except loginError as e:
        print(e)
    except problemError as e:
        print(e)
    driver.quit()
    print('主进程', MP, '下的问题执行程序', i, '结束运行')


def problemTask(nodelist, filename, MP):
    print('主进程', str(MP), '开始运行')
    account = datadeal.readcvs(filename)
    n = len(account)
    k = len(NODELIST)
    step = int(n / k)
    if MP < n % k:
        step += 1
    threads = []
    for s in range(step):
        index = s * k + MP
        t = multiprocessing.Process(target=problem,
                                    args=(nodelist, account[index][0], account[index][1], index, MP,))
        threads.append(t)
    for t in range(step):
        threads[t].start()
    for t in range(step):
        threads[t].join()
    print('主进程', str(MP), '结束运行')


def sign(nodelist, user, pwd, i, MP):
    print('主进程', MP, '下的注册程序', i, '开始运行')
    driver = driverremote.browser(nodelist.get('host'), nodelist.get('DesiredCapabilities'))
    try:
        message = loginorsign.sign(driver, user, pwd)
        if message in 'sign: success':
            print(message)
        else:
            raise signError(message)
    except signError as e:
        print(message)
    driver.quit()
    print('主进程', MP, '下的注册程序', i, '结束运行')


def signTest(nodelist, filename, num, MP):
    print('主进程', MP, '开始运行')
    datadeal.usersput(filename, num)
    account = datadeal.readcvs(filename)
    n = len(account)
    k = len(NODELIST)
    step = int(n / k)
    if MP < n % k:
        step += 1
    threads = []
    for s in range(step):
        index = s * k + MP
        t = multiprocessing.Process(target=sign, args=(nodelist, account[index][0], account[index][1], index, MP,))
        threads.append(t)
    for t in range(step):
        threads[t].start()
    for t in range(step):
        threads[t].join()
    # print(sign)
    print('主进程', MP, '结束运行')


def login(nodelist, url, user, pwd, i, MP):
    print('主进程', MP, '下的登录程序', i, '开始运行')
    driver = driverremote.browser(nodelist.get('host'), nodelist.get('DesiredCapabilities'))
    try:
        message = loginorsign.login(driver, url, user, pwd)
        if message in 'sign: success':
            print(message)
        else:
            raise loginError(message)
    except loginError as e:
        print(message)
    driver.quit()
    print('主进程', MP, '下的登录程序', i, '结束运行')


def loginTest(nodelist, url, filename, MP):
    print('主进程', MP, '开始运行')
    account = datadeal.readcvs(filename)
    n = len(account)
    k = len(NODELIST)
    step = int(n / k)
    if MP < n % k:
        step += 1
    threads = []
    for s in range(step):
        index = s * k + MP
        t = multiprocessing.Process(target=login,
                                    args=(nodelist, url, account[index][0], account[index][1], index, MP,))
        threads.append(t)
    for t in range(step):
        threads[t].start()
    for t in range(step):
        threads[t].join()
    # print(sign)
    print('主进程', MP, '结束运行')


if __name__ == '__main__':
    # print(windowsMasterNode())
    # time.sleep(5)
    # print(windowsNode())
    threads = []
    lock = multiprocessing.Lock
    i = 0
    url = 'http://zwu.hustoj.com/loginpage.php'
    for nodelist in NODELIST:
        filename = '账号密码1.xls'
        # t = multiprocessing.Process(target=signTest, args=(nodelist, filename, 3, i))
        # t = multiprocessing.Process(target=problemTask, args=(nodelist, filename, i))
        t = multiprocessing.Process(target=loginTest, args=(nodelist, url, filename, i))
        threads.append(t)
        i += 1
    # for i in range(3):
    #     print(i)
    #     t = multiprocessing.Process(target=testT, args=(i,))
    #     threads.append(t)
    for t in range(len(NODELIST)):
        threads[t].start()
    for t in range(len(NODELIST)):
        threads[t].join()
