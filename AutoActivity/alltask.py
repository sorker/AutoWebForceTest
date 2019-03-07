# -*- coding:utf-8 -*-
"""
 @time    : 2019/2/20 13:12
 @desc    : 多线程测试
 @Author  : Sorke
 @Email   : sorker0129@hotmail.com
"""
import django
import os
import time
import multiprocessing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AutoWebForceTest.settings')
django.setup()

from AutoActivity import configs, submitproblem, driverremote, loginorsign, datadeal
from AutoActivity.myexception.loginError import loginError, problemError, signError
from AutoActivity.mysqldeal import sqlsetSignAccout, sqlsetLoginAccout, sqlsetProcesssPart

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


def problem(nodelist, user, pwd, i, MP, lock, message):
    print('主进程', MP, '下的问题执行程序', i, '开始运行')
    i = 'problem' + str(i)
    driver = driverremote.browser(nodelist.get('host'), nodelist.get('DesiredCapabilities'))
    url = 'http://zwu.hustoj.com/loginpage.php'
    try:
        login = loginorsign.login(driver, url, user, pwd)
        if login in 'login: success':
            message[i] = submitproblem.problem_test(driver)
            if '获取结果超时' in message[i]:
                raise problemError(message[i])
            print(message[i])
        else:
            raise loginError(login)
    except loginError as e:
        print(e)
    except problemError as e:
        print(e)
    finally:
        driver.quit()
        lock.acquire()
        lock.release()
    print('主进程', MP, '下的问题执行程序', i, '结束运行')


def problemTask(nodelist, filename, MP):
    print('主进程', str(MP), '开始运行')
    lock = multiprocessing.Lock()
    message = {}
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
                                    args=(nodelist, account[index][0], account[index][1], index, MP, lock, message,))
        threads.append(t)
    for t in range(step):
        threads[t].start()
    for t in range(step):
        threads[t].join()
    print('主进程', str(MP), '结束运行')


def sign(nodelist, user, pwd, i, MP, lock, message):
    test_sign = 0
    print('主进程', MP, '下的注册程序', i, '开始运行')
    i = 'sign' + str(i)
    driver = driverremote.browser(nodelist.get('host'), nodelist.get('DesiredCapabilities'))
    try:
        message[i] = loginorsign.sign(driver, user, pwd)
        if message[i] in 'sign: success':
            test_sign = 1
        else:
            raise signError(message)
    except signError as e:
        print(message[i])
    finally:
        driver.quit()
        lock.acquire()
        sqlsetSignAccout(site_ip='http://zwu.hustoj.com/', username=user, password=pwd, test_sign=test_sign)
        lock.release()
    print('主进程', MP, '下的注册程序', i, '结束运行')


def signTest(nodelist, filename, num, MP):
    print('主进程', MP, '开始运行')
    message = {}
    lock = multiprocessing.Lock()
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
        t = multiprocessing.Process(target=sign,
                                    args=(nodelist, account[index][0], account[index][1], index, MP, lock, message,))
        threads.append(t)
    for t in range(step):
        threads[t].start()
    for t in range(step):
        threads[t].join()
    # print(sign)
    print('主进程', MP, '结束运行')


def login(nodelist, url, user, pwd, i, MP, lock, message):
    print('主进程', MP, '下的登录程序', i, '开始运行')
    i = 'login' + str(i)
    test_login = 0
    driver = driverremote.browser(nodelist.get('host'), nodelist.get('DesiredCapabilities'))
    try:
        message[i] = loginorsign.login(driver, url, user, pwd)
        if message[i] in 'login: success':
            test_login = 1
        else:
            raise loginError(message[i])
    except loginError as e:
        print(message[i])
    finally:
        driver.quit()
        lock.acquire()
        sqlsetLoginAccout(site_ip='http://' + url.split('/')[2] + '/', username=user, password=pwd,
                          test_login=test_login)
        lock.release()
    print('主进程', MP, '下的登录程序', i, '结束运行')


def loginTest(nodelist, url, filename, MP):
    message = {}
    lock = multiprocessing.Lock()
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
                                    args=(
                                    nodelist, url, account[index][0], account[index][1], index, MP, lock, message,))
        threads.append(t)
    for t in range(step):
        threads[t].start()
    for t in range(step):
        threads[t].join()
    # print(sign)
    print('主进程', MP, '结束运行')


def signAndLoginTest(nodelist, filename, url, num, MP):
    """
    :param nodelist: 分布式驱动信息
    :param filename:用户文件地址
    :param url: 登录的网址
    :param num: 注册用户数量
    :param MP: 进程值
    :return:
    """
    signTest(nodelist, filename, num, MP)
    time.sleep(1)
    loginTest(nodelist, url, filename, MP)


def loginProcess(url, filename):
    """
    :param url: 登录的地址
    :param filename: 账号密码文件
    :return:
    """
    start = time.time()
    threads = []
    i = 0
    for nodelist in NODELIST:
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
    end = time.time()
    sqlsetProcesssPart(main_process='loginProcess:' + str(len(NODELIST)), strecondary_process='loginTest',
                       from_process='login', site_ip='http://' + url.split('/')[2] + '/',
                       start_end_time=int(round((end - start) * 1000)))


def signloginProcess(filename, url, num):
    start = time.time()
    threads = []
    i = 0
    for nodelist in NODELIST:
        t = multiprocessing.Process(target=signAndLoginTest, args=(nodelist, filename, url, num, i))
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
    end = time.time()
    sqlsetProcesssPart(main_process=len(NODELIST), strecondary_process='loginTest', from_process='login',
                       site_ip='http://' + url.split('/')[2] + '/', start_end_time=end - start)


if __name__ == '__main__':
    # print(windowsMasterNode())
    # time.sleep(5)
    # print(windowsNode())
    # threads = []
    # lock = multiprocessing.Lock
    # i = 0
    url = 'http://zwu.hustoj.com/loginpage.php'
    # for nodelist in NODELIST:
    filename = '账号密码.xls'
    #     # t = multiprocessing.Process(target=signTest, args=(nodelist, filename, 3, i))
    #     # t = multiprocessing.Process(target=problemTask, args=(nodelist, filename, i))
    #     t = multiprocessing.Process(target=loginTest, args=(nodelist, url, filename, i))
    #     # t = multiprocessing.Process(target=signAndLoginTest, args=(nodelist, filename, url, 1, i))
    #     threads.append(t)
    #     i += 1
    # for t in range(len(NODELIST)):
    #     threads[t].start()
    # for t in range(len(NODELIST)):
    #     threads[t].join()
    loginProcess(url, filename)
