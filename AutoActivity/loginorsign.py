# -*- coding:utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import UnexpectedAlertPresentException
from time import time
from AutoActivity import configs
from AutoActivity import driverremote

IMG_DIR = configs.IMG_DIR
NODELIST = configs.NODELIST[0]

def login(driver, url, user, pwd):
    """
    :param self:
    :param driver:  driver为浏览器驱动
    :param url:     登录地址
    :param user:    user为用户名
    :param pwd:     pwd为密码
    :return:        message
    desc:使用登录方法可直接跳转到登录页面
    """
    try:
        driver.get(url)
        username = driver.find_element_by_xpath('//input[contains(@placeholder, "用户名")]')
        password = driver.find_element_by_xpath('//input[contains(@placeholder, "密码")]')
        submit = driver.find_element_by_xpath('//*[@type="submit"]')
        username.clear()
        password.clear()
        username.send_keys(user)
        password.send_keys(pwd)
        submit.click()
        driver.get('http://zwu.hustoj.com')  # 登陆后回到主页
        return 'login: success'
    except UnexpectedAlertPresentException:
        # print(e.msg)
        # message = str(e.msg).split(':')[1].split('}')[0]   # 得到alert信息
        # self.driver.save_screenshot(IMG_DIR + '\\' + str(int(time())) + '.png')
        # print(message)
        return 'login: UserName or Password Wrong'
    except Exception as e:
        # print('Expection occur')
        # print(e)
        return '未知错误.error: %s' % e


def sign(driver, user, pwd):
    """使用注册方法可直接跳转到注册页面"""
    try:
        driver.get('http://zwu.hustoj.com/registerpage.php')
        username = driver.find_element_by_xpath('/html/body/div[1]/div/form/center/table/tbody/tr[2]/td[2]/input')
        password = driver.find_element_by_xpath('/html/body/div[1]/div/form/center/table/tbody/tr[4]/td[2]/input')
        passwordagain = driver.find_element_by_xpath('/html/body/div[1]/div/form/center/table/tbody/tr[5]/td[2]/input')
        submit = driver.find_element_by_xpath('/html/body/div[1]/div/form/center/table/tbody/tr[8]/td[2]/input[1]')
        username.clear()
        password.clear()
        passwordagain.clear()
        username.send_keys(user)
        password.send_keys(pwd)
        passwordagain.send_keys(pwd)
        submit.click()
        driver.switch_to.default_content()
        # print(user, pwd, 'success')
        return 'sign: success'
    except UnexpectedAlertPresentException:
        return 'sign: User ID Too Short OR Password should be Longer than 6!'
    except Exception:
        return '未知错误，请联系管理员'
    '''
    # alert = self.driver.switch_to.alert()
    # if alert.text:
    #     message = alert.text
    #     alert.accept()
    #     return message
    # else:
    #     self.driver.get('http://zwu.hustoj.com/registerpage.php')
    #     return 'sign seccess'
    '''


if __name__ == "__main__":
    # driver = webdriver.Firefox()
    driver = driverremote.browser(NODELIST.get('host'), NODELIST.get('DesiredCapabilities'))
    result = sign(driver, user='1', pwd='')
    print(result)
    url = 'http://zwu.hustoj.com/loginpage.php'
    result = login(driver, url, user='test', pwd='12346')
    print(result)
    driver.quit()




