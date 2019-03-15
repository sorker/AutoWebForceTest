"""
 @time    : 2019/2/20 15:32
 @desc    : 单元测试类
 @Author  : Sorke
 @Email   : sorker0129@hotmail.com
"""
import unittest
from time import sleep
from selenium import webdriver
from AutoActivity.datadeal import readcvs, usersput
from AutoActivity.loginorsign import login


class loginandsigntest(unittest.TestCase):
    def setUp(self):
        self.filename = '账号密码.xls'
        self.filenames = '账号密码1.xls'
        self.users = readcvs(self.filename)  # 读取excle文件中的所以用户，得到字典
        self.user = self.users.get('user')  # 从字典中取出用户名
        self.pwd = self.users.get('pwd')  # 从字典中取出密码
        driver = webdriver.Chrome()
        self.user_active = login(driver=driver)
        print('start')

    def test_login(self):
        """登录网页"""
        message = self.user_active.login(self.user[0], self.pwd[0])  # 获得登录后的返回结果
        self.assertEqual(message, 'login seccess')  # 对比结果是否想要的值

    # def test_sign(self):
    #     """批量注册用户"""
    #     usersput(self.filenames, 1)  # 随机生成多个用户，存放到xls文件夹
    #     message = self.user_active.sign(self.user[0], self.pwd[0])
    #     self.assertEqual(message, 'sign seccess')

    def tearDown(self):
        print('end')


if __name__ == '__main__':
    unittest.main()
