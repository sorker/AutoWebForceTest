# -*- coding:utf-8 -*-
"""
 @time    : 2019/2/20 13:12
 @desc    : 用户名文件的创建和获取
 @Author  : Sorke
 @Email   : sorker0129@hotmail.com
"""
import xlrd
import xlwt
import os
from random import randint
from AutoActivity import configs

DATA_DIR = configs.DATA_DIR
LONG_DATE = configs.LONG_DATE


# 新建表并生成随机用户名密码
def usersput(filename, num):
    """
    :param filename:  文件名, 例：账号密码.xls
    :param num: 用户密码的数量
    :return:  success
    """
    try:
        filename = os.path.join(DATA_DIR, filename)
        if not os.path.isfile(filename):  # 判断文件是否存在，如果不存在就创建一个
            open(filename, 'w')
            workbook = xlwt.Workbook()
            sheet1 = workbook.add_sheet('sheet1', cell_overwrite_ok=True)
            sheet1.write(0, 0, 'user')
            sheet1.write(0, 1, 'pwd')
            for i in range(num):
                user_pwd = 'test' + str(randint(1, LONG_DATE))
                sheet1.write(i + 1, 0, user_pwd)
                sheet1.write(i + 1, 1, user_pwd)
            workbook.save(filename)
            # print('已生成有' + str(num) + '个用户的excle文件')
            return 'success'
        else:
            return '文件已存在，请更换名字'
    except Exception as e:
        return '文件生成错误, error: %s' % e


# 读取xls的用户名密码并生成字典
def readcvs(filename):
    """
    :param filename: 文件名,例：账号密码.xls
    :return:  返回账号密码列表[[user1, pwd1],[user2, pwd2]]
    """
    filename = os.path.join(DATA_DIR, filename)
    ExcelFile = xlrd.open_workbook(filename)
    sheet = ExcelFile.sheet_by_name(ExcelFile._sheet_names[0])
    # rows = sheet.row_values(0)  # 获取第一行的所有值
    cols1 = sheet.col_values(0)  # 获取第一列的所有值
    cols2 = sheet.col_values(1)  # 获取第二列的所有值
    user_pwd = []   # 账号密码列表并返回[[user1, pwd1],[user2, pwd2]]
    for i, col1 in enumerate(cols1):
        col2 = cols2[i]
        if type(col1) == float:
            col1 = int(col1)
        if type(col2) == float:
            col2 = int(col2)
        # print(clo1)
        a = [col1, col2]
        user_pwd.append(a)
    user_pwd.pop(0)
    return user_pwd


if __name__ == "__main__":
    print(usersput('账号密码2.xls', 10))
    # print(readcvs('账号密码1.xls'))
