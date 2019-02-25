# -*- coding:utf-8 -*-
"""
 @time    : 2019/2/20 13:12
 @desc    : this is a desc
 @Author  : Sorke
 @Email   : sorker0129@hotmail.com
"""
import time, os, multiprocessing
from AutoActivity import services, configs, driver, submitproblem
from selenium.webdriver import Remote

SERVICES = configs.SERVICES[0]
NODELIST = configs.NODELIST


def windowsMasterNode():
    status = os.system('java -jar ../selenium-server-standalone-3.141.59.jar -role hub')
    return status


def windowsNode():
    status = os.system('java -jar ../selenium-server-standalone-3.141.59.jar -role node')
    return status


def distributedTask(driver):
    print('start')
    driver.get('http://zwu.hustoj.com')
    message = submitproblem.problem_test(driver)
    print(message)
    driver.quit()
    print('end')

def testT(sleeptime):
    print("start\n")
    time.sleep(sleeptime)
    print("end\n")

if __name__ == '__main__':
    '''
    service = services.sshConnect(        # linux node conn
        hostname=SERVICES.get('hostname'), username=SERVICES.get('username'),
        password=SERVICES.get('password'), port=SERVICES.get('port')
    )
    # windowsMasterNode()
    print(services.linuxNode(service))
    '''
    print(windowsMasterNode())
    time.sleep(5)
    print(windowsNode())
    threads = []
    # for host, browserName in NODELIST:
    #     driver = Remote(command_executor='http://' + host,
    #                     desired_capabilities={'browserName': browserName}
    #                     )
    #     t = multiprocessing.Process(target=distributedTask, args=(driver,))
    #     threads.append(t)
    for i in range(5):
        print(i)
        t = multiprocessing.Process(target=testT, args=(i,))
        threads.append(t)
    # for t in range(len(NODELIST)):
    #     threads[t].start()
    # for t in range(len(NODELIST)):
    #     threads[t].join()
