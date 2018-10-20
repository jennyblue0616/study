---
author: 于梦娇
title:Redis
---

# 非关系型数据库(NoSQL数据库)

- Redis-高速缓存
- MongoDB-数据体量大价值低
- ElasticSearch-搜索引擎


MySQL/MongoDB-体量大的

Redis放的应该是体量不大的热点数据
热(点)数据-经常被访问的数据

网站优化的两大定律:
1.缓存-用空间换时间-Redis/Memcached
2.削峰-削除CPU利用的峰值,能推迟的事情都不要马上做-RabbitMQ/RocketMQ(消息队列)

修改配置文件redis.conf

1. bind(69行)绑定私网IP
2. 查找/requirepass修改密码
3. 持久化方案/appendonly

开启服务器

```
连上服务器 (使用自己配置好的配置文件来启动)
redis-server redis.conf > redis.log &
连上客户端
redis-cli -h 172.17.19.226(私有IP)
验证身份
auth 0616ymj
检查是否连上
ping
停止
1. kill 进程号
2. fg 置于前台后ctrl+c
3. 客户端>shutdown

放键值对
set yumengjiao(键) 522495731@qq.com(值)
查看存活时间
ttl(time to live) ymj
-1 永不超时     -2 没有这个值     nil 空值
再设时间
expire 键 时间
查值
get 键
删除键值对
del 键
看有没有
exists 键
查看所有键
keys *
全部删除
flushall
一共16个数据库,选择第一个数据库
select 1
删除当前数据库
flushdb
保存数据
save
bgsave(后台保存)
投票系统  增加
incr 键
减少
decr 键
退出
quit
基准测试,读写数据的次数,测试服务器的吞吐量
redis-benchmark -h IP -a 密码

value常用的5种数据类型
Sring(字符串)        应用:点赞,手机验证码
incrby 30
append 追加
不存在才给key赋值
setnx (none exist)
设置键值对时可以设置时间
setex

Hash(哈希表)         应用:保存对象,字典中的字典
放对象
hdel 删除键对应的字段

List(列表)          栈,队列
lpush 放东西(从左)
lpop 取东西
rpop(从右)
blpop list1 10有东西的时候不阻塞,没有则阻塞,等待时间10s

Set(集合)           user:1--->{'胖子','吃货'}贴标签功能
sinter-交集
sunion-并集
sdiff-差集
sismember set1-看集合里有没有这个数 
spop-取走元素
srandmember-随机拿出一个元素,没有取走
srem set1 10-删除指定的元素

SortedSet(有序集合)   排行榜

object encoding 键-可以看到内部数据类型

```



   ```
主从复制(读写分离)
master不用修改任何配置
slave 修改两条配置   
vim
/slavrof 281行
去掉注释 slaveof 主人IP 端口6379
288行 #masterauth 密码
改之前先停服务器,改好后再重启服务器
redis-cli 连自己的redis服务器
info replication  查看复制信息
主人可以写,奴隶会同步数据,但奴隶不能写,只能读

哨兵-配置文件sentinel.conf
15行 bind 内网IP地址
69行 sentinel monitor mymaster 主人IP 主人端口 1(投票)
98行 认定下线时间down-after-milliseconds mymaster 10000
在认定时间内主人回来就还是主人
131行 故障恢复时间
启动哨兵的服务器
redis-server sentinel.conf --sentinel
   ```







