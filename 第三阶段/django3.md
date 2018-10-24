---
author: 于梦娇
title: django3
---

# django3



## 删除

删除,首先选出要删除的记录,然后运用模型名.objects.filter(条件).delete()即可删除

```python
def del_stu(request):
    #实现删除
    Student.objects.filter(s_name='香芋').delete()
    return HttpResponse('删除成功')
```

## 更新

更新,首先选出要更新的记录,运用模型名.objects.filter(条件).update(字段1=xxx, 字段2=xxx)

```python
def update_stu(request):
    #实现更新
    #第一种方法
    # stu = Student.objects.filter(s_name='力哥').first()
    # #Student.objects.get(s_name='力哥')
    # stu.s_name = '小宝贝'
    # stu.save()
    #第二种方法
    Student.objects.filter(s_name='小宝贝').update(s_name='小傻瓜')
    return HttpResponse('更新成功')
```

## 查询

```python
from django.db.models import Q, F
#Q(),F()可以使用alt+enter快捷键
    #或  查询年龄20或是女生的学生信息
    stus = Student.objects.filter(Q(s_age=20) | Q(s_gender=0))
    #且  查询年龄20并且是女生的学生信息
    stus = Student.objects.filter(Q(s_age=20) & Q(s_gender=0))
    # 非条件~  查询年龄不是20的学生信息
    stus = Student.objects.filter(~Q(s_age=20))
    #查询语文比数学成绩加10分还高的学生信息
    #F()
    stus = Student.objects.filter(yuwen__gt=F('shuxue') + 10)
```

## 一对一关联关系

1. 在models.py文件中定义一个模型,保存学生的电话和地址

```python
class StudentInfo(models.Model):
    phone = models.CharField(max_length=11, null=True)
    address = models.CharField(max_length=100)
    
    #OneToOneField指定一对一的关联关系,该字段定义在任何一个模型都可以
    stu = models.OneToOneField(Student)

    class Meta:
        db_table = 'student_info'
```

2. 然后在settings.py文件中,修改DIRS的参数,指定templates的路径,新建一个与day02同级的文件夹templates,里面存放的是html页面

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],   
    }
]
```

3. urls.py文件中新建一个url`url(r'^all_stu/', views.all_stu),`
4. views.py文件中新建一个方法

```python
def all_stu(request):
    #获取学生信息
    stus = Student.objects.all()
    #返回页面
    #render渲染, 参数: 请求,页面,数据
    return render(request, 'stus.html', {'students':stus})
    #字典的key可以随意命名,value是stus,如果向页面传参就写第三个参数,否则可不写
```

5. 在templates文件夹中新建一个stus.html文件

```python
p<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<table>
    <thead>
        <th>姓名</th>
        <th>年龄</th>
        <th>操作</th>

    </thead>
    <tbody>
        {% for stu in students %}
            <tr>
                <td>{{ stu.s_name }}</td>
                <td>{{ stu.s_age }}</td>
                <td>
                    <a href="/add_info/?stu_id={{ stu.id }}">添加扩展信息</a>
                </td>
            </tr>
        {% endfor %}
    </tbody>
</table>
</body>
</html>
```

注意:a标签中的href属性`/add_info/`前不能忘记`/`

## 获取页面数据,一对一关联关系

1. models.py文件中,新建一个类,OneToOneField指定一对一的关联关系,该字段定义在任何一个模型都可以

```python
#一对一(相当于一对多,多的那个唯一约束)
class StudentInfo(models.Model):
    phone = models.CharField(max_length=11, null=True)
    address = models.CharField(max_length=100)
    #OneToOneField指定一对一的关联关系,该字段定义在任何一个模型都可以
    stu = models.OneToOneField(Student)

    class Meta:
        db_table = 'student_info'
```



2. urls.py文件中设置`url(r'^add_info/', views.add_info)`
3. views.py文件中写方法

```python
def add_info(request):
  #页面默认是GET,访问就是GET
  if request.method == 'GET':
     return render(request, 'info.html')
  if request.method == 'POST':
     #获取页面中提交的手机号和地址
     #request.POST 返回的是<QueryDict: {'phone': ['113'], 'address': ['33']}>
     phone = request.POST.get('phone')
     adress = request.POST.get('address')
     stu_id = request.GET.get('stu_id')
     #保存数据
     StudentInfo.objects.create(phone=phone, 
                                adress=adress,
                                stu_id=stu_id)
     return HttpResponse('创建拓展表信息成功')
```



4. info.html文件

```python
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <form action="" method="post">
        电话号码: <input type="text" name="phone">
        地址:<input type="text" name="address">
        <input type="submit" value="提交">
    </form>
</body>
</html>
```



5. 已知学生查询拓展的信息

```python
def sel_info_by_stu(request):
    if request.method == 'GET':
        # 通过学生查询拓展表信息
        stu = Student.objects.get(s_name='小雨')
        #第一种方法
        info = StudentInfo.objects.filter(stu_id=stu.id)
        info = StudentInfo.objects.filter(stu=stu)
        #第一个stu是StudentInfo模型中的stu = models.OneToOneField(Student)
        
        #第二种方法  学生对象.关联的模型名小写
        info = stu.studentinfo
        
        return HttpResponse('通过学生查找拓展表信息')
```

6. 已知学生拓展信息找学生

```python
def sel_stu_by_info(request):
    if request.method == 'GET':
        info = StudentInfo.objects.get(phone='110')
        student = info.stu
        #info.stu相当于学生对象,可以通过info.stu获取student表中的所有信息
        print(student)
        return HttpResponse('通过手机号找学生信息')

#info.stu  <Student: Student object>
#info   <StudentInfo: StudentInfo object>
```

## 一对多关联关系

1. models.py文件

```python
class Grade(models.Model):
    g_name = models.CharField(max_length=10, unique=True)

    class Meta:
        db_table = 'grade'
       
class Student(models.Model):
    grade = models.ForeignKey(Grade, null=True)
    
```



2. urls.py文件

```python
url(r'^add_grade', views.add_grade),
url(r'sel_stu_grade/', views.sel_stu_grade),
```

3. views.py文件

​       students = grade.student_set()

```python
def add_grade(request):
    if request.method == 'GET':

        Grade.objects.create(g_name='1班')
        Grade.objects.create(g_name='2班')
        Grade.objects.create(g_name='3班')
        Grade.objects.create(g_name='4班')
        
        return HttpResponse('添加班级成功')
        
def sel_stu_grade(request):
    if request.method == 'GET':
        # 1.通过学生查找班级
        stu = Student.objects.filter(s_name='小雨').first()
        grade = stu.grade
        # 2.通过班级查找学生
        grade = Grade.objects.get(g_name='4班')
        students = grade.student_set.filter(s_gender=0).all()
        return HttpResponse('查询学生和班级信息')

```





## 总结关联关系



>关联关系
>1) 一对一:OneToOneField
>   class A:
>
>```
>   id = xxx
>   b = OneToOneField(B)
>```
>
>   class B:
>
>```
>   id = xxx
>```
>
>   已知a对象,查找b对象:a.b
>   已知b对象,查找a对象:b.a
>
>2) 一对多:ForeignKey
>
>  class A:
>
>```
>   id = xxx
>   b = ForeignKey(B)
>```
>
>  class B:
>
>```
>   id = xxx
>```
>
>  已知a对象,查找b对象:a.b
>  已知b对象,查找a对象:b.a_set



## GET和POST区别

1. GET比POST更不安全，因为参数直接暴露在URL上，所以不能用来传递敏感信息。
2. GET参数通过URL传递，POST放在Request body中。
3. GET请求在URL中传送的参数是有长度限制的，而POST没有。
4. GET在浏览器回退时是无害的，而POST会再次提交请求。
5. GET产生的URL地址可以被Bookmark，而POST不可以。
6. GET请求会被浏览器主动cache，而POST不会，除非手动设置。
7. GET请求只能进行url编码，而POST支持多种编码方式。
8. GET请求参数会被完整保留在浏览器历史记录里，而POST中的参数不会被保留。
9. 对参数的数据类型，GET只接受ASCII字符，而POST没有限制。

  本质上,GET和POST都是TCP链接,但是由于浏览器(发起HTTP请求)和服务器(接收HTTP请求)的不同,导致两者在应用过程中体现一些不同之处

  另外,GET产生一个TCP数据包；POST产生两个TCP数据包。

  对于GET方式的请求，浏览器会把http header和data一并发送出去，服务器响应200（返回数据）；

  而对于POST，浏览器先发送header，服务器响应100 continue，浏览器再发送data，服务器响应200 ok（返回数据）。

因为POST需要两步，时间上消耗的要多一点，看起来GET比POST更有效。因此Yahoo团队有推荐用GET替换POST来优化网站性能。但这是一个坑！跳入需谨慎。为什么？

1. GET与POST都有自己的语义，不能随便混用。
2. 据研究，在网络环境好的情况下，发一次包的时间和发两次包的时间差别基本可以无视。而在网络环境差的情况下，两次包的TCP在验证数据包完整性上，有非常大的优点。
3. 并不是所有浏览器都会在POST中发送两次包，Firefox就只发送一次。