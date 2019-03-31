# -*- coding:utf-8 -*-
"""
 @time    : 2019/2/20 13:12
 @desc    : 基础配置文档
 @Author  : Sorke
 @Email   : sorker0129@hotmail.com
"""
import os
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities as DC

BASE_DIR = os.path.dirname(os.path.abspath(__file__))   # 当前文件夹目录
DATA_DIR = os.path.join(BASE_DIR, 'data')               # 当前文件夹目录下的date目录
IMG_DIR = os.path.join(DATA_DIR, 'img')                 # 当前文件夹目录下的img目录
LOG_DIR = os.path.join(DATA_DIR, 'log')
LONG_DATE = 999999999999999                             # 默认长整型

NODELIST = [
    # {"host": "127.0.0.1:4444/wd/hub", "DesiredCapabilities": DC.CHROME},  # 分布式节点的地址、自动化端口、运行的浏览器驱动
    {"host": "127.0.0.1:5555/wd/hub", "DesiredCapabilities": DC.CHROME},
    # {"host": "10.60.76.127:8888/wd/hub", "DesiredCapabilities": DC.CHROME},
    {"host": "10.60.76.116:6666/wd/hub", "DesiredCapabilities": DC.CHROME},
]   # 分布式地址

DEFAULT_ANSWER_ID = 1000

DEFAULT_ANSWER = '#include <stdio.h>\n' \
                 'int main()\n' \
                 '{\n' \
                 'int a,b;\n' \
                 'scanf("%d %d",&a, &b);\n' \
                 'printf("%d\\n",a+b);\n' \
                 'return 0;\n' \
                 '}'



def windowsMasterNode():
    print('start hub')
    result = os.popen('java -jar ../selenium-server-standalone-3.141.59.jar -role hub')
    return result


def windowsNode():
    print('start node')
    result = os.popen('java -jar ../selenium-server-standalone-3.141.59.jar -role node -port 5555')
    return result


urls = ['http://zwu.hustoj.com/', 'http://zwu.hustoj.com/bbs.php', 'http://zwu.hustoj.com/faqs.php', 'http://zwu.hustoj.com/problemset.php', 'http://zwu.hustoj.com/status.php', 'http://zwu.hustoj.com/ranklist.php', 'http://zwu.hustoj.com/recent-contest.php', 'http://zwu.hustoj.com/contest.php', 'http://zwu.hustoj.com/#', 'http://zwu.hustoj.com/loginpage.php', 'http://zwu.hustoj.com/registerpage.php', 'http://zwu.hustoj.com/discuss3/', 'http://zwu.hustoj.com/discuss3/discuss.php?#', 'http://zwu.hustoj.com/discuss3/newpost.php', 'http://zwu.hustoj.com/discuss3/discuss.php', 'http://zwu.hustoj.com/discuss3/discuss.php?pid=1328', 'http://zwu.hustoj.com/userinfo.php?user=2016011160', 'http://zwu.hustoj.com/discuss3/thread.php?tid=28', 'http://zwu.hustoj.com/discuss3/discuss.php?pid=1247', 'http://zwu.hustoj.com/userinfo.php?user=2016011304', 'http://zwu.hustoj.com/discuss3/thread.php?tid=18', 'http://zwu.hustoj.com/discuss3/discuss.php?pid=1102', 'http://zwu.hustoj.com/userinfo.php?user=2016011109', 'http://zwu.hustoj.com/discuss3/thread.php?tid=1', 'http://zwu.hustoj.com/discuss3/discuss.php?pid=1141', 'http://zwu.hustoj.com/userinfo.php?user=2016011224', 'http://zwu.hustoj.com/discuss3/thread.php?tid=7', 'http://zwu.hustoj.com/discuss3/thread.php?tid=5', 'http://zwu.hustoj.com/discuss3/discuss.php?pid=1078', 'http://zwu.hustoj.com/discuss3/thread.php?tid=2', 'http://zwu.hustoj.com/faqs.php#', 'http://zwu.hustoj.com/index.php', 'http://zwu.hustoj.com/problemset.php#', 'http://zwu.hustoj.com/problemset.php?page=2', 'http://zwu.hustoj.com/problemset.php?page=3', 'http://zwu.hustoj.com/problemset.php?page=4', 'http://zwu.hustoj.com/problemset.php?page=5', 'http://zwu.hustoj.com/problemset.php?page=6', 'http://zwu.hustoj.com/problemset.php?page=7', 'http://zwu.hustoj.com/problem.php?id=1000', 'http://zwu.hustoj.com/status.php?problem_id=1000&jresult=4', 'http://zwu.hustoj.com/status.php?problem_id=1000', 'http://zwu.hustoj.com/status.php?problem_id=1093&jresult=4', 'http://zwu.hustoj.com/status.php?problem_id=1093', 'http://zwu.hustoj.com/problem.php?id=1094', 'http://zwu.hustoj.com/status.php?problem_id=1094&jresult=4', 'http://zwu.hustoj.com/status.php?problem_id=1094', 'http://zwu.hustoj.com/problem.php?id=1095', 'http://zwu.hustoj.com/status.php?problem_id=1095&jresult=4', 'http://zwu.hustoj.com/status.php?problem_id=1098', 'http://zwu.hustoj.com/problem.php?id=1099', 'http://zwu.hustoj.com/status.php?problem_id=1099&jresult=4', 'http://zwu.hustoj.com/status.php?problem_id=1099', 'http://zwu.hustoj.com/status.php#', 'http://zwu.hustoj.com/userinfo.php?user=test248506210390830', 'http://zwu.hustoj.com/userinfo.php?user=test415491463939034', 'http://zwu.hustoj.com/userinfo.php?user=test819121354056467', 'http://zwu.hustoj.com/userinfo.php?user=test540221672658081', 'http://zwu.hustoj.com/userinfo.php?user=test', 'http://zwu.hustoj.com/userinfo.php?user=test595835314857604', 'http://zwu.hustoj.com/userinfo.php?user=test339927540571105', 'http://zwu.hustoj.com/ranklist.php?scope=d', 'http://zwu.hustoj.com/ranklist.php?scope=w', 'http://zwu.hustoj.com/ranklist.php?scope=m', 'http://zwu.hustoj.com/ranklist.php?scope=y', 'http://zwu.hustoj.com/status.php?user_id=2016011160&jresult=4', 'http://zwu.hustoj.com/status.php?user_id=2016011160', 'http://zwu.hustoj.com/status.php?user_id=2016011173&jresult=4', 'http://zwu.hustoj.com/status.php?user_id=2016011173', 'http://zwu.hustoj.com/userinfo.php?user=2016011067', 'http://zwu.hustoj.com/status.php?user_id=2016011067&jresult=4', 'http://zwu.hustoj.com/status.php?user_id=2016011067', 'http://zwu.hustoj.com/status.php?user_id=2016016230&jresult=4', 'http://zwu.hustoj.com/status.php?user_id=2016016230', 'http://zwu.hustoj.com/userinfo.php?user=2016011207', 'http://zwu.hustoj.com/status.php?user_id=2016011207&jresult=4', 'http://zwu.hustoj.com/status.php?user_id=2016011207', 'http://zwu.hustoj.com/userinfo.php?user=2016011342', 'http://zwu.hustoj.com/status.php?user_id=2016011342&jresult=4', 'http://zwu.hustoj.com/status.php?user_id=2016011342', 'http://zwu.hustoj.com/userinfo.php?user=2016011073', 'http://zwu.hustoj.com/status.php?user_id=2016011073&jresult=4', 'http://zwu.hustoj.com/status.php?user_id=2016011073', 'http://zwu.hustoj.com/userinfo.php?user=2017010609', 'http://zwu.hustoj.com/status.php?user_id=2017010609&jresult=4', 'http://zwu.hustoj.com/status.php?user_id=2017010609', 'http://zwu.hustoj.com/userinfo.php?user=2016011039', 'http://zwu.hustoj.com/status.php?user_id=2016011039&jresult=4', 'http://zwu.hustoj.com/status.php?user_id=2016011039', 'http://zwu.hustoj.com/status.php?user_id=2016011170&jresult=4', 'http://zwu.hustoj.com/status.php?user_id=2016011170', 'http://zwu.hustoj.com/userinfo.php?user=2017010602', 'http://zwu.hustoj.com/status.php?user_id=2016011328&jresult=4', 'http://zwu.hustoj.com/status.php?user_id=2016011328', 'http://zwu.hustoj.com/userinfo.php?user=xhh', 'http://zwu.hustoj.com/status.php?user_id=xhh&jresult=4', 'http://zwu.hustoj.com/status.php?user_id=xhh', 'http://zwu.hustoj.com/userinfo.php?user=2016011278', 'http://zwu.hustoj.com/status.php?user_id=2016011278&jresult=4', 'http://zwu.hustoj.com/status.php?user_id=2016011278', 'http://zwu.hustoj.com/userinfo.php?user=2016011251', 'http://zwu.hustoj.com/status.php?user_id=2016011251&jresult=4', 'http://zwu.hustoj.com/status.php?user_id=2016011251', 'http://zwu.hustoj.com/userinfo.php?user=2016011331', 'http://zwu.hustoj.com/status.php?user_id=2016011331&jresult=4', 'http://zwu.hustoj.com/status.php?user_id=2016011331', 'http://zwu.hustoj.com/userinfo.php?user=2016011227', 'http://zwu.hustoj.com/status.php?user_id=2016011227&jresult=4', 'http://zwu.hustoj.com/status.php?user_id=2016011227', 'http://zwu.hustoj.com/userinfo.php?user=2016011181', 'http://zwu.hustoj.com/status.php?user_id=2016011181&jresult=4', 'http://zwu.hustoj.com/status.php?user_id=2016011181', 'http://zwu.hustoj.com/ranklist.php?start=0', 'http://zwu.hustoj.com/ranklist.php?start=50', 'http://zwu.hustoj.com/ranklist.php?start=100', 'http://zwu.hustoj.com/ranklist.php?start=150', 'http://zwu.hustoj.com/ranklist.php?start=200', 'http://zwu.hustoj.com/ranklist.php?start=250', 'http://zwu.hustoj.com/ranklist.php?start=300', 'http://zwu.hustoj.com/ranklist.php?start=350', 'http://zwu.hustoj.com/ranklist.php?start=400', 'http://zwu.hustoj.com/ranklist.php?start=850', 'http://zwu.hustoj.com/recent-contest.php#', 'http://zwu.hustoj.com/contest.php#', 'http://zwu.hustoj.com/contest.php?cid=1135', 'http://zwu.hustoj.com/contest.php?cid=1100', 'http://zwu.hustoj.com/contest.php?cid=1099', 'http://zwu.hustoj.com/contest.php?cid=1098', 'http://zwu.hustoj.com/contest.php?cid=1097', 'http://zwu.hustoj.com/contest.php?cid=1096', 'http://zwu.hustoj.com/contest.php?cid=1095', 'http://zwu.hustoj.com/contest.php?cid=1094', 'http://zwu.hustoj.com/contest.php?cid=1093', 'http://zwu.hustoj.com/contest.php?cid=1092', 'http://zwu.hustoj.com/contest.php?cid=1090', 'http://zwu.hustoj.com/contest.php?cid=1089', 'http://zwu.hustoj.com/contest.php?cid=1088', 'http://zwu.hustoj.com/contest.php?cid=1087', 'http://zwu.hustoj.com/contest.php?cid=1086', 'http://zwu.hustoj.com/contest.php?cid=1085', 'http://zwu.hustoj.com/contest.php?cid=1084', 'http://zwu.hustoj.com/contest.php?cid=1026', 'http://zwu.hustoj.com/contest.php?cid=1025', 'http://zwu.hustoj.com/contest.php?cid=1024', 'http://zwu.hustoj.com/contest.php?cid=1023', 'http://zwu.hustoj.com/contest.php?cid=1022', 'http://zwu.hustoj.com/contest.php?cid=1021', 'http://zwu.hustoj.com/contest.php?cid=1020', 'http://zwu.hustoj.com/contest.php?cid=1019', 'http://zwu.hustoj.com/contest.php?cid=1018', 'http://zwu.hustoj.com/contest.php?cid=1017', 'http://zwu.hustoj.com/contest.php?cid=1016', 'http://zwu.hustoj.com/contest.php?cid=1015', 'http://zwu.hustoj.com/contest.php?cid=1014', 'http://zwu.hustoj.com/contest.php?cid=1013', 'http://zwu.hustoj.com/contest.php?cid=1012', 'http://zwu.hustoj.com/contest.php?cid=1011', 'http://zwu.hustoj.com/contest.php?cid=1010', 'http://zwu.hustoj.com/contest.php?cid=1009', 'http://zwu.hustoj.com/contest.php?cid=1008', 'http://zwu.hustoj.com/contest.php?cid=1007', 'http://zwu.hustoj.com/contest.php?cid=1006', 'http://zwu.hustoj.com/contest.php?cid=1004', 'http://zwu.hustoj.com/contest.php?cid=1003', 'http://zwu.hustoj.com/contest.php?cid=1000', 'http://zwu.hustoj.com/loginpage.php#', 'http://zwu.hustoj.com/lostpassword.php', 'http://zwu.hustoj.com/registerpage.php#']

if __name__ == "__main__":
    windowsNode()
    windowsMasterNode()
