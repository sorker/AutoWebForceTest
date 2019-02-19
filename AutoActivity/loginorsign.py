# -*- coding:utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import UnexpectedAlertPresentException
from time import time
from AutoActivity import configs

IMG_DIR = configs.IMG_DIR


class loginorsign():
    # driver为浏览器驱动，user为用户名，pwd为密码
    def __init__(self, driver):
        self.driver = driver

    def login(self, user, pwd):
        """使用登录方法可直接跳转到登录页面"""
        try:
            start = time()
            self.driver.get('http://zwu.hustoj.com/loginpage.php')
            username = self.driver.find_element_by_xpath('/html/body/div[1]/div/form/div[1]/div/input')
            password = self.driver.find_element_by_xpath('/html/body/div[1]/div/form/div[2]/div/input')
            submit = self.driver.find_element_by_xpath('/html/body/div[1]/div/form/div[3]/div[1]/button')
            username.clear()
            password.clear()
            username.send_keys(user)
            password.send_keys(pwd)
            submit.click()
            self.driver.get('http://zwu.hustoj.com')  # 登陆后回到主页
            end = time()
            print(end - start)
            return 'login: success'
        except UnexpectedAlertPresentException as e:
            # print(e.msg)
            # message = str(e.msg).split(':')[1].split('}')[0]   # 得到alert信息
            # self.driver.save_screenshot(IMG_DIR + '\\' + str(int(time())) + '.png')
            # print(message)
            return 'login: UserName or Password Wrong'
        except Exception:
            # print('Expection occur')
            # print(e)
            return '未知错误，请联系管理员'



        '''
        # alert = self.driver.switch_to.alert
        # if alert.text != '':
        #     message = alert.text
        #     alert.accept()
        #     return message
        # else:
        #     self.driver.get('http://zwu.hustoj.com')
        #     return 'login seccess'
        '''

    def sign(self, user, pwd):
        """使用注册方法可直接跳转到注册页面"""
        try:
            start = time()
            self.driver.get('http://zwu.hustoj.com/registerpage.php')
            username = self.driver.find_element_by_xpath('/html/body/div[1]/div/form/center/table/tbody/tr[2]/td[2]/input')
            password = self.driver.find_element_by_xpath('/html/body/div[1]/div/form/center/table/tbody/tr[4]/td[2]/input')
            passwordagain = self.driver.find_element_by_xpath('/html/body/div[1]/div/form/center/table/tbody/tr[5]/td[2]/input')
            submit = self.driver.find_element_by_xpath('/html/body/div[1]/div/form/center/table/tbody/tr[8]/td[2]/input[1]')
            username.clear()
            password.clear()
            passwordagain.clear()
            username.send_keys(user)
            password.send_keys(pwd)
            passwordagain.send_keys(pwd)
            submit.click()
            end = time()
            print(end - start)
            return 'sign: success'
        except UnexpectedAlertPresentException as e:
            return 'sign: User ID Too Short! Password should be Longer than 6!'
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
    a = loginorsign(driver=webdriver.Firefox())
    print(a.sign(user='1', pwd=''))
    print(a.login(user='test', pwd='12346'))




