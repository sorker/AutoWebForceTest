# -*- coding:utf-8 -*-
"""
 @time    : 2019/2/20 13:12
 @desc    : this is a desc
 @Author  : Sorke
 @Email   : sorker0129@hotmail.com
"""
import multiprocessing
import os
import time

from AutoActivity import configs, submitproblem, services, driverremote, loginorsign,datadeal
from selenium.webdriver import Remote
from selenium import webdriver

SERVICES = configs.SERVICES[0]
NODELIST = configs.NODELIST


def windowsMasterNode():
    print('start hub')
    result = os.popen('java -jar ../selenium-server-standalone-3.141.59.jar -role hub -port 5555')
    return result


def windowsNode():
    print('start node')
    result = os.popen('java -jar ../selenium-server-standalone-3.141.59.jar -role node -port 5555')
    return result


def problem()


def problemTask(host, browserName, filename, i):
    print('start', str(i))
    # driver = Remote(command_executor='http://' + host, desired_capabilities={'browserName': browserName})
    driver = driverremote.browser(host,browserName)
    driver.get('http://zwu.hustoj.com')
    account = datadeal.readcvs(filename)
    login = loginorsign.login(driver, account[i][0], account[i][1])
    if login in 'login: success':
        message = submitproblem.problem_test(driver)
    print(message)
    driver.quit()
    print('end', str(i))


def sign(host, browserName, user, pwd, i, MP):
    print('主进程', MP, '下的注册程序', i, '开始运行')
    driver = driverremote.browser(host, browserName)
    message = loginorsign.sign(driver, user, pwd)
    print(message)
    driver.quit()
    print('主进程', MP, '下的注册程序', i, '结束运行')



def signTest(host, browserName, filename, num, i):
    print('主进程', i, '开始运行')
    datadeal.usersput(filename, num)
    account = datadeal.readcvs(filename)
    n = len(account)
    k = len(NODELIST)
    step = int(n/k)
    if i < n%k:
        step += 1
    threads = []
    for s in range(step):
        index = s*k+i
        t = multiprocessing.Process(target=sign, args=(host, browserName, account[index][0], account[index][1], index, i,))
        threads.append(t)
    for t in range(step):
        threads[t].start()
    for t in range(step):
        threads[t].join()
    # print(sign)
    print('主进程', i, '结束运行')



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
        filename = '账号密码2.xls'
        t = multiprocessing.Process(target=signTest, args=(nodelist.get('host'), nodelist.get('browserName'), filename, 3, i))
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
