---
author: 于梦娇
title: flask02
---

# flask02

 ### session

 session 可以看做是在不同的请求之间保存数据的方法,因为 HTTP 是无状态的协议，但是在业务应用上我们希望知道不同请求是否是同一个人发起的。比如张三，王二都在自己的手机上用淘宝购物，将想购买的商品放入购物车中，当王二，张三结账时，不能将他俩的购物车混淆了，服务器区分和保存购物车数据的方法就是session。

flask的session是基于cookie的会话保持。简单的原理即：

当客户端进行第一次请求时，客户端的HTTP request（cookie为空）到服务端，服务端创建session，视图函数根据form表单填写session，请求结束时，session内容填写入response的cookie中并返回给客户端，客户端的cookie中便保存了用户的数据。

当同一客户端再次请求时， 客户端的HTTP request中cookie已经携带数据，视图函数根据cookie中值做相应操作（如已经携带用户名和密码就可以直接登陆）。

flask中有一个session对象,允许在不同请求间存储特定用户信息

 Session和Cookie的结合使用,一般有两种存储方式:

第一种: session数据存储在客户端,session数据保存在cookie中

第二种:session数据存储在服务端中

当客户端发送请求到服务端的时候,服务端会校验请求中cookie参数中的sessionid值,如果没有,则服务端会传递给客户端一个cookie,并在cookie中存储一个新的sessionid值,并将数据保存在session,当下次客户端再发送请求时,通过校验cookie中的sessionid,即可判断是否是同一会话.如果一致,则可以从session中获取之前保存的数据

### Cookie

概念：

```
a）客户端会话技术，浏览器的会话技术

b）数据全部存储在客户端中

c）存储使用的键值对结构进行存储

特性：
	支持过期时间
	默认会自动携带本网站的cookie
	不能跨域名
	不能跨浏览器
```

**第一种方式:将session数据存储在cookie中**

```python
在views.py文件中
from flask import Blueprint, request, render_template, session, url_for, redirect

from utils.function import login_function

@blue.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == '123123':
            # 模拟校验用户名和密码成功, 则向session中存储登录成功后的用户id值
            session['user_id'] = 1
            # return redirect(url_for('user.index'))
            return redirect('/app/index/')
        else:
            return render_template('login.html')
        
@blue.route('/index/')
@login_function
def index():
    user_id = session['user_id']
    return '我是首页, 用户id为%s' % user_id
```

在manage.py文件中设置secret_key加密

`app.secret_key = 'dfdkjshfkjs'`

```html
在login.html页面
{% extends 'base_main.html' %}
{% block css %}
<!--django中是block.super-->
    {{ super() }}
{% endblock %}

{% block content  %}
    {% from 'function.html' import hello %}

    {{ hello() }}

    <p>登录页面</p>
    <form action="" method="post">
        用户名:<input type="text" name="username">
        密码:<input type="password" name="password">
        <input type="submit" value="提交">
    </form>

{% endblock %}
```



在function.py文件中,写登录校验的装饰器

```python

from flask import session, render_template,redirect, url_for

def login_function(func):
    def login_user():
        try:
            user_id = session['user_id']
        except Exception as e:
            return redirect(url_for('user.login'))
        return func()
    return login_user

def login_a(func):
    def login_user():
        user_id = session.get('user_id')
        if not user_id:
            return redirect(url_for('user.login'))
        return func()
    return login_user
```

**第二种方式:session存储到数据库redis中**

  在manage.py文件中,配置session存储数据库

`app.config['SESSION_TYPE'] = 'redis'`

`app.config['SESSION_REDIS'] = redis.Redis(host='127.0.0.1', port=6379)`

```
初始化flask对象app
第一种
Session(app)

第二种
sess = Session()
sess.init_app(app)
```

### 模板

与dajong不同之处在于

(1) 继承{{ super() }}

(2) 静态文件加载

```html
<!--引入static中的css-->
<!--第一种-->
<link href="/static/css/style.css" rel="stylesheet">
<!--第二种-->
<link  href="{{ url_for('static', filename='css/style.css') }}" rel="stylesheet">

```

(3) 编号 {{ loop.index }}

(4) 定义宏,可以把宏单独定义在templates文件夹下的function.html文件中

```html
<!--声明函数-->
    {% macro hello() %}
        <p>
            你好
        </p>
    {% endmacro %}

    {% macro say(name) %}
        <p>你好,{{ name }}</p>
    {% endmacro %}
```

引用时写`{% from 'function.html' import hello %}`

`{{ hello() }}`

### 模型

安装 pip install pymysql

pip install flask-sqlalchemy



在models.py文件中

```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# 第一步:声明模型


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True,nullable=False)
    password = db.Column(db.String(100), nullable=True)
    gender = db.Column(db.Boolean, default=1)

    __tablename__ = 'day02_user'



```



在manage.py文件中修改配置

```python
from app.models import db
# 数据库配置
# dialect+driver://username:password@host:port/database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/flask6'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 初始化app和db
db.init_app(app)
```

在views.py文件中迁移表

```python
@blue.route('/create_db/')
def create_db():
    # 第一次迁移模型
    db.create_all()
    return '创建模型成功'

@blue.route('/drop_db/')
def drop_db():
    db.drop_all()
    return '删除模型成功'
```

