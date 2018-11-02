---
author:于梦娇
title:django10
---

# django10

## 分页

  首先在settings.py文件中配置

```python
# rest-framework配置
REST_FRAMEWORK={
    #设置分页
    'DEFAULT_PAGINATION_CLASS':'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE':2,
    #过滤配置
    'DEFAULT_FILTER_BACKENDS':(
        'rest_framework.filters.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter'
    )
}
```

![分页](..\pictures\分页.png)

## 模糊查询

1. 安装过滤的库`pip install django-filter`



2. 在views.py文件中指定filter_class

```
class ArticleView(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin):
    # 查询数据(下面三个都是固定的)
    queryset = Article.objects.filter(is_delete=0)
    # 序列化
    serializer_class = ArticleSerializer
    # 过滤
    filter_class = ArticleFilter
```

3. 编写filter_class过滤信息

```python
#定义filter_class类
import django_filters

from rest_framework import filters

from app.models import Article


class ArticleFilter(filters.FilterSet):
    #i=ignore 忽略大小写,
    #127.0.0.1:8080/app/article/?t=django
    
    #查询标题模糊查询(lookup_expr)包含django
    t = django_filters.CharFilter('title', lookup_expr='icontains')
    desc = django_filters.CharFilter('desc', lookup_expr='contains')
    # 127.0.0.1:8080/app/article/?create_time_min=
    # 创建时间大于create_min并且小于create_max
    create_time_min = django_filters.DateTimeFilter('create_time', lookup_expr='gt')
    create_time_max = django_filters.DateTimeFilter('create_time', lookup_expr='lt')

    class Meta:
        model = Article
        fields = []
```

4. 实现方法

![模糊查询](..\pictures\模糊查询.png)



## cookie+session 会话保持



在views.py文件中

```python
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    if request.method == 'POST':
        # 1.获取参数
        name = request.POST.get('name')
        password = request.POST.get('pw')
        #2.验证数据完整性
        if not all([name, password]):
            msg = '请填写完整的登录信息'
            return render(request, 'login.html', {'msg':msg})
        #3.验证用户是否注册
        user = User.objects.filter(name=name).first()
        if not user:
            msg = '该账户没有注册,请去注册'
            return render(request, 'login.html', {'msg':msg})
        #4. 校验密码
        if password != user.password:
            msg = '密码不正确'
            return render(request, 'login.html', {'msg': msg})
        # 1.使用cookie+session
        # 向cookie中设置sessionid值
        # 向django_session表中存sessionid值
        # key:value存在session表中session_data
        request.session['user_id'] = user.id
        return HttpResponseRedirect(reverse('user:index'))
```

在functions.py文件中

```python
def login_required(func):

    def check_login(request):
        try:
            #验证cookie中的session值是否存在
            #验证服务端django_session表中 是否存在对应的记录值
            #如果存在则获取是否设置user_id值
            request.session['user_id']
        except Exception as e:
            return HttpResponseRedirect(reverse('user:login'))
        return func(request)
    return check_login
```



## 总结登录注册



1. django自带auth模块,实现登录注册注销

​         登录:auth.login()
​                 request.user赋值,赋值为登录系统的用户,在页面中直接解析{{ user }},{{ user.username }}
​         退出:auth.logout()
​                 request.user匿名用户AnymouseUser
​         验证:login_required()
​         权限验证: permission_required()

2. 自己实现,通过令牌token

​         登录:1)设置cookie,cookie中保存令牌token值

​                 2)服务端,保存token和登录系统用户关联关系(存在于mongodb)



​         退出:1)清空cookie

​                  2)删除服务端中token和用户的关联关系



​         登录校验:

​                  1)装饰器
​                  2)中间件
​                      验证cookie中的token值,是否能从服务端找到对应的用户信息

3. cookie+session (会话保持,会话上下文)

​          cookie:存放在客户端
​          session:存放在服务端

​          登录: request.session[key]=value
​          退出: 删除session中的key
​          登录校验: 获取session中的key值,如果能获取到,表示登录,获取不到,表示没登录	