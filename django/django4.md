---
author: 于梦娇
title: django4
---

# django4

## 多对多关联关系

1. 首先在models.py文件中新建一个课程模型,通过ManyToManyField()建立关联关系,自动生成course_stu中间表,其中有三个字段:id,course_id,student_id

```python
class Course(models.Model):
    c_name = models.CharField(max_length=10)
    #多对多关联字段
    stu = models.ManyToManyField(Student)

    class Meta:
        db_table = 'course'
```

2. 在urls.py文件中`url(r'^add_course/', views.add_course),`

   `url(r'^add_stu_course/', views.add_stu_course),`

3. 在views.py文件中

```python
from django.http import HttpResponse, HttpResponseRedirect
def add_course(request):
	#添加课程
    list1 = ['数学课', '英语课', '体育课', '美术课', '计算机课']
    for i in list1:
       Course.objects.create(c_name=i)
    return HttpResponse('添加成功')
        
def add_stu_course(request):
	#添加学生选课数据
    if request.method == 'GET':
        cou = Course.objects.all()
        return render(request, 'course.html', {'cou':cou})
    if request.method == 'POST':
        #获取课程id,学生id
        c_id = request.POST.get('cous_id')
        s_id = request.GET.get('stu_id')
        stu = Student.objects.get(pk=s_id)
        #一对多 设置学生和课程的关联关系
        course = Course.objects.get(pk=c_id)
        #stu.course_set拿到关联关系
        stu.course_set.add(course)
        # course.stu.add(stu)
        # add == >> remove
        # return HttpResponse('选课成功')
        return HttpResponseRedirect('/all_stu/')
```

注:(1)如果要给中间表添加字段,就自己定义中间表,自己建立跟学生表,课程表的外键

​     (2)跳转-HttpResponseRedirect() 响应码是:302

4. 在course.html文件中

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <form action="" method="post">
        <select name="cous_id">
            {% for co in cou %}
            <option value="{{ co.id }}">{{ co.c_name }}</option>
            {% endfor %}
        </select>
        <input type="submit" value="提交"/>
    </form>
</body>
</html>
```

注:select定义name就是option里的value值

## 模板

1. 父模板,block标签

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>
        {% block title %}
        {% endblock %}
    </title>
    {% block css %}
    {% endblock %}
    {% block js %}
    {% endblock %}
</head>
<body>
    {% block content %}
    {% endblock %}
</body>
</html>
```

父模板中只有一个大体的框架结构,`{% block %}`标签可以想象成占位符,子模板可以通过继承来把占位的`{% block %}`替换成具体的内容



2. 子模板`base_main.html`,通过`{% extends 'base.html' %}`继承父模板`base.html`

```html
{% extends 'base.html' %}
#继承后重写{% block js %}
{% block js %}
        <script src="https://code.jquery.com/jquery-3.1.1.min.js"></script>
{% endblock %}
```

`base_main.html`可以看成是一个存放初始值的页面,继承`base.html`,重写了`{% block %}`



3. 子模板继承`base_main.html`

  首先,为了能够更加清楚地看到不同应用对应的url路由地址,我们可以在app文件夹中新建一个名为`urls.py`的文件,格式与day04文件夹下的`urls.py`一致,区别在于day04文件夹下的`urls.py`中要做如下操作

```python
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # 127.0.0.1:8080/app/xxx
    url(r'^app/', include('app.urls'))
]
```

这样,把专属于app的url就可以存放在这个文件中,更加清晰,访问时形如`127.0.0.1:8080/app/xxx`即可

```python
from django.conf.urls import url

from app import views

urlpatterns = [
    #127.0.0.1:8080/app/index/
    url(r'^index/', views.index),
    url(r'^all_stu/', views.all_stu),
]
```

  然后,在views.py文件中

```python
from django.shortcuts import render

from app.models import Student


def index(request):
    if request.method == 'GET':
        return  render(request, 'index.html')

    
def all_stu(request):
    if request.method == 'GET':
        stus = Student.objects.all()
        content_h2 = '<h2>开心</h2>'
        return render(request, 'stus.html', {'stus':stus, 'content':content_h2})
```

  子模板`index.html`,通过`{% extends 'base_main.html' %}`继承父模板

```python

{% extends 'base_main.html' %}

{% block title %}
    我是首页
{% endblock %}

{% block css %}
    <!--加载静态文件css的两种方式-->
    <!--<link href="/static/css/index.css" rel="stylesheet">-->
    {% load static %}
    <link href="{% static 'css/index.css' %}" rel="stylesheet">
{% endblock %}


{% block content %}
    <p>千峰</p>
{% endblock %}

{% block js %}
    <!--引入父模板的block js中定义的内容-->
    <!--第一种:单行注解-->
    {# 注解1 #}
    {# 注解2 #}
    {# 注解3 #}
    <!--第二种:多行注解-->
    {% comment %}
        开心
    {% endcomment %}

    {{ block.super }}
{% endblock %}

```

  注: (1)`{% block js %}`

​         `{{ block.super }}`

​         `{% endblock %}`

​          因为在父模板`base_main.html`中有jquery了,在子类中还需要运用,就不用重写了,     用`{{ block.super }}`就可以引入在父模板中定义的jquery内容

​       (2)注意,注解不要直接ctrl+/,这是html中的注解,并不能起到注解的作用,应该用`{# #}`充当注解.

​       (3)引入css/js,用两种方式,static是与app同级的文件夹,主要用来加载一些模板中用到的资源,主要配置css,html,图片,文字等.

​            a. 绝对路径`<link href='/static/xxx.css' rel='stylesheet'/>`

​            b.静态配置文件      `STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]`

​              加载静态配置文件

​               `{% load static %}`

​               `<link href='{% static 'xxx.css' %}' rel='stylesheet'/>`

​               同时要在settings.py文件中指定静态目录static的地址,这样就不用写绝对全路径了

​         

子模板`stus.html`,通过`{% extends 'base_main.html' %}`继承父模板

```html
{% extends 'base_main.html' %}

{% block content %}
<table>
  <thead>
  	<th>序号</th>
    <th>id</th>
    <th>姓名</th>
    <th>创建时间</th>
  </thead>
  <tbody>
  	{% for stu in stus %}
    <tr>
      <td> {{ forloop.count }}  </td>
      <td> {{ stu.id }} </td>
      <td> 
      	{% ifequal forloop.counter 1 %}
        <em style="color:red;" > {{ stu.s_name }} </em>
        {% else %}
        	{{ stu.s_name }}
        {% endifequal %}
      </td>
      <td> {{ stu.s_age | add:1}} </td>
      <td> {{ stu.create_time | date:'Y年m月d日 H:m:s'  }} </td>
    </tr>
  	{% endfor %}
  
  </tbody>
  
  
 </table>
{{ content | safe }}
{% endblock %}
```

​	注:(1) 重写了`{block content}`

​             (2)`forloop.counter`从1开始

​                 `forloop.counter0`从0开始

​                 `forloop.revcounter`倒着开始,到1结束

​                 `forloop.revcounter0`倒着开始,到0结束

​            (3)`{% if forloop.counter == 1 %}`与`{% ifequal forloop.counter 1 %}`是等价的

​            (4)过滤器`{{ stu.s_age | add:1}}`是取到学生的年龄再加上1岁

​                            `{{ content | safe }}`



## 总结

1. 标签

>语法  {%  tag  %}
>
>作用  a.加载外部传入的变量
>
>​         b.输出中创建文本
>
>​         c.控制循环或逻辑
>
> 应用    for/if/ifequal/extends/block/comment
>
>{%for k in stus%}
>{% endfor %}
>
>{% if xxx == 1 %}
>{% endif %}

2. 过滤器

>定义  {{ var| 过滤器 }}
>
>应用
>
>{{  stu.s_age | add:5 }}---学生年龄加5岁
>
>{{ content | safe }} 将接收到的数据当成普通字符串处理还是渲染成html







