---
title: Linux
---



# Linux 系统基础命令

  ## Linux概述

  Linux是一个通用操作系统,是C语言编写的,比windows操作系统优于其可靠的安全性和稳定性,支持多用户和多任务,拥有大量的实用程序和强大的支持文档.

 www.kernel.org 是Linux的内核下载网站

## 基础命令

1. 获取登录信息- 看到用户登陆的信息

   ```
   w/who/who am i
   ```

   ​

2. 查看自己使用的Shell 

   ```
   ps(查看进程)
   kill PID(结束进程)
   kill -9 PID(强行结束进程)
   ```

   Shell也被称为“壳”，它是用户与内核交流的翻译官，简单的说就是人与计算机交互的接口。目前很多Linux系统默认的Shell都是bash（Bourne Again Shell），因为它可以使用Tab键进行命令补全、可以保存历史命令、可以方便的配置环境变量以及执行批处理操作等。

3. 查看命令的说明 

   ```
   whatis
   ```

4. 查看帮助文档

   ```
   man ps-打开命令的使用手册
   info ps-给程序员看的 
   ps --help
   ```

5. 切换用户

   ```
   su(switch user)
   sudo(super user do)-普通用户以超级管理员身份执行
   #命令行提示符-超级管理员
   $-普通用户
   ```

6. 登入登出

   ```
   adduser-创建新用户
   passwd-设置密码
   exit-退出登录
   log out
   userdel-删除用户
   ```

7. 重启和关机

   ```
   shutdown-关机
   shutdown -c 取消关机
   init 0 关机
   reboot-重启
   init 6 重启
   ```

8. 查看历史命令

   ```
   history-查看所有历史命令 上下键可以查看历史命令
   history -c 清空历史命令
   !30-执行第30行的历史命令
   ```

   ## 实用程序

   1. 创建/删除文件夹

      ```
      mkdir-make directories-创建文件夹
      rmdir-remove empty directories-删除空文件夹
      mkdir -p(parents上一级目录也会创建)
      ```

   2. 创建/删除文件

      ```
      touch/rm
      touch readme.txt 创建文件名为readme的文本文件
      rm -rf ./* 删除当前文件夹里所有文件
      ```

      - touch 命令用于创建空白文件或修改文件时间
      - rm重要参数有 -i:交互式删除 -r:删除目录并递归的删除目录中的文件和目录 -f:强制删除

   3. 切换和查看当前工作目录

      ```
      cd-change directory -改变所在目录
      pwd-print current working-查看当前工作目录
      ```

      >```
      >cd命令后面可以跟相对路径（以当前路径作为参照）或绝对路径（以/开头）来切换到指定的目录，也可以用cd ..来返回上一级目录。
      >/系统根目录相当于我的电脑
      >~用户主目录
      >```

   4. 查看目录内容-ls

      ls(list directory contents)

      -l：以长格式查看文件和目录。
      -a：显示以点开头的文件和目录（隐藏文件）。
      -R：遇到目录要进行递归展开（继续列出目录下面的文件和目录）。
      -d：只列出目录，不列出其他内容。
      -S/-t：按大小/时间排序。

   5. 查看文件内容-cat/head/tail/more/less

      ```
      cat -n(行号:命令的参数)concatnate-连接多个文件并显示到标准输出上
      ./当前目录
      ../父级目录
      /根目录
      ```

   6. 拷贝/移动文件

      ```
      cp-copy files and directories
      mv-move 可以改名字
      cp index.htm abc/efg/(文件名不变)
      cp index.html ../拷贝到上一级目录,文件重名会有提示是否覆盖
      cp -r(递归) abc /usr/hello 拷贝文件夹,名字hello
      cp -r(递归) abc /usr/hello/ 名字没变,到hello文件夹下面去了
      ```

   7. 查找文件和查找内容

      ```
      find-查找文件
      grep-查找内容
      ```

      ​

   8. 链接

      ```
      -ln
      
       ln [参数][源文件或目录][目标文件或目录]
       给文件创建软链接，为log2013.log文件创建软链接link2013，如果log2013.log丢失，link2013将失效：
       ln -s log2013.log link2013
      ```

      ​

      说明：链接可以分为硬链接和软链接（符号链接）。硬链接可以认为是一个指向文件数据的指针，就像Python中对象的引用计数，每添加一个硬链接，文件的对应链接数就增加1，只有当文件的链接数为0时，文件所对应的存储空间才有可能被其他文件覆盖。我们平常删除文件时其实并没有删除硬盘上的数据，我们删除的只是一个指针，或者说是数据的一条使用记录，所以类似于“文件粉碎机”之类的软件在“粉碎”文件时除了删除文件指针，还会在文件对应的存储区域填入数据来保证文件无法再恢复。软链接类似于Windows系统下的快捷方式，当软链接链接的文件被删除时，软链接也就失效了。

   9. 压缩/解压缩和归档/解归档

      ```
      gzip-压缩
      gunzip-解压缩 g表示遵循开源协议
      xz-压
      tar-归档文件-把多个文件合并成一个文件
         -解归档-把一个文件拆成多个文件
      tar -x(extract)v(看到过程)f(文件名)   
      ```

   10. 其他工具

    ```
    1.echo
    echo " print ' hello,world'" > hello.py
    >输出重定向
    >>追加重定向,把新的内容追加到原来内容的后面
    重定向时文件没有会自动创建新文件
    echo $a-返回a的值
    echo $[a+b]-返回a+b的结果
    2.alias
    命令的别名
    unalias rmd 删除起的别名
    3.wget
    通过网络下载文件命令
    4.ls --help | more 前面指令的输出是后面指令的输入
    |管道(进程间通信)-把前一个进程的输出当成后一个进程的输入
    进程之间通信方式:管道|,套接字
    5.wc
    word count
    统计
    6.uniq-unique-去重
    7.sort排序 先排序后去重
    8.diff  比较两个文件哪里不一样
    9.chmod-改变文件模式
    chmod u+x g+x o+x
    chmod 755
    10.chown-改变所有者
    11.发消息
    write 用户名,输入结束后按ctrl+d
    不接受消息-mesg n
    接收消息-mesg y
    wall-write all给所有人发消息
    ```


   ​

   ​

   #### 目录结构

1. /bin - 基本命令的二进制文件。

2. /boot - 引导加载程序的静态文件,系统启动。
3. /dev - 设备文件。
4. **/etc** - 配置文件。
5. /home - 普通用户主目录的父目录。
6. /lib - 共享库文件。
7. /lib64 - 共享64位库文件。
8. /lost+found - 存放未链接文件。
9. /media - 自动识别设备的挂载目录。
10. /mnt - 临时挂载文件系统的挂载点。
11. /opt - 可选插件软件包安装位置。
12. /proc - 内核和进程信息。
13. **/root** - 超级管理员用户主目录。
14. /run - 存放系统运行时需要的东西。
15. /sbin - 超级用户的二进制文件。
16. /sys - 设备的伪文件系统。
17. /tmp - 临时文件夹。
18. **/usr** - 用户应用目录。
19. /usr/bin 放指令的
20. /usr/local 安装软件
21. /var - 变量数据目录。

​

## 安装软件

 使用包管理工具

1.  yum - Yellow dog Updater Modified。

    - `yum search`：搜索软件包，例如`yum search nginx`。
    - `yum list installed`：列出已经安装的软件包，例如`yum list installed | grep zlib`。
    - `yum install`：安装软件包，例如`yum install nginx`。
    - `yum remove`：删除软件包，例如`yum remove nginx`。
    - `yum update`：更新软件包，例如`yum update`可以更新所有软件包，而`yum update tar`只会更新tar。
    - `yum check-update`：检查有哪些可以更新的软件包。
    - `yum info`：显示软件包的相关信息，例如`yum info nginx`。

2. **rpm** - Red hat Package Manager。

    ​

    Cent OS安装Python 3.7
    1.下载python源代码 

    ```
    wget https://www.python.org/ftp/python/3.7.0/Python-3.7.0.tgz
    ```

    ​
    2.解压缩

    ```
    gunzip Python-3.7.0.tgz
    ```

    ​
    3.解归档

    ```
    tar -xvf Python-3.7.0.tar
    ```

    ​
    4.安装底层依赖库
    `yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel libffi-devel`
    5.安装前的配置

    ```
    /root/Python-3.7.0./configure --prefix=/usr/local/python37 --enable-optimizations
    ```

    6.make && make install 构建安装
    && 前的执行完,后面再执行,如果前面错误,后面也不执行

    7.配置PATH环境变量 

    ```
    export PATH=$PATH:/usr/local/python37/bin
    ```

    $PATH:读取原有的path路径
    8.注册软链接(符号链接)

    ```
    ln -s /usr/local/python37/bin/python3.7 /usr/bin/python3
    ```

    ​

    ​

    ### vim-文本编辑神器

    命令模式--->编辑模式 i(insert),a(append)

    编辑模式 ---> 命令模式 `esc`

    命令模式 ---> 末行模式 : / ?

    ​

    ### 移动光标

    `hjkl`结合数字

    `HML`

    H:第一行一列 M:中间一列 L:屏幕最后一行

    0 行首

    $ 行尾

    w 下一个单词

    `gg`

     文章开头

    G 文章结尾

    ### 翻页

    ```
    ctrl+e-往下翻一行
    ctrl+y-往上翻一行
    ctrl+f-往下翻一页
    ctrl+b-往上翻一页
    ```

    ### 其他操作

    ```
     yy-复制
     p-粘贴
     dd-删除
     u-撤销
     ctrl+r-重做上一个动作
     ctrl+x ctrl+o - 代码提示
     chmod u(user)+x(x执行权限) 改变模式

     :w
     :q
     :qa - 退出全部窗口
     :set nu
     :set ts=4
     :set autoindent 自动缩进
     :1,$s/被替换的内容/替换后的内容/gice
       -g: 全局模式
       -i: 忽略大小写
       -c: 确认模式
       -e: 忽略错误
      /正则表达式 - 正向搜索
      n - 正向搜索
      N - 反向搜索
      ?正则表达式 - 反向搜索

    如果vim打开了多个文件可以在末行模式中通过
        :b <编号> 切换到其他文件
        :ls - 查看打开的文件

    拆分窗口
        :vs 垂直拆分
        :sp 水平拆分
        ctrl+w ctrl+w - 在窗口之间切换光标

    设置快捷键
        :imap-输入模式下的快捷键
        :inoremap-不要递归的map

    想拿到命令行参数
        在py文件中插入import sys
        sys.argv可以拿到命令行参数
        三元条件运算符: y = year if 条件1 else 条件二
        
     命令mount挂载u盘
     umount反挂载
     
    执行命令,把命令的执行结果赋给变量
    username=`whoami`

    命令之间用;隔开-一个一个执行
    用&&隔开-前面成功了后面才执行
    ||-前面不成功才执行后面的
    ```

    ### Nginx服务器

    ​

    ```

        一.
           Nginx是一个http服务器。是一个使用c语言开发的高性能的http服务器及反向代理服务器。
        二.
           Nginx 应用场景
           1、 http服务器。Nginx是一个http服务可以独立提供http服务。可以做网页静态服务器。

           2、 虚拟主机。可以实现在一台服务器虚拟出多个网站。例如个人网站使用的虚拟主机。

           - 基于端口的，不同的端口
           - 基于域名的，不同域名

           3、 反向代理，负载均衡。当网站的访问量达到一定程度后，单台服务器不能满足用户的请求时，需         要用多台服务器集群可以使用nginx做反向代理。并且多台服务器可以平均分担负载，不会因为         某台服务器负载高宕机而某台服务器闲置的情况。
        三.
           使用Nginx:
           systemctl start nginx
           nginx 首页html文件放在/usr/share/nginx/html里
    ```

    ### 

    ### 网络访问和管理

    ​

    ```
    1.通过网络获取资源-wget

    2.显示/操作网络配置(旧)-ifconfig 
    if:interface 网络端口的配置
    查看Linux系统中的IP地址
      显示/操作网络配置(新)-ip

    3.网络可达性检查-ping
    ping www.baidu.com

    4.查看网络服务和端口-netstat
    netstat -nap | grep nginx
    n(number)a(all)p(process)

    5.安全远程连接-ssh
    ssh root@别人的公网IP
    连接到别人的服务器

    6.安全文件拷贝-scp
    scp 文件名 root@IP地址:/root/新文件名

    7.安全文件传输-sftp
    sftp root@别人公网IP
    下载文件-get
    上传文件-put
    看自己系统的目录 lls
    退出 quit/bye
    ```

    | 计算机网络分层架构模型                    |         |
    | ------------------------------ | ------- |
    | Internet                       | TCP/IP  |
    | TCP(transfer control protocol) | 传输控制协议  |
    | UDP(user datagram protocol)    | 用户数据报协议 |
    | IP(Internet protocol)          | 网际协议    |

    ```
    ip地址找到网络上的一台主机，而端口号可以用来区分不同的服务；
           HTTP - 80
           HTTPS - 443
    端口号：
           -1 ： 可以使用ping
           22 ： 可以使用远程连接Xshell
           3389: 监控
    Linux常用防火墙服务Firewall和Iptables
    自己配防火墙 ,在阿里云APP里的安全组规则,新建一个,协议选TCP,端口设置1-65535
       
    增加端口

    firewall-cmd --add-port=80/tcp--permanent

    查看端口

    firewall-cmd --query-port=80/tcp

    将自己的项目克隆到服务器上：
           - 1、git clone http://gitee.com/jackfrued/Python1806
           - 2、将本地的项目上传（通过Xftp)
           
    TCP/IP模型
    应用层(定义应用之间如何传输数据,定义应用级协议)
      -HTTP/SMTP/POP3/FTP/SSH
      -ICQ/QQ
    传输层(端到端传输数据)- TCP/UDP
    网络层/网际层(寻址和路由)-IP/ICMP
    物理链路层(数据分帧+校验)-冗余校验码
    ```

    ### 进程管理

    1. 查询进程

       ```
       ps -ef
       标准格式查看所有进程
       ```

    2. 终止进程

       ```
       kill -9
       强制终止
       ```

    3. 将进程置于后台

       - `ctrl+Z`
       - &    如果执行命令时在命令后加上&就可以将命令置于后台运行

    4. 进程转换

       ```
       bg %编号-让暂停的进程继续在后台运行
       fg %编号-让后台进程拿到前台运行
       ```

    5. 进程监控

       ```
       按CPU占用率从高到低排列进程-top
       查询后台进程-jobs
       ```

       ### 配置服务

       1.启动服务

       ```
       systemctl start firewall
       ```

       2.终止服务

       ```
       systemctl stop firewall
       ```

       3.重启服务

       ```
       systemctl restart firewall
       ```

       4.查看服务

       ```
       systemctl status firewall
       ```

       5.设置是否开机自启动

       ```
       systemctl enable firewall-开机自启动
       systemctl disable firewall-禁止开机自启动
       ```



​                    




