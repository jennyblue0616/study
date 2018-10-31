---
author:于梦娇
title:django8
---

# django8

## 权限

  RBAC（Role-Based Access Control，基于角色的访问控制）就是用户通过角色与权限进行关联。简单地说，一个用户拥有若干角色，每一个角色拥有若干权限。这样，就构造成“用户-角色-权限”的授权模型。在这种模型中，用户与角色之间，角色与权限之间，一般者是多对多的关系。![per](..\pictures\per.png)

```python
class PermissionsMixin(models.Model):
	groups = models.ManyToManyField(Group..)
	user_permissions = models.ManyToManyField(Permission..)

class Group(models.Model):
	permissions = models.ManyToManyField(Permission..)
	objects = GroupManager()
	
class Permission(models.Model):
	content_type = models.ForeignKey(ContentType..)
```

防止被劫持 
在表单中添加{% csrf_token %}就可以 生成随机字符串,提交表单中的数据会进行校验

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <form action=""  method="post">
        {% csrf_token %}
        姓名:<input type="text" name="username">
        密码:<input type="text" name="password">
        <input type="submit" value="提交">


    </form>

</body>
</html>
```





1. 在应用中的models.py文件中自定义权限,自定义权限的名称（‘codename’，‘name’）即codename为权限名，name为权限的描述。

```python
from django.contrib.auth.models import User, Permission, Group, AbstractUser
from django.db import models

# Create your models here.
class MyUser(AbstractUser):
    # 拓展django自带的auth_user表,可以自定义新增的字段

    class Meta:
        # django,默认给每个模型初始化三个权限
        # 默认是change, delete, add权限
        permissions = (
            ('add_my_user', '新增用户权限'),
            ('change_my_user_username', '修改用户名权限'),
            ('change_my_user_password', '修改用户密码权限'),
            ('all_my_user', '查看用户权限'),
        )

```

在settings.py文件中添加`AUTH_USER_MODEL = 'app.MyUser'`,告诉django, User模型修改为自定义的User模型,在数据库的auth_permission表中，会新增权限.

2. 创建权限

>用户Users模型和权限Permission之间是ManyToManyField()多对多关联关系，关联字段为user_permission。
>
>添加权限：user对象.user_permission.add(permission对象1, permission对象2)
>
>删除权限：user对象.user_permission.remove(permission对象1, permission对象2)
>
>清空权限：user对象.user_permission.clear()



```python
def add_user_permission(request):
    if request.method == 'GET':
        # 1.创建用户abc
        user = MyUser.objects.create_user(username='abc',
                              password='123'
        )
        # 2.指定刚创建的用户,并分配给它权限(新增用户权限,查看用户权限)

        permissions = Permission.objects.filter(codename__in=['add_my_user','all_my_user']).all()

        for permission in permissions:
        # 多对多的添加,添加关联关系
            user.user_permissions.add(permission)

        #3.删除刚创建的用户的新增用户权限
        # user.user_permissions.remove(权限对象)

        return HttpResponse('创建用户权限成功')
```

3. 创建,分配组

>给组添加权限，涉及到组group表和permission权限表，以及中间关联表。其为ManyToManyFiled()关联关系，关联字段为permissions 语法:
>
>添加权限：group对象.permissions.add(permission对象1, permission对象2)
>
>删除权限：group对象.permissions.remove(permission对象1, permission对象2)
>
>清空权限：group对象.permissions.clear()

>给用户添加组权限，涉及到组group表和user用户表，以及中间关联表。其为ManyToManyFiled()关联关系，关联字段为groups 语法:
>
>添加权限：user对象.groups.add(groups对象1, groups对象2)
>
>删除权限：user对象.groups.remove(groups对象1, groups对象2)
>
>清空权限：user对象.groups.clear()



```python
def add_group_permission(request):
    if request.method == 'GET':
        # 创建超级管理员组(所有),创建普通管理员(修改,查看)(审核组)
        group = Group.objects.create(name='审查组')

        ps = Permission.objects.filter(codename__in=['all_my_user',
                                                'change_my_user_password',
                                                'all_my_user']).all()
        for permission in ps:
            group.permissions.add(permission)

        return HttpResponse('创建组权限成功')

def add_user_group(request):
    if request.method == 'GET':
        # 给abc用户分配审查组
        user = MyUser.objects.filter(username='abc').first()
        group = Group.objects.filter(name='审查组').first()
        # 分配组
        user.groups.add(group)

        return HttpResponse('用户分配组成功')
```

4. 检测用户是否有某权限,和所有权限，组权限

   >查询用户所有的权限：**user.get_all_permissions()**方法列出用户的所有权限，返回值是permission name
   >
   >查询用户的组权限：**user.get_group_permissions()**方法列出用户所属group的权限，返回值是permission name

      django自带的

   ```python
   def my_index(request):
       if request.method == 'GET':
           #当前登录系统的用户
           user = request.user
           # 获取当前用户对应组的权限
           user.get_group_permissions()
           # 获取当前用户的所有权限
           user.get_all_permissions()
           # 判断是否有某个权限
           user.has_perm('应用app名.权限名')
           return render(request, 'my_index.html')
   ```

     自己写的

   ```html
   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8">
       <title>Title</title>
   </head>
   <body>
       <!--通过用户查询组,组查询权限-->
       <!--{{ user.groups.all.0.permissions.all }}-->
       {% for permission in user.groups.all.0.permissions.all %}
           {{ permission.codename }}
       {% endfor %}
       <!--通过用户直接查找权限-->
       <br>
       <!--{{ user.user_permissions.all }}-->
       {% for per in user.user_permissions.all %}
           {{ per.codename }}
       {% endfor %}

   </body>

   </html>
   ```

5. 校验权限

  django自带

```python
from django.contrib.auth.decorators import permission_required
@permission_required('app.a_my_user')
def new_index(request):
    if request.method == 'GET':
        return HttpResponse('需要权限才能查看')
```

  自己写装饰器

```python
from django.contrib.auth.models import Permission
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from app.models import MyUser

# 1. 外层函数内嵌内层函数
# 2. 外层函数返回内层函数
# 3. 内层函数调用外层函数的参数


def check_permissions(func):

    def check_login(request):
        # abc用户,有查看用户列表权限 才能访问如下的视图函数
        user = MyUser.objects.filter(username='abc').first()
        # 验证权限 user.user_permissions全部权限
        permission = user.user_permissions.filter(codename='all_my_user').first()

        if permission:
            #用户有列表权限,则继续访问被装饰器装饰的函数
            return func(request)
        else:
            return HttpResponse('用户没有查看列表权限,不能访问方法')

    return check_login


```

定义登录的路由，并实现登录操作，当用户登录后，再次访问all_my_user.html路由地址，则可以访问到对应的视图函数，如果用户没有登录则因为权限问题访问不了all_my_user.html路由对应的视图函数。