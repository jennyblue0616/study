---
author: 于梦娇
title: django2
---

## 创建应用

  在terminal中输入`python manage.py startapp app`创建一个名为app的应用,在app文件夹中会有6个文件,其中models.py文件是模型层,views.py是写业务逻辑的文件

## 简单的显示hello

1. 首先,在urls.py文件中

```
from app import views

urlpatterns = [
  url(r'^hello/', views.hello),
]
#意为在访问127.0.0.1:8080/hello/时,会调用views.hello方法
```

2. 然后,在views.py文件中,定义hello方法

```
from django.http import HttpResponse

def hello(request):
	return HttpResponse('你好!')
```

3. 访问127.0.0.1:8080/hello/ ,就可以看到 '你好'



## 使用ORM创建表

  ORM(object-relational-mapping)对象关系映射,里面有很多方法,让我们不用写SQL语句,就可以对数据库进行访问查询等操作,例如:all()----映射到数据库,转化成SQL语句就是select * from 表.

1. 在models.py文件中,声明一个Student模型

```
class Student(models.Model):
	#定义s_name字段,最长不超过6字符,varchar类型,唯一
	s_name = models.CharField(max_length=6, unique=True)
	#定义s_age字段,int类型
    s_age = models.IntegerField(default=18)
    #定义s_gender字段,int类型
    s_gender = models.BooleanField(default=1)
    #定义create_time字段,创建时间
    create_time = models.DateTimeField(auto_now_add=True, null=True)
    #定义operate_time字段,修改时间
    operate_time = models.DateTimeField(auto_now=True, null=True)
    class Meta:
    	#定义模型迁移到数据库中的表名
    	db_table = 'student'
```

2. 在terminal命令行中输入`python manage.py makemigrations`会出现错误No changes detected,此时需要到settings.py文件中修改配置,INSTALLED_APPS = ['app',],添加app

   ```
   INSTALLED_APPS = [
       'django.contrib.admin',
       'django.contrib.auth',
       'django.contrib.contenttypes',
       'django.contrib.sessions',
       'django.contrib.messages',
       'django.contrib.staticfiles',
       'app',
   ]
   ```

   ​

3. 在terminal命令行中输入`python manage.py makemigrations `生成迁移文件,migrations文件夹下回生成0001_initial.py文件

4. 在terminal里输入 `python manage.py migrate`迁移到数据库,数据库里就会生成student的表.

5. 打开数据库,就可以看到生成的student表,而django_migrations表是保存迁移的记录

## 给表添加数据

1. 在urls.py里添加一个`url(r'create_stu/', views.create_stu),`
2. 然后在views.py表中定义create_stu方法

```
def create_stu(request):
	方式一
	创建学生
	stu = Student()
	stu.s_name = '小鱼'
	stu.s_age = 20
	#保存到数据库中
	#再执行一次会报错'Duplicate',因为s_name具有唯一性约束
	stu.save() 
	方式二
	Student.objects.create(s_name='大咖')
	return HttpResponse('创建成功')
```

3. 打开浏览器,访问127.0.0.1:8080/create_stu/就能在数据库中新增数据

## 使用Debug:

- 如果关闭了服务器,浏览器还是正常显示,就换端口.debug可以用来调试程序,左边的红点放到哪行,程序就执行到哪行.



## 查询表中的数据

```
def sel_stu(request):
    # 实现查询
    # all()查询所有对象信息
    stus = Student.objects.all()
    
    # filter()过滤
    stus = Student.objects.filter(s_name='小王')
    # first()获取第一个对象
    # last()获取最后一个对象
    stus = Student.objects.filter(s_age=20).first()
    
    # get方法与上面效果相同，容易出错
    stus = Student.objects.get(s_age=20)
    Student.objects.filter同get相同,都拿到的是学生对象,
    区别:get拿不到值会报错,返回多个也会报错.filter返回是空,不会报错
    
    # 模糊查询 like
    # 包含
    stus = Student.objects.filter(s_name__contains='锤')
    stu_names = [stu.s_name for stu in stus]
    print(stu_names)

    # 以开头
    stus = Student.objects.filter(s_name__startswith='小')
    stu_names = [stu.s_name for stu in stus]
    print(stu_names)

    # 以结尾
    stus = Student.objects.filter(s_name__endswith='锤')
    stu_names = [stu.s_name for stu in stus]
    print(stu_names)

    # 大于/大于等于 gt/gte 小于小于等于 lt/lte
    stus = Student.objects.filter(s_age__gt=18)
    stus = Student.objects.filter(s_age__gte=18)
    stu_names = [stu.s_name for stu in stus]
    print(stu_names)

    # 排序 order_by()
    # 升序
    stus = Student.objects.order_by('id')
    # 降序
    stus = Student.objects.order_by('-id')

    # 查询不满足条件的数据 exclude()
    stus = Student.objects.exclude(s_age=20).order_by('id')

    # 计算统计的个数：count()\len()
    print(len(stus))
    stus_count = stus.count()
    print(stus_count)

    # values()
    stus_values = stus.values()
    print(stus_values)
    
    # id = pk(primary key)
    stus = Student.objects.filter(id=3)
    stus = Student.objects.filter(pk=3)

    stu_names = [stu.s_name for stu in stus]
    print(stu_names)
    return HttpResponse('查询成功')

```

