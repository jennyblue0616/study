---
author : 于梦娇
title : django7
---

# django7

## 中间件

访问任何一个url地址,都会经过中间件,所以登录和注册时,不用做登录验证,要将两者屏蔽



在day05项目utils文件下新建一个middleware.py文件

```python
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from user.models import UserToken


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # 屏蔽掉登录和注册的url,不需要做登录验证
        not_check = ['/user/login/', '/user/register/']
        path = request.path
        if path in not_check:
            # 不继续执行以下登录验证的代码,直接执行视图函数
            return None

        token = request.COOKIES.get('token')
        if not token:
            # cookie中没有登录的标识符,跳转到登录
            return HttpResponseRedirect(reverse('user:login'))

        user_token = UserToken.objects.filter(token=token).first()
        if not user_token:
            # token标识符有误,跳转到登录页面
            return HttpResponseRedirect(reverse('user:login'))

        # 给全局request对象修改user属性值,修改为当前登录系统用户
        # 像京东导航栏上方,登录后每个页面都有用户
        request.user = user_token.user

        return None
```

## 上传图片

1. 在models.py文件中,建立一个文章模型

```python
from django.db import models

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=20)
    desc = models.CharField(max_length=150)
    img = models.ImageField(upload_to='article')
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'article'
```



2. 在urls.py文件中`url(r'^add_article/', views.add_article, name='add_article'),`

  `url(r'show_article/(\d+)/', views.show_article, name='show_article'),`

3. 在views.py文件中

```python
def add_article(request):
    if request.method == 'GET':
        return render(request, 'articles.html')
    if request.method == 'POST':

        #保存图片,文章
        img = request.FILES.get('img')
        title = request.POST.get('title')
        desc = request.POST.get('desc')
        #创建文章
        Article.objects.create(img=img,
                               title=title,
                               desc=desc)
        return HttpResponse('创建图片成功')


def show_article(request, id):
    if request.method == 'GET':
        article = Article.objects.get(pk=id)
        return render(request, 'show_articles.html', {'article':article})
```

4. 在articles.html中

```html
{% extends 'main.html' %}

{% block title %}
    添加文章页面
{% endblock %}

{% block content %}
    <form method="post" enctype="multipart/form-data">

        标题:<input type="text" name="title">
        <br>
        描述:<input type="text"  name="desc">
        <br>
        图片:<input type="file" name="img">
        <br>

        <input type="submit"  value="提交">

    </form>


{% endblock %}
```

  在show_articles.html中

```html
{% extends 'main.html' %}
{% block title %}
    展示文章
{% endblock %}

{% block content %}
    标题:{{ article.title }}
    描述:{{ article.desc }}
    图片:<img src="/media/{{ article.img }}">

{% endblock %}
```

**注:**

(1)安装PIL库

```
pip install Pillow
```

(2)定义Article模型时,图片字段设置

```
 img = models.ImageField(upload_to='article')
```

在指定字段为ImageField类型的时候，要指定upload_to参数，表示上传的图片的保存路径

(3) 应用中的settings.py文件中,配置media路径,media文件夹下保存存放的图片

```
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

(4)工程目录下的urls.py文件中,

```python
from django.contrib.staticfiles.urls import static

from day06.settings import MEDIA_URL, MEDIA_ROOT

#将media文件夹解析为静态文件夹
#django在debug为True的情况下,就可以访问media文件夹下的内容

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
```

(5)articles.html文件中,配置form表单的enctype属性`<form method="post" enctype="multipart/form-data">`

(6)views.py文件中注意获取图片用`img = request.FILES.get('img')`

(7)页面中解析上传的图片信息

  在数据库中用于保存图片的字段s_content的字段中存的是media下的upload/xxx.jpg地址，所以在页面解析的时候，需要加上media的目录，这样才能解析到图片在服务器中的路径

```html
图片:<img src="/media/{{ article.img }}">
```

## 分页

1. 分页的工具

>```
>Paginator： 数据分页工具
>Page：具体的某一页
>```



2. 语法

**Paginator(数据集, 每一页数据)**

属性：

```
count  计算和

num_pages: 页面总和

page_range: 页码列表，从1开始

```

方法：

```
page(页码)：获取的一个page对象，页码不存在则抛出invalidPage的异常
```

**page**

```
对象获取，通过Paginator的page()方法获得

```

属性：

```
object_list: 当前页面上所有的数据对象
number： 当前页的页码值
paginator: 当前page关联的Paginator对象

```

方法：

```
has_next()   判断是否有下一页
has_previous():  判断是否有上一页
has_other_pages():  判断是否有上一页或下一页
next_page_number();  返回下一页的页码
previous_page_number(): 返回上一页的页码
len(): 返回当前也的数据的个数
```

以下是代码

在views.py文件中

```python
def articles(request):
    if request.method == 'GET':
        # get(,1)1是默认值
        page = request.GET.get('page', 1)
        # 查询所有文章对象,并进行分页
        articles = Article.objects.all()
        # 将所有文章进行分页,每一页最多6条数据
        paginator = Paginator(articles, 6)
        # 获取哪一页文章信息
        arts = paginator.page(page)
        return render(request, 'arts.html', {'arts':arts})
```

在arts.html文件中

```html
{% extends 'main.html' %}

{% block content %}

{% for art in arts %}

    <p>标题:{{art.title}}</p>
    描述:{{art.desc}}
    图片:<img src="/media/{{ art.img }}">


{% endfor %}
<br>

<p>
    {% if arts.has_previous %}
        <a href="{% url 'user:articles' %}?page={{ arts.previous_page_number }}" >上一页</a>
    {% endif %}

    {% for i in arts.paginator.page_range %}
        <a href="{% url 'user:articles' %}?page={{ i }}">{{ i }}</a>
    {% endfor %}

    {% if arts.has_next %}
     <a href="{% url 'user:articles' %}?page={{ arts.next_page_number }}" >下一页</a>
    {% endif %}
</p>
{% endblock %}
```

## 日志

在settings.py文件中,配置日志,创建与templates,media,并列的logs文件

```python

#加上自己建好的LoggingMiddleware
MIDDLEWARE = ['utils.middleware.LoggingMiddleware']

#配置日志
LOGGING = {
    'version': 1,
    # True表示禁用日志
    'disable_existing_loggers': False,
    # 指定写入到日志文件中的日志格式
    'formatters': {
        'default':{
            'format':'%(name)s %(asctime)s %(message)s'
        }
    },
    'handlers':{
        'console':{
            'level': 'INFO',
            'filename': '%s/log.txt'% os.path.join(BASE_DIR, 'logs'),
            'formatter': 'default',
            #当日志文件大于5M,则做自动备份
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 5 * 1024 * 1024,
        }
    },
    'loggers':{
        '':{
            'handlers':['console'],
            'level':'INFO'
        }
    }
}
```

在middleware文件中

```python
class LoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 记录当前请求访问服务器的时间,请求参数,请求内容...
        request.init_time = time.time()
        request.init_body = request.body
        return None

    def process_response(self, request, response):
        # 记录返回响应的时间和访问服务器时间的差(时间戳),记录返回状态码...
        try:
            times = time.time() - request.init_time
            # 响应状态码
            code = response.status_code
            # 响应内容
            res_body = response.content
            # 请求内容
            req_body = request.init_body

            # 日志信息
            msg = '%s %s %s %s' %(times, code, res_body, req_body)
            # 写入日志
            logging.info(msg)
        except Exception as e:
            logging.critical('log error, Exception: %s' % e)
        return response
```

