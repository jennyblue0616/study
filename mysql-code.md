---
author:于梦娇
title: mysql-code
---

## 员工管理数据库

-- 创建人力资源管理系统数据库
drop database if exists HRS;
create database HRS default charset utf8 collate utf8_bin;

-- 切换数据库上下文环境
use HRS;

-- 删除表
drop table if exists TbEmp;
drop table if exists TbDept;

-- 创建部门表
create table TbDept
(
dno tinyint not null comment '部门编号',
dname varchar(10) not null comment '部门名称',
dloc varchar(20) not null comment '部门所在地',
primary key (dno)
);

-- 添加部门记录
insert into TbDept values 
(10, '会计部', '北京'),
(20, '研发部', '成都'),
(30, '销售部', '重庆'),
(40, '运维部', '深圳');

-- 创建员工表
create table TbEmp
(
eno int not null comment '员工编号',
ename varchar(20) not null comment '员工姓名',
job varchar(20) not null comment '员工职位',
mgr int comment '主管编号',
sal int not null comment '月薪',
comm int comment '月补贴',
dno tinyint comment '所在部门编号',
primary key (eno)
);

-- 添加外键约束
alter table TbEmp add constraint fk_dno foreign key (dno) references TbDept(dno) on delete set null on update cascade;

-- on delete set null 删除部门,部门编号会赋值null  cascade级联更新,职员表中的部门编号跟着变化

-- 添加员工记录
insert into TbEmp values 
(7800, '张三丰', '总裁', null, 9000, 1200, 20),
(2056, '乔峰', '分析师', 7800, 5000, 1500, 20),
(3088, '李莫愁', '设计师', 2056, 3500, 800, 20),
(3211, '张无忌', '程序员', 2056, 3200, null, 20),
(3233, '丘处机', '程序员', 2056, 3400, null, 20),
(3251, '张翠山', '程序员', 2056, 4000, null, 20),
(5566, '宋远桥', '会计师', 7800, 4000, 1000, 10),
(5234, '郭靖', '出纳', 5566, 2000, null, 10),
(3344, '黄蓉', '销售主管', 7800, 3000, 800, 30),
(1359, '胡一刀', '销售员', 3344, 1800, 200, 30),
(4466, '苗人凤', '销售员', 3344, 2500, null, 30),
(3244, '欧阳锋', '程序员', 3088, 3200, null, 20),
(3577, '杨过', '会计', 5566, 2200, null, 10),
(3588, '朱九真', '会计', 5566, 2500, null, 10);

-- 查询薪资最高的员工姓名和工资 max,子查询
select ename,sal from tbemp where sal=(select max(sal) from tbemp);

-- 查询员工的姓名和年薪((月薪+补贴)*12)
select ename,(sal+if(comm,comm,0))*12 as 年薪 from tbemp;
-- t
select ename,(sal+ifnull(comm,0))*12 as 年薪 from tbemp where (sal+ifnull(comm,0))*12>50000;

-- 查询有员工的部门的编号和人数
select dno,count(dno) from tbemp group by dno having count(dno)>0;

-- 查询所有部门的名称和人数
select dname,num from tbdept t1,
(select dno,count(dno) as num from tbemp group by dno)t2 
where t1.dno=t2.dno;
-- t 左外连接
select dname,ifnull(num,0)
from tbdept t1 left join
(select dno,count(dno) as num from tbemp group by dno)t2 
on t1.dno=t2.dno;

-- 查询薪资最高的员工(Boss除外)的姓名和工资
select ename,sal+if(comm,comm,0) as salary from tbemp order by salary desc limit 1,1;
-- t
select ename,sal from tbemp where sal=
(select max(sal) from tbemp where mgr is not null);

-- 查询薪水超过平均薪水的员工的姓名和工资 子查询
select ename as 姓名,sal+if(comm,comm,0) as 工资 from tbemp where sal+if(comm,comm,0)>(select avg(sal+if(comm,comm,0)) from tbemp);

select ename,sal from tbemp where sal>(select avg(sal) from tbemp);

-- 查询薪水超过其所在部门平均薪水的员工的姓名、部门编号和工资
select ename,t1.dno,sal,salary from tbemp t1,
(select dno,avg(sal) as salary from tbemp group by dno)t2
where t1.dno=t2.dno and t1.sal>salary;

-- 查询薪水超过其所在部门平均薪水的员工的姓名、部门名称和工资
select ename,dname,sal from tbemp,tbdept,

(select dno,avg(sal) as salary from tbemp group by dno)t2
where t2.dno=tbemp.dno and t2.dno=tbdept.dno and tbemp.sal>t2.salary;



-- t
select ename,dname,sal,salary from tbemp t1 inner join
(select dno,avg(sal) as salary from tbemp group by dno)t2
on t1.dno=t2.dno and t1.sal>salary inner join tbdept t3 on t3.dno=t2.dno;

-- 查询部门中薪水最高的人姓名、工资和所在部门名称

select ename,sal,dname from tbemp,tbdept,
(select dno as dno2,max(sal) as salary from tbemp group by dno2)t1 
where t1.dno2=tbemp.dno and t1.salary=tbemp.sal and t1.dno2=tbdept.dno;


-- 查询主管的姓名和职位
select ename from tbemp where eno in
(select mgr from tbemp group by mgr);

select ename,job from tbemp where eno in
(select distinct mgr from tbemp where mgr is not null);

-- 说明:去重(distinct)操作和集合运算(in/not in)效率是非常低下的
-- 通常建议用exists 或 not exists来替代去重和集合

select 1 from tbemp;

-- x可以任意替换成别的字符
select ename,job from tbemp t1
where exists(select 'x' from tbemp t2 where t1.eno=t2.mgr);


-- 视图是查询的快照
create view vw_emp_sal_gt_avg as 
select ename,dname,sal from tbemp t1 inner join
(select dno,avg(sal) as salary from tbemp group by dno)t2
on t1.dno=t2.dno and t1.sal>salary inner join tbdept t3 on t3.dno=t2.dno;


select * from vw_emp_sal_gt_avg;

-- 索引(相当于一本书的目录)
-- 为表创建索引可以加速查询(用空间换时间)
-- 索引虽然很好,但是不能滥用,一方面占用额外空间
-- 因为索引会让增删改变得更慢,因为增删改操作调整了数据,所以可能会导致更新索引
-- 如果哪个列经常被用于查询的筛选条件,那么这个列就要建索引
-- 主键上右默认的索引(唯一索引)

-- 创建索引
-- 说明:如果使用模糊查询,如果查询条件不以%开头,那么索引有效,如果查询条件以%开头,那么索引失效
create index idx_emp_ename on tbemp(ename);
create unique index uni_emp_ename on tbemp(ename);
-- 删除索引
alter table tbemp drop index uni_emp_ename;







