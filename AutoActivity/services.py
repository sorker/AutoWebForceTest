# -*- coding:utf-8 -*-
import pexpect
import re


def ssh_command(host, user, password, command):
    ssh_new_key = 'Are you sure you want to continue connecting'
    child = pexpect.spawn('ssh -l %s %s %s' % (user, host, command))
    i = child.expect([pexpect.TIMEOUT, ssh_new_key, 'password: '])
    if i == 0:
        print('ERROR!')
        print('SSH could not login. Here is what SSH said:')
        print(child.before, child.after)
        return None
    if i == 1:
        child.sendline('yes')
        child.expect('password: ')
        i = child.expect([pexpect.TIMEOUT, 'password: '])
        if i == 0:
            print('ERROR!')
            print('SSH could not login. Here is what SSH said:')
            print(child.before, child.after)
            return None
    child.sendline(password)
    return child


if __name__ in '__main__':
    a = ssh_command('192.168.0.114', 'root', '123456', 'cat /proc/meminfo')
    print(a)


'''
---------------------
作者：代码帮
来源：CSDN
原文：https://blog.csdn.net/ITLearnHall/article/details/80693913
版权声明：本文为博主原创文章，转载请附上博文链接！
'''