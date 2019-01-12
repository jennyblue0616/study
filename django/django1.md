---
author: 于梦娇
title: Django
---

# Django

  ## Django简介



  Django是一个用python编写的Web应用框架,采用了MVC框架模式,M(Model-模式)V(View-视图)C(Controller-控制器)是一种软件设计的典范.

  View视图是指用户看到并与之交互的界面.通过Model对数据库进行操作:业务逻辑判断,数据库的存取,应用于模型的代码只需写一次就可以被多个视图重用,减少了代码的重复性.Controller是指控制器接收用户的输入并调用模型和视图完成用户的需求.

![MVC](D:\picture\1.png)

Django===>MVT

M(模型层)

V(视图):处理业务逻辑

T(模板Template):html



## virtualenv虚拟环境

  virtualenv使用场景:当开发成员负责多个项目的时候，每个项目安装的库又是有很多差距的时候，会使用虚拟环境将每个项目的环境给隔离开来。 

  安装virtualenv,django

  ```
首先在d盘里新建一个名为env的文件夹
在命令窗口进入env文件夹,输入:
1.
pip install virtualenv
2.
virtualenv --no-site-packages evn(虚拟环境命名)
参数: --no-site-package 意为纯净的虚拟环境
参数: -p 是python版本,如果只有一个版本可不写
3.
pip list 查看全局安装了哪些软件
4.
cd evn\Scripts
activate 进入虚拟环境
5.
pip install django==1.11 在纯净的环境里面装django
6.
deactivate 退出虚拟环境
  ```

## 创建,启动项目

1. 创建项目

在cmd命令窗口中输入`django -admin startproject day01`,创建一个名为day01的项目,然后用pycharm打开,一共有五个文件![2](D:\picture\2.png)

(1)__init__ 文件-空

(2)settings 文件-配置信息 ,例如Installed Apps安装应用,Templates 页面的路径,Databases 数据等修改,都是在这个文件里修改的

(3)urls 文件-路由,定义路径

(4)wsgi文件-部署项目的配置

(5)manage文件-工具管理文件,用来启动项目

2. 启动项目

  Terminal窗口中输入python manager.py查看命令,一定要在虚拟环境下执行!![4](D:\picture\4.png)

`python manager.py runserver 0.0.0.0(IP):8080(PORT)`

(0.0.0.0)所有用户都可以访问,要么都写IP和端口,要么只写端口

3. 访问管理后台

`http://localhost:8080/admin`

`http://127.0.0.1:8080/admin/`

4. 修改数据库的配置

   先在mysql中创建名为dj6的数据库

```
settings.py文件中
DATABASES={
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dj6',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': 3306
}
```

5. 映射模型到数据库中

 `python manage.py migrate`

数据库中会有新创建的表格![3](D:\picture\3.png)

其中,auth开头的是跟权限相关的表

6. 安装数据库驱动,初始化数据库驱动

```
安装数据库驱动
terminal中输入pip install pymysql

初始化数据库驱动
在init文件中输入
import pymysql
pymysql.install_as_MySQLdb()

```

7. 创建超级管理员命令

`python manage.py createsuperuser`

输入用户名和密码,就可以创建超级管理员,然后在http://localhost:8080/admin/就可以登录了.

