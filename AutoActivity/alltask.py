# -*- coding:utf-8 -*-
"""
 @time    : 2019/2/20 13:12
 @desc    : this is a desc
 @Author  : Sorke
 @Email   : sorker0129@hotmail.com
"""
import django, os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AutoWebForceTest.settings')
django.setup()

import multiprocessing
from AutoActivity import configs, submitproblem, services, driverremote, loginorsign,datadeal
from AutoActivity.myexception.loginError import defaultError
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


def problem(host, DesiredCapabilities, user, pwd, i, MP):
    print('主进程', MP, '下的登录程序', i, '开始运行')
    driver = driverremote.browser(host, DesiredCapabilities)
    driver.get('http://zwu.hustoj.com')
    try:
        login = loginorsign.login(driver, user, pwd)
        if login in 'login: success':
            message = submitproblem.problem_test(driver)
            print(message)
        else:
            raise defaultError(login)
    except defaultError as e:
        print(e)
    driver.quit()
    print('主进程', MP, '下的注册程序', i, '结束运行')


def problemTask(host, DesiredCapabilities, filename, MP):
    print('start', str(MP))
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
                                    args=(host, DesiredCapabilities, account[index][0], account[index][1], index, MP,))
        threads.append(t)
    for t in range(step):
        threads[t].start()
    for t in range(step):
        threads[t].join()
    print('end', str(MP))


def sign(host, DesiredCapabilities, user, pwd, i, MP):
    print('主进程', MP, '下的注册程序', i, '开始运行')
    driver = driverremote.browser(host, DesiredCapabilities)
    message = loginorsign.sign(driver, user, pwd)
    print(message)
    driver.quit()
    print('主进程', MP, '下的注册程序', i, '结束运行')


def signTest(host, DesiredCapabilities, filename, num, MP):
    print('主进程', MP, '开始运行')
    datadeal.usersput(filename, num)
    account = datadeal.readcvs(filename)
    n = len(account)
    k = len(NODELIST)
    step = int(n/k)
    if MP < n%k:
        step += 1
    threads = []
    for s in range(step):
        index = s*k+i
        t = multiprocessing.Process(target=sign, args=(host, DesiredCapabilities, account[index][0], account[index][1], index, MP,))
        threads.append(t)
    for t in range(step):
        threads[t].start()
    for t in range(step):
        threads[t].join()
    # print(sign)
    print('主进程', MP, '结束运行')



if __name__ == '__main__':
    '''
    service = services.sshConnect(        # linux node conn
        hostname=SERVICES.get('hostname'), username=SERVICES.get('username'),
        password=SERVICES.get('password'), port=SERVICES.get('port')
    )
    # windowsMasterNode()
    print(services.linuxNode(service))
    '''
    # print(windowsMasterNode())
    # time.sleep(5)
    # print(windowsNode())
    threads = []
    i = 0
    for nodelist in NODELIST:
        filename = '账号密码.xls'
        # t = multiprocessing.Process(target=signTest, args=(nodelist.get('host'), nodelist.get('DesiredCapabilities'), filename, 3, i))
        t = multiprocessing.Process(target=problemTask, args=(nodelist.get('host'), nodelist.get('DesiredCapabilities'), filename, i))
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
