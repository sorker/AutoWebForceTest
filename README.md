# AutoWebForceTest
  提供可使用的通用工具为：服务器监控、自动多用户登录。
  
  其他的都是我毕业设计的代码
  
  可编辑的config可设置：分布式服务器等内容。/AutoActivity/configs.py
  

  ####使用前环境配置要求：
  windows7以上，安装有chrome、firefox、谷歌浏览器驱动最新版、Firefox浏览器驱动最新版、java8环境
  
  我的python环境：版本3.7.0，安装的基本包：selenium、os、request、django
  
  运行config下的主程序启动本地分布式环境，当然最好用cmd启动(在文件夹下的cmd中输入：java -jar ../selenium-server-standalone-3.141.59.jar -role hub、java -jar ../selenium-server-standalone-3.141.59.jar -role node -port 5555)
  
  在文件夹下用cmd输入命令：python manage.py runserver
