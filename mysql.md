---
title: 数据库
author: 于梦娇
---

# 关系型数据库

## 关系型数据概述

1.数据持久化

- 文件操作(读写文件)-Excel/文本文件
- 数据库
- 云存储

2.关系型数据库特点

- 理论基础:集合论和关系代数
- 具体表象:用二维表(行和列)组织数据
- 编程语言:结构化查询语言(SQL)

3.关系型数据库产品

- Oracle
- DB2
- SQL Server
- MySQL
- SQLite

## MySQL简介

图形化的`MySQL`客户端工具

-`Navicat for MySQL`



-`Toad for MySQL`



-`SQLyog`



1.安装和配置

>安装时选最后一项custom自定义安装
>展开MySQL Server,选64位的,右边必选第一个,最后一个
>下一步会提示缺东西,选上后点execute
>安装好后准备配置
>选第一个Standalone单机版
>下一步选开发机选项Development Machine
>端口是IP地址的拓展
>services.msc  windows的服务窗口
>下一步设置超级管理员密码
>下一步第一个选项勾选-把mysql安装成windows的一项服务
>第二个是开机自启不选
>下一步什么都不要
>点execute
>
>启动可以在服务里启动,也可以在cmd敲 net start mysql
>
>然后输密码
>
>show databases 查看数据库
>use mysql进入到mysql数据库
>show tables 查看表格



2.常用命令

当我们做数据持久化操作时不仅希望能够把数据长久的保存起来,更重要的是希望方便管理数据,需要时方便地把数据取出来
具体表象:用二维表来组织数据
行:记录-实体
列:字段-实体属性

`SQL分为DDL:creat/drop/alter`

`DML:insert/delete/update/select`

`DCL:grant/revoke`

### 关于数据库的命令有

```
#创建数据库
create database 数据库名 default charset utf8;

#删除数据库
#如果存在school的数据库就删除
drop database if exits school;

#切换数据库
use school

```

### 关于表的命令有

```
#创建表
#记得创建一个能唯一确定数据的主键
create table tb_student
(
stuid int not null,
stuname varchar(4) not null,
gender bit default 1,
birth date,
primary key (stuid)
);

#删除表
drop table if exists tb_student;
#删除全表
truncate table tb_student

#修改表
#column可以省略
alter table tb_student add column tel char(11) not null;
alter table tb_student drop column birth;

外键约束,保证了引用完整性,必须保证类型一样
#创建外键约束
alter table tb_student add constraint fk_student_id foreign key (id) references tb_colloge(id);
#删除外键约束
alter table tb_student drop foreign key fk_student_id;

#添加唯一约束
alter table tb_college add constraint uni_college_collname unique (collname);

注意:在关系型数据库中,如果遇到多对多关系时,光靠两张表是无法建立多对多关系的,这时需要另外一张表,充当他们之间的一个中转站
```

### 关于数据的命令

```
#插入数据
insert into tb_student values 
(001, '小明', 1, '13983206512'),
(002, '小王', 1, '13784256512'),
(003, '小红', 0, '13593206512');

#删除数据
delete from tb_student where stuid in (001,002);

#更新数据
update tb_student set addr='兰州' where stuid=003;

#查询数据
select * from tb_student;

#投影 查指定的列
select stuname, gender from tb_student;

#别名(alias - as可省略)
select stuname as 姓名 from tb_student;
#当性别是1时是男,否则是女
select stuname 姓名, case gender when 1 then '男' else '女' end as 性别 from tb_student;

#对列做运算
#concat()合并成一列
select concat(stuname, ':', tel) as 信息 from tb_student;
```

### 数据的完整性

- 实体完整性:

  每一条记录都是独一无二的,没有冗余.

  主键/唯一索引(唯一约束)

- 参照完整性:

  B表参照了A表,A表中没有的数据在B表中绝不能出现 

  外键

- 域完整性:

  录入的数据都是有效的

  数据类型/非空约束/默认值约束/检查约束 (MySQL中不生效)




### 数据的一致性

- A:Atomicity原子性-不可分割
- C:Consistency一致性-事务前后数据状态一致
- I:Isolation隔离性-多个事务不能看到彼此的中间状态
- D:Duration持久性-事务完成后数据要持久化



在出现并发事务访问数据的时候,数据库底层有锁机制来保护数据,但是通常写SQL的时候不用显示书写锁操作,数据库会根据我们设定的事务隔离级别自动的数据加锁

并发(多个线程)数据访问可能出现5种问题:
1.第一类丢失更新
2.第二类丢失更新(别人的更新丢失了)
3.脏读(没提交就看到了修改结果,读脏数据)-一个事务读取了另一个事务尚未提交的数据
-------------以下两项对统计结算问题有影响
4.不可重复读-一个事务在读取查询结果时发现其他事务更新了数据导致无法读取
5.幻读-一个事务在执行查询时发现被其他事务提交了新的数据

```
Read Uncommited-脏读

Read Commied-避免脏读

Repeatable Read-避免不可重复读

Serializable(串行化)-避免幻读

级别,性能由高到低

安全从低到高

改级别set session transaction isolaion level read committed;

查级别 select @@tx_isolation;

```




### 筛选

```
select * from tb_student where stuid=1001;
select * from tb_student where stuid in (1001, 1003, 1005);
select * from tb_student where stuid not in (1001, 1003, 1005);
select stuid, stuname, gender from tb_student where stuid between 1003 and 1007;
select * from tb_student where stuid>1003 and gender=0;
select * from tb_student where stuid>1003 or gender=0;

# 注意:判断一个字段是否是null,不能用=和<>
select * from tb_student where addr is null;
select * from tb_student where addr is not null;
#判断是否是空字符串,用=''

# 模糊(char / varchar)
# % 是一个通配符,表示0个或任意多个字符
select * from tb_student where stuname like '小%';
# _是一个通配符,表示1个字符
select * from tb_student where stuname like '小_';
# 名字里有小这个字的查询
select * from tb_student where stuname like '%小%';

# 排序
select * from tb_student order by gender asc, stuid desc;

# 分页
# 跳过2条取3条
select * from tb_student limit 3 offset 2;
select * from tb_student limit 2, 3;

#去重
select distinct seldate from tb_score;

#聚合函数
max()/min()/avg()/count()/sum()
select avg(mark) as 平均分 from tb_score where cid=1111;

#分组
select if(gender,'男','女') as 性别,count(gender) as 总人数 from tb_student group by gender;
count和group by通常会一起使用

# where-分组前的筛选
# having-分组后的筛选
select sid,avg(mark) from tb_score group by sid having avg(mark)>=90;

#子查询:在一个查询中又用到了另外一个查询结果

#双表查询/集合
select sname from tb_student where stuid in(select sid from tb_score group by sid having count(sid)>2);

连接查询
三表查询
select sname,cname,mark from tb_score,tb_student,tb_sourse where stuid=sid and couid=cid and mark is not null;
第二种写法
select sname,cname,mark from tb_student inner join tb_score on stuid=sid 
inner join tb_course on couid=cid
where mark is not null;

左外连接 把写在前面的表不满足连表条件的记录也显示出来,对应记录补上空值
右外连接 把写在后面的表不满足连接条件的记录也查出来对应记录补空值
左外连接和子查询(查询每个学生的姓名和选课数量)
select sname,total from tb_student left join
(select sid,count(sid) as total from tb_score group by sid)t2
on stuid=sid;
左外连接是能查出左边的表所有的记录,即使该记录不在右边的表.
查询所有部门的名称和人数(包括部门人数为0的部门)
ifnull(num,0)-有值是num,没有是0

select dname,ifnull(num,0)
from tbdept t1 left join
(select dno,count(dno) as num from tbemp group by dno)t2 
on t1.dno=t2.dno;
```



### 数据控制语言(DCL)

```
-- @'localhost'限定本机
-- 创建名为abc的用户并设置口令
create user'abc'@'%'identified by '123123';

-- 授权
grant select on srs.* to 'abc'@'%';
grant insert,delete,update on 
srs.* to 'abc'@'%';
grant create,drop,alter on srs.* to 'abc'@'%';
-- 数据库srs的全部权利给abc
grant all privileges on srs.* to 'abc'@'%';
-- abc可以授权给别人
grant all privileges on srs.* to 'abc'@'%' with grant option;

-- 召回
revoke all privileges on srs.* from 'abc'@'%'; 
-- 多个增删改查的操作,要么都成功,要么都不做,需要用到事务控制,例如:转账
```

### 视图和索引

​    	视图是查询的快照,视图可以限制访问权限在列上面
通过视图可以将用户对表的访问权限进一步加以限制,也就是说将来普通用户不能够直接查询表的数据,只能通过指定的视图去查看到允许他访问的内容

​	索引(相当于一本书的目录)
为表创建索引可以加速查询(用空间换时间),索引虽然很好,但是不能滥用,一方面占用额外空间
因为索引会让增删改变得更慢,因为增删改操作调整了数据,所以可能会导致更新索引
如果哪个列经常被用于查询的筛选条件,那么这个列就要建索引





### python中使用MySQL



安装依赖库有三种方式

1. file/setting
2. 先写代码 import pymysql

   双击点红灯泡,里面有安装包

3. 下方terminal 进入,然后输入pip install -i https://pypi.doubanio.com/simple pymysql

>用豆瓣的镜像下载会很快
>一劳永逸 在用户主目录下新建一个名为pip的文件夹,里面新建一个文件pip.ini,里面写[global]
>index-url=https://pypi.doubanio.com/simple



```
import pymysql

class Dept():

    def __init__(self, no, name, loc):
        self.no = no
        self.name = name
        self.loc = loc


def main():

    #1.创建数据库连接
    conn = pymysql.connect(host="localhost",port=3306,
                           user="root",password="123456",
                           db="hrs", charset="utf8",autocommit=True,cursorclass=pymysql.cursors.DictCursor)

    try:
        #2.通过连接,拿到游标的对象,上下文语法,离开with代码,游标自动关闭
        with conn.cursor() as cursor:
            #3.向数据库服务器发出SQL
            cursor.execute(
                '''select dno as no, dname as name, 
                dloc as loc from tbdept'''
                )
            print(cursor.fetchone())
            print(cursor.fetchmany(2))

            for row in cursor.fetchall():
                print(row['no'], end='\t')
                print(row['name'], end='\t')
                print(row['loc'])
                # dept = Dept(**row)
                # print(dept.no, end='\t')
                # print(dept.name, end='\t')
                # print(dept.loc)

    finally:
        conn.close()

if __name__ == '__main__':
    main()
```

