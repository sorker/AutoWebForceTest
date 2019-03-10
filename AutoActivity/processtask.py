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


def problem(nodelist, user, pwd, i, MP, lock, dtime, problemmsg, loginmsg):
    print('主进程', MP, '下的问题执行程序', i, '开始运行')
    driver = driverremote.browser(nodelist.get('host'), nodelist.get('DesiredCapabilities'))
    dtime['start' + str(i)] = time.time()
    url = 'http://zwu.hustoj.com/loginpage.php'
    try:
        loginmsg['problem' + str(i)] = loginorsign.login(driver, url, user, pwd)
        if loginmsg['problem' + str(i)] in 'login: success':
            loginmsg['problem' + str(i)] = 1
            problemmsg['problem' + str(i)] = submitproblem.problem_test(driver)
            if '获取结果超时' in problemmsg['problem' + str(i)]:
                raise problemError(problemmsg['problem' + str(i)])
        else:
            raise loginError(login)
    except loginError:
        loginmsg['problem' + str(i)] = 0
        problemmsg['problem' + str(i)] = '登录失败，未测试问题'
    except problemError:
        problemmsg['problem' + str(i)] = '未知错误，获取结果超时'
    finally:
        dtime['end' + str(i)] = time.time()
        driver.quit()
        lock.acquire()
        sqlsetLoginProblem(site_ip='http://zwu.hustoj.com/', username=user, password=pwd,
                           login_status=loginmsg['problem' + str(i)], problem_id=1000,
                           problem_res=problemmsg['problem' + str(i)],
                           start_end_time=int(round((dtime['end' + str(i)] - dtime['start' + str(i)]) * 1000)))
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
    driver = driverremote.browser(nodelist.get('host'), nodelist.get('DesiredCapabilities'))
    dtime['start' + str(i)] = time.time()
    try:
        loginmsg['force' + str(i)] = loginorsign.login(driver, url, user, pwd)
        if loginmsg['force' + str(i)] in 'login: success':
            loginmsg['force' + str(i)] = 1
            for page in urls:
                driver.get(page)
        else:
            raise loginError(login)
    except loginError:
        loginmsg['force' + str(i)] = 0
    finally:
        dtime['end' + str(i)] = time.time()
        driver.quit()
        lock.acquire()
        sqlsetForceTime(site_ip='http://' + url.split('/')[2] + '/', username=user, password=pwd,
                        login_status=loginmsg['force' + str(i)],
                        urls_len=len(urls),
                        start_end_time=int(round((dtime['end' + str(i)] - dtime['start' + str(i)]) * 1000)))
        lock.release()
    print('主进程', MP, '下的压力程序', i, '结束运行')


# 注册成功或尝试登入，确认注册是否有效
def sign(nodelist, user, pwd, url, i, MP, lock, signmsg, loginmsg):
    print('主进程', MP, '下的注册程序', i, '开始运行')
    driver = driverremote.browser(nodelist.get('host'), nodelist.get('DesiredCapabilities'))
    try:
        signmsg['sign' + str(i)] = loginorsign.sign(driver, user, pwd)
        if signmsg['sign' + str(i)] in 'sign: success':
            signmsg['sign' + str(i)] = 1
            loginmsg['login' + str(i)] = 1
        else:
            raise signError(signmsg['sign' + str(i)])
    except signError:
        signmsg['sign' + str(i)] = 0
        loginmsg['login' + str(i)] = 0
    finally:
        driver.quit()
        lock.acquire()
        sqlsetSignAccout(site_ip='http://zwu.hustoj.com/', username=user, password=pwd,
                         test_sign=signmsg['sign' + str(i)], test_login=loginmsg['login' + str(i)])
        lock.release()
    print('主进程', MP, '下的注册程序', i, '结束运行')


def login(nodelist, url, user, pwd, i, MP, lock, message):
    print('主进程', MP, '下的登录程序', i, '开始运行')
    driver = driverremote.browser(nodelist.get('host'), nodelist.get('DesiredCapabilities'))
    try:
        message['login' + str(i)] = loginorsign.login(driver, url, user, pwd)
        if message['login' + str(i)] in 'login: success':
            message['login' + str(i)] = 1
        else:
            raise loginError(message['login' + str(i)])
    except loginError as e:
        print(message['login' + str(i)])
        message['login' + str(i)] = 0
    finally:
        driver.quit()
        lock.acquire()
        sqlsetLoginAccout(site_ip='http://' + url.split('/')[2] + '/', username=user, password=pwd,
                          test_login=message['login' + str(i)])
        lock.release()
    print('主进程', MP, '下的登录程序', i, '结束运行')


def forceTest(nodelist, urls, url, filename, MP):
    print('压力测试主进程:', MP, '开始运行')
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
    print('压力测试主进程:', MP, '结束运行')


def problemTask(nodelist, filename, MP):
    print('问题测试主进程:', str(MP), '开始运行')
    lock = multiprocessing.Lock()
    dtime = {}
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
                                    args=(
                                        nodelist, account[index][0], account[index][1], index, MP, lock, dtime,
                                        problemmsg,
                                        loginmsg,))
        threads.append(t)
    for t in range(step):
        threads[t].start()
    for t in range(step):
        threads[t].join()
    print('问题测试主进程:', str(MP), '结束运行')


def signTest(nodelist, url, filename, MP):
    print('注册主进程:', MP, '开始运行')
    signmsg = {}
    loginmsg = {}
    account = datadeal.readcvs(filename)
    n = len(account)
    k = len(NODELIST)
    step = int(n / k)
    if MP < n % k:
        step += 1
    threads = []
    lock = multiprocessing.Lock()
    for s in range(step):
        index = s * k + MP
        t = multiprocessing.Process(target=sign, args=(
            nodelist, account[index][0], account[index][1], url, index, MP, lock, signmsg, loginmsg,))
        threads.append(t)
    for t in range(step):
        threads[t].start()
    for t in range(step):
        threads[t].join()
    # print(sign)
    print('注册主进程:', MP, '结束运行')


def loginTest(nodelist, url, filename, MP):
    print('登录主进程:', MP, '开始运行')
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
        t = multiprocessing.Process(target=login, args=(
                                        nodelist, url, account[index][0], account[index][1], index, MP, lock, message,))
        threads.append(t)
    for t in range(step):
        threads[t].start()
    for t in range(step):
        threads[t].join()
    # print(sign)
    print('登录主进程', MP, '结束运行')


# def signAndLoginTest(nodelist, filename, url, num, MP):
#     """
#     :param nodelist: 分布式驱动信息
#     :param filename:用户文件地址
#     :param url: 登录的网址
#     :param num: 注册用户数量
#     :param MP: 进程值
#     :return:
#     """
#     signTest(nodelist, filename, num, MP)
#     time.sleep(1)
#     loginTest(nodelist, url, filename, MP)


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
def signProcess(url, filename, num):
    start = time.time()
    threads = []
    i = 0
    file_message = datadeal.usersput(filename, num)
    if '成功' in file_message:
        for nodelist in NODELIST:
            t = multiprocessing.Process(target=signTest, args=(nodelist, url, filename, i))
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
        file_message += '，注册程序运行完成'
    else:
        file_message += '，无法注册'
    return file_message


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
    # urls = findurls.all_urls_deep(webdriver.Chrome(chrome_options=opt), url, deep)
    urls = ['http://zwu.hustoj.com/', 'http://zwu.hustoj.com/bbs.php', 'http://zwu.hustoj.com/faqs.php', 'http://zwu.hustoj.com/problemset.php', 'http://zwu.hustoj.com/status.php', 'http://zwu.hustoj.com/ranklist.php', 'http://zwu.hustoj.com/recent-contest.php', 'http://zwu.hustoj.com/contest.php', 'http://zwu.hustoj.com/#', 'http://zwu.hustoj.com/loginpage.php', 'http://zwu.hustoj.com/registerpage.php', 'http://zwu.hustoj.com/discuss3/', 'http://zwu.hustoj.com/discuss3/discuss.php?#', 'http://zwu.hustoj.com/discuss3/newpost.php', 'http://zwu.hustoj.com/discuss3/discuss.php', 'http://zwu.hustoj.com/discuss3/discuss.php?pid=1328', 'http://zwu.hustoj.com/userinfo.php?user=2016011160', 'http://zwu.hustoj.com/discuss3/thread.php?tid=28', 'http://zwu.hustoj.com/discuss3/discuss.php?pid=1247', 'http://zwu.hustoj.com/userinfo.php?user=2016011304', 'http://zwu.hustoj.com/discuss3/thread.php?tid=18', 'http://zwu.hustoj.com/discuss3/discuss.php?pid=1102', 'http://zwu.hustoj.com/userinfo.php?user=2016011109', 'http://zwu.hustoj.com/discuss3/thread.php?tid=1', 'http://zwu.hustoj.com/discuss3/discuss.php?pid=1141', 'http://zwu.hustoj.com/userinfo.php?user=2016011224', 'http://zwu.hustoj.com/discuss3/thread.php?tid=7', 'http://zwu.hustoj.com/discuss3/thread.php?tid=5', 'http://zwu.hustoj.com/discuss3/discuss.php?pid=1078', 'http://zwu.hustoj.com/discuss3/thread.php?tid=2', 'http://zwu.hustoj.com/faqs.php#', 'http://zwu.hustoj.com/index.php', 'http://zwu.hustoj.com/problemset.php#', 'http://zwu.hustoj.com/problemset.php?page=2', 'http://zwu.hustoj.com/problemset.php?page=3', 'http://zwu.hustoj.com/problemset.php?page=4', 'http://zwu.hustoj.com/problemset.php?page=5', 'http://zwu.hustoj.com/problemset.php?page=6', 'http://zwu.hustoj.com/problemset.php?page=7', 'http://zwu.hustoj.com/problem.php?id=1000', 'http://zwu.hustoj.com/status.php?problem_id=1000&jresult=4', 'http://zwu.hustoj.com/status.php?problem_id=1000', 'http://zwu.hustoj.com/status.php?problem_id=1093&jresult=4', 'http://zwu.hustoj.com/status.php?problem_id=1093', 'http://zwu.hustoj.com/problem.php?id=1094', 'http://zwu.hustoj.com/status.php?problem_id=1094&jresult=4', 'http://zwu.hustoj.com/status.php?problem_id=1094', 'http://zwu.hustoj.com/problem.php?id=1095', 'http://zwu.hustoj.com/status.php?problem_id=1095&jresult=4', 'http://zwu.hustoj.com/status.php?problem_id=1098', 'http://zwu.hustoj.com/problem.php?id=1099', 'http://zwu.hustoj.com/status.php?problem_id=1099&jresult=4', 'http://zwu.hustoj.com/status.php?problem_id=1099', 'http://zwu.hustoj.com/status.php#', 'http://zwu.hustoj.com/userinfo.php?user=test248506210390830', 'http://zwu.hustoj.com/userinfo.php?user=test415491463939034', 'http://zwu.hustoj.com/userinfo.php?user=test819121354056467', 'http://zwu.hustoj.com/userinfo.php?user=test540221672658081', 'http://zwu.hustoj.com/userinfo.php?user=test', 'http://zwu.hustoj.com/userinfo.php?user=test595835314857604', 'http://zwu.hustoj.com/userinfo.php?user=test339927540571105', 'http://zwu.hustoj.com/ranklist.php?scope=d', 'http://zwu.hustoj.com/ranklist.php?scope=w', 'http://zwu.hustoj.com/ranklist.php?scope=m', 'http://zwu.hustoj.com/ranklist.php?scope=y', 'http://zwu.hustoj.com/status.php?user_id=2016011160&jresult=4', 'http://zwu.hustoj.com/status.php?user_id=2016011160', 'http://zwu.hustoj.com/status.php?user_id=2016011173&jresult=4', 'http://zwu.hustoj.com/status.php?user_id=2016011173', 'http://zwu.hustoj.com/userinfo.php?user=2016011067', 'http://zwu.hustoj.com/status.php?user_id=2016011067&jresult=4', 'http://zwu.hustoj.com/status.php?user_id=2016011067', 'http://zwu.hustoj.com/status.php?user_id=2016016230&jresult=4', 'http://zwu.hustoj.com/status.php?user_id=2016016230', 'http://zwu.hustoj.com/userinfo.php?user=2016011207', 'http://zwu.hustoj.com/status.php?user_id=2016011207&jresult=4', 'http://zwu.hustoj.com/status.php?user_id=2016011207', 'http://zwu.hustoj.com/userinfo.php?user=2016011342', 'http://zwu.hustoj.com/status.php?user_id=2016011342&jresult=4', 'http://zwu.hustoj.com/status.php?user_id=2016011342', 'http://zwu.hustoj.com/userinfo.php?user=2016011073', 'http://zwu.hustoj.com/status.php?user_id=2016011073&jresult=4', 'http://zwu.hustoj.com/status.php?user_id=2016011073', 'http://zwu.hustoj.com/userinfo.php?user=2017010609', 'http://zwu.hustoj.com/status.php?user_id=2017010609&jresult=4', 'http://zwu.hustoj.com/status.php?user_id=2017010609', 'http://zwu.hustoj.com/userinfo.php?user=2016011039', 'http://zwu.hustoj.com/status.php?user_id=2016011039&jresult=4', 'http://zwu.hustoj.com/status.php?user_id=2016011039', 'http://zwu.hustoj.com/status.php?user_id=2016011170&jresult=4', 'http://zwu.hustoj.com/status.php?user_id=2016011170', 'http://zwu.hustoj.com/userinfo.php?user=2017010602', 'http://zwu.hustoj.com/status.php?user_id=2016011328&jresult=4', 'http://zwu.hustoj.com/status.php?user_id=2016011328', 'http://zwu.hustoj.com/userinfo.php?user=xhh', 'http://zwu.hustoj.com/status.php?user_id=xhh&jresult=4', 'http://zwu.hustoj.com/status.php?user_id=xhh', 'http://zwu.hustoj.com/userinfo.php?user=2016011278', 'http://zwu.hustoj.com/status.php?user_id=2016011278&jresult=4', 'http://zwu.hustoj.com/status.php?user_id=2016011278', 'http://zwu.hustoj.com/userinfo.php?user=2016011251', 'http://zwu.hustoj.com/status.php?user_id=2016011251&jresult=4', 'http://zwu.hustoj.com/status.php?user_id=2016011251', 'http://zwu.hustoj.com/userinfo.php?user=2016011331', 'http://zwu.hustoj.com/status.php?user_id=2016011331&jresult=4', 'http://zwu.hustoj.com/status.php?user_id=2016011331', 'http://zwu.hustoj.com/userinfo.php?user=2016011227', 'http://zwu.hustoj.com/status.php?user_id=2016011227&jresult=4', 'http://zwu.hustoj.com/status.php?user_id=2016011227', 'http://zwu.hustoj.com/userinfo.php?user=2016011181', 'http://zwu.hustoj.com/status.php?user_id=2016011181&jresult=4', 'http://zwu.hustoj.com/status.php?user_id=2016011181', 'http://zwu.hustoj.com/ranklist.php?start=0', 'http://zwu.hustoj.com/ranklist.php?start=50', 'http://zwu.hustoj.com/ranklist.php?start=100', 'http://zwu.hustoj.com/ranklist.php?start=150', 'http://zwu.hustoj.com/ranklist.php?start=200', 'http://zwu.hustoj.com/ranklist.php?start=250', 'http://zwu.hustoj.com/ranklist.php?start=300', 'http://zwu.hustoj.com/ranklist.php?start=350', 'http://zwu.hustoj.com/ranklist.php?start=400', 'http://zwu.hustoj.com/ranklist.php?start=850', 'http://zwu.hustoj.com/recent-contest.php#', 'http://zwu.hustoj.com/contest.php#', 'http://zwu.hustoj.com/contest.php?cid=1135', 'http://zwu.hustoj.com/contest.php?cid=1100', 'http://zwu.hustoj.com/contest.php?cid=1099', 'http://zwu.hustoj.com/contest.php?cid=1098', 'http://zwu.hustoj.com/contest.php?cid=1097', 'http://zwu.hustoj.com/contest.php?cid=1096', 'http://zwu.hustoj.com/contest.php?cid=1095', 'http://zwu.hustoj.com/contest.php?cid=1094', 'http://zwu.hustoj.com/contest.php?cid=1093', 'http://zwu.hustoj.com/contest.php?cid=1092', 'http://zwu.hustoj.com/contest.php?cid=1090', 'http://zwu.hustoj.com/contest.php?cid=1089', 'http://zwu.hustoj.com/contest.php?cid=1088', 'http://zwu.hustoj.com/contest.php?cid=1087', 'http://zwu.hustoj.com/contest.php?cid=1086', 'http://zwu.hustoj.com/contest.php?cid=1085', 'http://zwu.hustoj.com/contest.php?cid=1084', 'http://zwu.hustoj.com/contest.php?cid=1026', 'http://zwu.hustoj.com/contest.php?cid=1025', 'http://zwu.hustoj.com/contest.php?cid=1024', 'http://zwu.hustoj.com/contest.php?cid=1023', 'http://zwu.hustoj.com/contest.php?cid=1022', 'http://zwu.hustoj.com/contest.php?cid=1021', 'http://zwu.hustoj.com/contest.php?cid=1020', 'http://zwu.hustoj.com/contest.php?cid=1019', 'http://zwu.hustoj.com/contest.php?cid=1018', 'http://zwu.hustoj.com/contest.php?cid=1017', 'http://zwu.hustoj.com/contest.php?cid=1016', 'http://zwu.hustoj.com/contest.php?cid=1015', 'http://zwu.hustoj.com/contest.php?cid=1014', 'http://zwu.hustoj.com/contest.php?cid=1013', 'http://zwu.hustoj.com/contest.php?cid=1012', 'http://zwu.hustoj.com/contest.php?cid=1011', 'http://zwu.hustoj.com/contest.php?cid=1010', 'http://zwu.hustoj.com/contest.php?cid=1009', 'http://zwu.hustoj.com/contest.php?cid=1008', 'http://zwu.hustoj.com/contest.php?cid=1007', 'http://zwu.hustoj.com/contest.php?cid=1006', 'http://zwu.hustoj.com/contest.php?cid=1004', 'http://zwu.hustoj.com/contest.php?cid=1003', 'http://zwu.hustoj.com/contest.php?cid=1000', 'http://zwu.hustoj.com/loginpage.php#', 'http://zwu.hustoj.com/lostpassword.php', 'http://zwu.hustoj.com/registerpage.php#']
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
    filename = '账号密码1.xls'
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
    # froceTestProcess(1, url, filename)
    # loginProcess(url, filename)
    r = signProcess(url, filename, 1)
    # print(r)
