# -*- coding:utf-8 -*-
"""
 @time    : 2019/2/20 15:32
 @desc    : 针对毕业设计站点:http://zwu.hustoj.com的操作类
 @Author  : Sorke
 @Email   : sorker0129@hotmail.com
"""
from AutoActivity import loginorsign
from AutoActivity import configs
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Remote
from selenium import webdriver
from time import sleep


NODELIST = configs.NODELIST
DEFAULT_ANSWER_ID = configs.DEFAULT_ANSWER_ID
DEFAULT_ANSWER = configs.DEFAULT_ANSWER


def problem_test(driver, problem_id=DEFAULT_ANSWER_ID, answer=DEFAULT_ANSWER, user='test', pwd='123456'):
    """
    网站问题页面提交
    :param driver: 浏览器驱动
    :param problem_id: 问题地址，默认1000。区间[1000-1653]
    :return:
    """
    username = driver.find_element_by_id('profile')   # 验证是否登陆
    if username.text == '登录':
        url = 'http://zwu.hustoj.com/loginpage.php'
        loginorsign.login(driver=driver, url=url, user=user, pwd=pwd)
    driver.get('http://zwu.hustoj.com/problem.php?id=' + problem_id)
    driver.find_element_by_link_text('提交').click()
    sleep(2)
    # frame_element = driver.find_element_by_id('frame_source')
    # driver.switch_to.frame(frame_element)
    # driver.find_element_by_xpath('/html/body/div[1]/div/center/form/pre/textarea').click()
    # js = 'editor.setValue(\'' + answer + '\')'
    js = 'editor.setValue("#include <stdio.h>\nint main()\n{\n    int a,b;\n    scanf(\"%d %d\",&a, &b);\n    printf(\"%d\\n\",a+b);\n    return 0;\n}")'   #js修改
    driver.execute_script(js)
    # driver.switch_to.default_content()
    driver.find_element_by_id('Submit').click()
    sleep(10)
    try:
        message_element = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/table/tbody/tr[1]/td[4]/span')
        while message_element.text == '等待' or message_element.text == '编译中':
            # print(message_element.text)
            sleep(0.8)
            message_element = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/table/tbody/tr[1]/td[4]/span')
    except NoSuchElementException:
        try:
            message_element = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/table/tbody/tr[1]/td[4]/a')
        except NoSuchElementException:
            message_element = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/table/tbody/tr[1]/td[4]/span')
    except Exception as e:
        return '获取结果超时, erroe %s' % e
    message = message_element.text
    return message


if __name__ == "__main__":
    for nodelist in NODELIST:  # 分布式
        # driver = Remote(command_executor='http://' + nodelist.get('host'),
        #                 desired_capabilities=nodelist.get('DesiredCapabilities')
        #                 )
        # driver = driver.browser(NODELIST[1].get('host'), NODELIST[1].get('browserName'))
        driver = webdriver.Chrome()
        driver.get('http://zwu.hustoj.com')
        answer = DEFAULT_ANSWER
        message = problem_test(driver, answer=answer)
        print(message)
        driver.quit()
