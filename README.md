# AutoWebForceTest
  提供可使用的通用工具为：服务器监控、自动多用户登录。
  
  其他的都是我毕业设计的代码
  
  可编辑的config可设置：分布式服务器等内容。
  

  ####使用前环境配置要求：
  windows7以上，至少安装有最新版chrome、谷歌浏览器驱动最新版、、java8环境、python3.5以上版本
  
  windows10直接`scoop install chromedriver`就可以安装chrome驱动了，不需要配置环境，10一下的系统需要下载驱动，安装解压到：C:\Program Files (x86)\Google\Chrome\Application下并配置到Path环境下

  我的python环境：版本3.7.0，安装的基本包：selenium、os、request、django、multiprocessing、time、re
  
  运行config下的主程序启动本地分布式环境，当然最好用cmd启动(在文件夹下的cmd中输入：
  ```
  java -jar ../selenium-server-standalone-3.141.59.jar -role hub -port 4444  主节点
  java -jar ../selenium-server-standalone-3.141.59.jar -role node -port 5555 本机分节点
  java -jar ../selenium-server-standalone-3.141.59.jar -role node -hub http://127.0.0.1:4444/grad/register -port 6666 远程分节点
  java -jar ../selenium-server-standalone-3.141.59.jar -role node -hub http://127.0.0.1:4444/grad/register -port 7777 远程分节点
  ```
  
  在/AutoActivity/configs.py需要修改成你本地的IP
  ```
  NODELIST = [
     # {"host": "127.0.0.1:4444/wd/hub", "DesiredCapabilities": DC.CHROME},   # 分布式节点的地址、自动化端口、运行的浏览器驱动(主机)
     # {"host": "127.0.0.1:5555/wd/hub", "DesiredCapabilities": DC.CHROME},    # 主机下的节点，不必要开启
     {"host": "10.60.76.113:6666/wd/hub", "DesiredCapabilities": DC.CHROME}, # 分节点
     {"host": "10.60.76.116:7777/wd/hub", "DesiredCapabilities": DC.CHROME}, # 分节点
]    # 分布式地址
```

  在AutoWebForceTest下的setting修改数据库信息
  
  在文件夹下用cmd输入命令：`python manage.py runserver` 运行网站
  
  **建议每台主机的并发数不要超过10个**