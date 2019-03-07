# -*- coding:utf-8 -*-
"""
 @time    : 2019/3/1 14:11
 @desc    : 自定义报错
 @Author  : Sorke
 @Email   : sorker0129@hotmail.com
"""

class loginError(Exception):
    def __init__(self, *args):
        self.args = args


class problemError(Exception):
    def __init__(self, *args):
        self.args = args


class signError(Exception):
    def __init__(self, *args):
        self.args = args
