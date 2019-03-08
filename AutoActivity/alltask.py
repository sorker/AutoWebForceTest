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
from selenium import webdriver

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AutoWebForceTest.settings')
django.setup()

from AutoActivity import configs, submitproblem, driverremote, loginorsign, datadeal, findurls
from AutoActivity.myexception.loginError import loginError, problemError, signError
from AutoActivity.mysqldeal import *

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


def problem(nodelist, user, pwd, i, MP, lock, problemmsg, loginmsg):
    print('主进程', MP, '下的问题执行程序', i, '开始运行')
    start = time.time()
    i = 'problem' + str(i)
    driver = driverremote.browser(nodelist.get('host'), nodelist.get('DesiredCapabilities'))
    url = 'http://zwu.hustoj.com/loginpage.php'
    try:
        loginmsg[i] = loginorsign.login(driver, url, user, pwd)
        if loginmsg[i] in 'login: success':
            loginmsg[i] = 1
            problemmsg[i] = submitproblem.problem_test(driver)
            if '获取结果超时' in problemmsg[i]:
                raise problemError(problemmsg[i])
        else:
            raise loginError(login)
    except loginError:
        loginmsg[i] = 0
    except problemError as e:
        print(e)
    finally:
        driver.quit()
        end = time.time()
        lock.acquire()
        sqlsetLoginProblem(site_ip='http://zwu.hustoj.com/', username=user, password=pwd,
                           login_status=loginmsg[i], problem_id=1000, problem_res=problemmsg[i],
                           start_end_time=int(round((end - start) * 1000)))
        lock.release()
    print('主进程', MP, '下的问题执行程序', i, '结束运行')


# 获取用户数据，登陆后开始加载网站页面，进行压力测试，把测试结果写入数据库
def force(nodelist, urls, url, user, pwd, i, MP, lock, dtime, loginmsg):
    """
    :param nodelist: 分布式驱动
    :param urls: 网站各页面地址
    :param url: 网站登录地址
    :param user: 登录用户名
    :param pwd: 登录密码
    :param i: 线程号
    :param MP: 主线程号
    :param lock: 进程锁
    :param message: 测试时间
    :param loginmsg: 登录信息
    :return:
    """
    print('主进程', MP, '下的压力程序', i, '开始运行')
    i = 'problem' + str(i)
    dtime['start' + i] = time.time()
    driver = driverremote.browser(nodelist.get('host'), nodelist.get('DesiredCapabilities'))
    try:
        loginmsg[i] = loginorsign.login(driver, url, user, pwd)
        if loginmsg[i] in 'login: success':
            loginmsg[i] = 1
            for page in urls:
                driver.get(page)
        else:
            raise loginError(login)
    except loginError:
        loginmsg[i] = 0
    finally:
        driver.quit()
        dtime['end' + i] = time.time()
        lock.acquire()
        sqlsetForceTime(site_ip='http://' + url.split('/')[2] + '/', username=user, password=pwd,
                        login_status=loginmsg[i],
                        urls_len=len(urls), start_end_time=int(round((dtime['end' + i] - dtime['start' + i]) * 1000)))
        lock.release()
    print('主进程', MP, '下的压力程序', i, '结束运行')


def sign(nodelist, user, pwd, i, MP, lock, message):
    print('主进程', MP, '下的注册程序', i, '开始运行')
    i = 'sign' + str(i)
    driver = driverremote.browser(nodelist.get('host'), nodelist.get('DesiredCapabilities'))
    try:
        message[i] = loginorsign.sign(driver, user, pwd)
        if message[i] in 'sign: success':
            message[i] = 1
        else:
            raise signError(message)
    except signError as e:
        print(message[i])
        message[i] = 0
    finally:
        driver.quit()
        lock.acquire()
        sqlsetSignAccout(site_ip='http://zwu.hustoj.com/', username=user, password=pwd, test_sign=message[i])
        lock.release()
    print('主进程', MP, '下的注册程序', i, '结束运行')


def login(nodelist, url, user, pwd, i, MP, lock, message):
    print('主进程', MP, '下的登录程序', i, '开始运行')
    i = 'login' + str(i)
    driver = driverremote.browser(nodelist.get('host'), nodelist.get('DesiredCapabilities'))
    try:
        message[i] = loginorsign.login(driver, url, user, pwd)
        if message[i] in 'login: success':
            message[i] = 1
        else:
            raise loginError(message[i])
    except loginError as e:
        print(message[i])
        message[i] = 0
    finally:
        driver.quit()
        lock.acquire()
        sqlsetLoginAccout(site_ip='http://' + url.split('/')[2] + '/', username=user, password=pwd,
                          test_login=message[i])
        lock.release()
    print('主进程', MP, '下的登录程序', i, '结束运行')


def forceTest(nodelist, urls, url, filename, MP):
    print('主进程', MP, '开始运行')
    dtime = {}
    loginmsg = {}
    lock = multiprocessing.Lock()
    account = datadeal.readcvs(filename)
    n = len(account)
    k = len(NODELIST)
    step = int(n / k)
    if MP < n % k:
        step += 1
    threads = []
    for s in range(step):
        index = s * k + MP
        t = multiprocessing.Process(target=force,
                                    args=(nodelist, urls, url, account[index][0], account[index][1], index, MP,
                                          lock, dtime, loginmsg,))
        threads.append(t)
    for t in range(step):
        threads[t].start()
    for t in range(step):
        threads[t].join()
    # print(sign)
    print('主进程', MP, '结束运行')


def problemTask(nodelist, filename, MP):
    print('主进程', str(MP), '开始运行')
    lock = multiprocessing.Lock()
    loginmsg = {}
    problemmsg = {}
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
                                    args=(nodelist, account[index][0], account[index][1], index, MP, lock, problemmsg,
                                          loginmsg,))
        threads.append(t)
    for t in range(step):
        threads[t].start()
    for t in range(step):
        threads[t].join()
    print('主进程', str(MP), '结束运行')


def signTest(nodelist, filename, num, MP):
    print('主进程', MP, '开始运行')
    message = {}
    lock = multiprocessing.Lock()
    file_message = datadeal.usersput(filename, num)
    print(file_message)
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


def loginTest(nodelist, url, filename, MP):
    print('主进程', MP, '开始运行')
    message = {}
    lock = multiprocessing.Lock()
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


# 获取用户数据，登录进程，把测试结果输入数据库
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
    for t in range(len(NODELIST)):
        threads[t].start()
    for t in range(len(NODELIST)):
        threads[t].join()
    end = time.time()
    sqlsetProcesssPart(main_process='loginProcess:' + str(len(NODELIST)), strecondary_process='loginTest',
                       from_process='login', site_ip='http://' + url.split('/')[2] + '/',
                       start_end_time=int(round((end - start) * 1000)))


# 创建一个新的用户文件，num是用户数量。注册后进行登录，把测试结果输入数据库
def signloginProcess(url, filename, num):
    start = time.time()
    threads = []
    i = 0
    for nodelist in NODELIST:
        t = multiprocessing.Process(target=signAndLoginTest, args=(nodelist, filename, url, num, i))
        threads.append(t)
        i += 1
    for t in range(len(NODELIST)):
        threads[t].start()
    for t in range(len(NODELIST)):
        threads[t].join()
    end = time.time()
    sqlsetProcesssPart(main_process='sign_loginProcess:' + str(len(NODELIST)), strecondary_process='sign_loginTest',
                       from_process='sing_login',
                       site_ip='http://' + url.split('/')[2] + '/', start_end_time=int(round((end - start) * 1000)))


# 问题测试，输入用户名文件，把测试结果输入到数据库
def problemTaskProcess(filename):
    start = time.time()
    threads = []
    i = 0
    for nodelist in NODELIST:
        t = multiprocessing.Process(target=problemTask, args=(nodelist, filename, i))
        threads.append(t)
        i += 1
    for t in range(len(NODELIST)):
        threads[t].start()
    for t in range(len(NODELIST)):
        threads[t].join()
    end = time.time()
    sqlsetProcesssPart(main_process='problemTaskProcess:' + str(len(NODELIST)), strecondary_process='problemTask',
                       from_process='problem',
                       site_ip='http://zwu.hustoj.com/', start_end_time=int(round((end - start) * 1000)))


# 获取用户数据，把总结果测试结果写入数据库
def froceTestProcess(deep, login_url, filename):
    start = time.time()
    threads = []
    i = 0
    url = 'http://' + login_url.split('/')[2] + '/'
    opt = webdriver.ChromeOptions()  # 创建chrome参数对象
    opt.add_argument('--headless')  # 把chrome设置成无界面模式，不论windows还是linux都可以，自动适配对应参数
    urls = findurls.all_urls_deep(webdriver.Chrome(chrome_options=opt), url, deep)
    # urls = ['http://zwu.hustoj.com/', 'https://icpc.baylor.edu/', 'http://cm.baylor.edu/welcome.icpc', 'https://github.com/zhblue/hustoj']
    print(urls)
    for nodelist in NODELIST:
        t = multiprocessing.Process(target=forceTest, args=(nodelist, urls, login_url, filename, i))
        threads.append(t)
        i += 1
    for t in range(len(NODELIST)):
        threads[t].start()
    for t in range(len(NODELIST)):
        threads[t].join()
    end = time.time()
    sqlsetProcesssPart(main_process='froceTestProcess:' + str(len(NODELIST)), strecondary_process='forceTest',
                       from_process='force',
                       site_ip=url, start_end_time=int(round((end - start) * 1000)))


if __name__ == '__main__':
    # print(windowsMasterNode())
    # time.sleep(5)
    # print(windowsNode())
    # threads = []
    # lock = multiprocessing.Lock
    # i = 0
    url = 'http://zwu.hustoj.com/loginpage.php'
    # for nodelist in NODELIST:
    filename = '账号密码4.xls'
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
    # problemTaskProcess(filename)
    froceTestProcess(1, url, filename)
