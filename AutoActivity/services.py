# -*- coding:utf-8 -*-
"""
 @time    : 2019/2/20 13:12
 @desc    : 所有与服务器的ssh通讯
 @Author  : Sorke
 @Email   : sorker0129@hotmail.com
"""
import paramiko
import re
from time import sleep
from AutoActivity import configs

LOG_DIR = configs.LOG_DIR


def sshConnect(hostname, username, password, port):
    """
    创建 ssh 连接函数
    hostname, port, username, password,访问linux的ip，端口，用户名以及密码
    """
    paramiko.util.log_to_file(LOG_DIR)
    try:
        # 创建一个SSH客户端client对象
        ssh_client = paramiko.SSHClient()
        # 获取客户端host_keys,默认~/.ssh/known_hosts,非默认路径需指定
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 创建SSH连接
        ssh_client.connect(hostname, port, username, password)
    except Exception as e:
        print("SSH链接失败：[hostname:%s];[username:%s];[error:%s]" % (hostname, username, e))
        ssh_client = False
    return ssh_client


def sshCommand(sshClient, command):
    """创建命令执行函数,command 传入linux运行指令"""
    stdin, stdout, stderr = sshClient.exec_command(command)
    filesystem_usage = stdout.readlines()
    return filesystem_usage


def sshClose(ssh_client):
    # 关闭ssh
    ssh_client.close()


def sshMemInfo(service):
    """内存监控"""
    sshRes = sshCommand(service, 'cat /proc/meminfo')
    mem_values = re.findall("(\d+)\ kB", ",".join(sshRes))
    MemTotal = mem_values[0]  # 总内存
    MemFree = mem_values[1]  # 空闲内存
    Buffers = mem_values[2]  # 给文件的缓冲大小
    Cached = mem_values[3]  # 高速缓冲存储器使用的大小
    SwapCached = mem_values[4]  # 被高速缓冲存储用的交换空间大小
    SwapTotal = mem_values[13]  # 交换内存总共
    SwapFree = mem_values[14]  # 交换内存剩余
    '''
    print('******************************内存监控*********************************' )
    print("*******************时间：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "******************")
    print("总内存：", MemTotal)
    print("空闲内存：", MemFree)
    print("给文件的缓冲大小:", Buffers)
    print("高速缓冲存储器使用的大小:", Cached)
    print("被高速缓冲存储用的交换空间大小:", SwapCached)
    print("给文件的缓冲大小:", Buffers)
    if int(SwapTotal) == 0:
        print("交换内存总共为：0")
    else:
        Rate_Swap = 100 - 100 * int(SwapFree) / float(SwapTotal)
        print("交换内存利用率：", Rate_Swap)

    Free_Mem = int(MemFree) + int(Buffers) + int(Cached)
    Used_Mem = int(MemTotal) - Free_Mem
    # Rate_Mem = 100 * Used_Mem / float(MemTotal)
    # print("内存利用率：%.2f " % (100+Rate_Mem) + "%")
    '''
    return int(int(MemTotal) / 1024), int((int(MemTotal) - int(MemFree)) / 1024)


def sshDiskInfo(service):
    """磁盘空间监控"""
    sshRes = sshCommand(service, 'df -h')
    sshResStr = ''.join(sshRes)
    sshResList = sshResStr.strip().split('\n')
    sshResLists = []
    disk_values = re.findall("(\d+)", str(sshResList[1:1]))
    if not disk_values:
        fisrtStr = ' '.join(sshResList[1:3])
        sshResLists.append(fisrtStr.strip().split())
    for disk in sshResList[3:]:
        sshResLists.append(disk.strip().split())
    '''
    print('************************磁盘空间监控****************************')
    print("*******************时间：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "******************")
    for disklist in sshResLists:
        FileSystem = disklist[0]    # 文件系统
        print("\t文件系统：", FileSystem)
        HardTotal = disklist[1]     # 容量
        print("\t容量：", HardTotal)
        HardUser = disklist[2]      # 已用
        print("\t已用：", HardUser)
        HardFree = disklist[3]      # 可用
        print("\t可用：", HardFree)
        print("\t已用%挂载点：", disklist[4])
        print("\t磁盘挂载的目录所在（挂载点）", disklist[5])
    '''
    HardTotal = sshResLists[0][1][:-1]
    HardUser = sshResLists[0][2][:-1]
    return HardTotal, HardUser


def sshComStr(service):
    """ 端口监控"""
    sshRes = sshCommand(service, 'netstat -tpln')
    sshResStr = ''.join(sshRes)
    sshResList = sshResStr.strip().split('\n')
    sshResLists = []
    for sshCom in sshResList[2:]:
        sshResLists.append(sshCom.strip().split())
    '''
    ReciveTotal = 0 # 接收总流量
    SendTotal = 0   # 发送总流量
    print('******************************端口监控*********************************')
    print("*******************时间：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "******************")    
    for temp in sshResLists:
        print("\t Proto:",temp[0])
        print("\t 接收-Q:", temp[1])
        print("\t 发送-Q:", temp[2])
        print("\t Local Address:", temp[3])
        print("\t  Foreign Address:", temp[4])
        print("\t State:", temp[5])
        print("\t PID/Program name:", temp[6])
        print("****************************************")
        ReciveTotal += int(temp[1])
        SendTotal += int(temp[2])
    '''
    return sshResLists


def sshLoadStat(service):
    """    负载均衡    """
    sshRes = sshCommand(service, 'cat /proc/loadavg')
    sshResStr = ''.join(sshRes)
    loadavgs = sshResStr.strip().split()
    LoadStat = loadavgs[2]
    Theards = loadavgs[3]
    '''
    print('************************负载均衡监控****************************')
    print("*******************时间：",time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),"******************")
    print("系统5分钟前的平均负载：", loadavgs[0])
    print("系统10分钟前的平均负载：", loadavgs[1])
    print("系统15分钟前的平均负载：", loadavgs[2])
    print("进程数/总进程数：",loadavgs[3])
    print("最近运行的进程id：", loadavgs[4])
    '''
    return LoadStat, Theards


def sshIONetwork(service):
    """    获取网络接口的输入和输出    """
    sshRes = sshCommand(service, 'cat /proc/net/dev')
    sshResStr = ''.join(sshRes)
    li = sshResStr.strip().split('\n')
    # print('************************获取网络接口的输入和输出监控****************************')
    # print("*******************时间：",time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),"******************")
    net = {}
    for line in li[2:]:
        line = line.split(":")
        eth_name = line[0].strip()
        # if eth_name != 'lo':
        net_io = {}
        net_io['Receive'] = round(float(line[1].split()[0]) / (1024.0 * 1024.0), 3)
        net_io['Transmit'] = round(float(line[1].split()[8]) / (1024.0 * 1024.0), 3)
        net[eth_name] = net_io
    ReceiveTotal = 0  # 接收总流量
    TransmitTotal = 0  # 发送总流量
    for k, v in net.items():
        if k != 'lo':
            ReceiveTotal += v.get('Receive')
            TransmitTotal += v.get('Transmit')
    return ReceiveTotal, TransmitTotal


def httpLinks(service):
    """80端口连接总数"""
    sshRes = sshCommand(service, 'netstat -nat|grep -i "80"|wc -l')
    sshResStr = ''.join(sshRes)
    # li = sshResStr.strip().split()
    linksNum = sshResStr
    return int(linksNum)


def linuxNode(service):
    sshRes = sshCommand(service, 'java -jar /home/node/selenium_server/selenium-server-standalone-3.141.59.jar '
                                 '-role node -port 6666 -hub http://192.168.0.114:4444/grid/register')
    sshResStr = ''.join(sshRes)
    return sshResStr


def sshCPUInfo(service):
    sshRes = sshCommand(service, 'cat /proc/stat')
    child = ''.join(sshRes)
    sleep(0.1)
    sshRes = sshCommand(service, 'cat /proc/stat')
    child1 = ''.join(sshRes)
    cpus = child.strip().split()
    cpus1 = child1.strip().split()
    T1 = int(cpus[1]) + int(cpus[2]) + int(cpus[3]) + int(cpus[4]) + int(cpus[5]) + int(cpus[6]) + int(cpus[8]) + int(
        cpus[9])
    T2 = int(cpus1[1]) + int(cpus1[2]) + int(cpus1[3]) + int(cpus1[4]) + int(cpus1[5]) + int(cpus1[6]) + int(
        cpus1[8]) + int(cpus1[9])
    Tol = T2 - T1
    Idle = int(cpus1[4]) - int(cpus[4])
    '''
    print('总的cpu时间1:',T1)
    print('总的cpu时间2:', T2)
    print('时间间隔内的所有时间片:', Tol)
    print('计算空闲时间idle:', Idle)
    print("计算cpu使用率：",100*(Tol-Idle)/Tol,"%")
    '''
    CPUP = round(((Tol - Idle) / Tol * 100), 2)
    if CPUP == 0:
        return 0
    return CPUP


def allTask(service):
    ServerInfo = []
    TotalM, UsedM = sshMemInfo(service)
    # print('总内存：', TotalM, 'KB，已用内存：', UsedM, 'KB')
    HardTotal, HardUser = sshDiskInfo(service)
    # print('总磁盘：', HardTotal, 'G，已用磁盘：', HardUser, 'G')
    LoadStat, Theards = sshLoadStat(service)
    # print('系统15分钟前的平均负载：', LoadStat, '进程数/总进程数：', Theards)
    ReceiveT, TransmitT = sshIONetwork(service)
    # print('接收总流量：', ReceiveT, 'MB，发送总流量：', TransmitT, 'MB')
    linksNum = httpLinks(service)
    # print('80端口连接总数:', linksNum)
    CPUP = sshCPUInfo(service)
    # print('CPU使用率:', CPUInfo, '%')

    ServerInfo = {"TotalM": TotalM, "UsedM": UsedM,
                  "HardTotal": HardTotal, "HardUser": HardUser,
                  "LoadStat": LoadStat, "Theards": Theards,
                  "ReceiveT": ReceiveT, "TransmitT": TransmitT,
                  "linksNum": linksNum, "CPUP": CPUP,
                  }
    return ServerInfo


if __name__ in '__main__':
    service = sshConnect('192.168.94.133', 'root', '123456', '22')
    # """ 端口监控"""
    # ReciveTotal, SendTotal, sshResLists = sshComStr(service)
    # print('总接收流量：', ReciveTotal, '总发送流量：', SendTotal, '端口信息 ：', sshResLists)

    args = allTask(service)
    # args = sshCPUInfo(service)
    print(args)
    # print(linuxNode(service))
    # print('q')
    sshClose(service)
