# -*- coding:utf-8 -*-
"""
 @time    : 2019/3/1 14:11
 @desc    : this is a desc
 @Author  : Sorke
 @Email   : sorker0129@hotmail.com
"""

class defaultError(Exception):
    def __init__(self, *args):
        self.args = args
