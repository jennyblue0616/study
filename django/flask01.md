---
author: 于梦娇
title:flask01
---

# flask01

## 创建flask

1.创建虚拟环境

`virtualenv --no-site-packages flaskenv6`

激活虚拟环境后,安装flask`pip install flask`

2.打开pycharm,创建new project,环境选择刚才装好的flaskenv6下的python.exe

  创建一个新的py文件

```python
# 导入Flask类
from flask import Flask
# 创建该类的实例,第一个参数是应用模块或包的名称,如果你使用单一的模块（如本例），你应该使用 __name__ 
app = Flask(__name__)
# 使用 route() 装饰器告诉 Flask 什么样的URL 能触发函数。
@app.route('/')
def hello_world():
    return 'Hello World!'
# 最后用 run() 函数来让应用运行在本地服务器上。 其中 if __name__ == '__main__': 确保服务器只会在该脚本被 Python 解释器直接执行的时候才会运行，而不是作为模块导入的时候。
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080, debug=True)
```

## 修改启动方式,使用命令行参数启动服务

1. 安装插件`pip install flask-script`

可以把安装的东西都写在一个txt文件中,安装时执行命令`pip install -r req.txt `,就可以一行一行安装

```python
from flask import Manager
from flask import Flask

app = Flask(__name__)
# 使用Manger管理app对象
manage = Manager(app)

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    manage.run()
```

  terminal中输入`python first.py runserver -p 8080 -h 0.0.0.0 -d`,就可以启动了

  也可以写成脚本文件

## 路由匹配规则

>写法：<选择器:参数名>
>
>选择器类型：
>
>```
>string 字符串
>int 整形
>float 浮点型
>path 接受路径，接收的时候是str，/也当做字符串的一个字符
>uuid 只接受uuid字符串
>any 可以同时指定多种路径，进行限定
>没有定义选择器: 表示接受的参数为string类型(默认)
>```
>
>例子：
>
>```
>@app_blueprint.route('/student/<int:id>/')
>def student(id):
>    return '我是学号为%d的学生' % id
>
>@app_blueprint.route('/float/<float:number>/')
>def hello_float(number):
>    return '我是float类型的参数: %s' % number
>
>
>@app_blueprint.route('/hello/<string:name>/')
>def hello_name(name):
>    return '你好: %s' % name
>
># 可以全部匹配path/后面的所有东西
>@app_blueprint.route('/path/<path:name>/')
>def path_name(name):
>    return  'path: %s' % name
>
>@app_blueprint.route('/uuid/<uuid:name>')
>def uuid_name(name):
>    return 'uuid: %s' % name
>```

## 拆分代码  蓝图管理路由

使用蓝图管理路由，蓝图的好处就是模块化管理应用

txt文件中加入flask_blueprint



  第一步: 实例化蓝图

`app_blueprint = Blueprint('app', __name__)`

Blueprint中传入了两个参数，第一个是蓝图的名称，第二个是蓝图所在的包或模块，`__name__`代表当前模块名或者包名

  第二步:注册

`app.register_blueprint(blueprint=app_blueprint, url_prefix='/app')`

注意：第一个参数即我们定义初始化定义的蓝图对象，第二个参数url_prefix表示该蓝图下，所有的url请求必须以/app开始。这样对一个模块的url可以很好的进行统一管理

  第三步:使用蓝图

修改视图上的装饰器，修改为@blue.router(‘/’)

```python
# manage.py
from flask import Flask
from flask_script import Manager

from app.views import app_blueprint

app = Flask(__name__)

# 第二步,注册蓝图(蓝图实现模块化的管理)
app.register_blueprint(blueprint=app_blueprint, url_prefix='/app')

# 使用Manager管理app对象
manage = Manager(app)



if __name__ == '__main__':
    
    manage.run()
    # python manage.py runserver -p -h -d
```

views.py文件

```python
import uuid

from flask import Blueprint,redirect, url_for, request, make_response, abort

#第一步,生成蓝图对象,使用蓝图对象管理路由
app_blueprint = Blueprint('app', __name__)


@app_blueprint.route('/hello/', methods=['GET', 'POST', 'PATCH'])
def hello():
    if request.method == 'GET':
        # 获取get提交请求传递的参数:request.args
        # request.args[key]或request.args.get('key')
        return 'Hello World!'
    if request.method == 'POST':
        # TODO: 获取post提交的参数
        # 获取post提交请求传递的参数:request.form
        return '你好,我是小猪猪'


@app_blueprint.route('/student/<int:id>/')
def student(id):
    return '我是学号为%d的学生' % id


@app_blueprint.route('/redirect/')
def redirect_url():
    # Django写法:HttpResponseRedirect(reverse('namespace:name'))
    # Flask写法:redirect(url_for('蓝图名称.跳转的函数名', key=value))
    return redirect(url_for('app.student', id=10))


# 响应response,是后端产生返回给前端(浏览器)
# make_response(响应内容, 响应状态码(默认为200))
# 响应绑定cookie, set_cookie/delete_cookie

@app_blueprint.route('/make_response/', methods=['GET'])
def make_my_response():
    res = make_response('<h2>今天天气真好</h2>', 200)

    return res


@app_blueprint.route('/absort_a/', methods=['POST'])
def absorb_a():
    try:
        a = int(request.form.get('a'))
        b = int(request.form.get('b'))
        c = a/b
        return '%s/%s=%s' % (a, b, c)

    except Exception as e:
        # 异常抛出
        abort(500)


@app_blueprint.errorhandler(500)
def error_handler(error):
    # 返回错误页面
    return 'Exception is %s' % error

```

## 反向解析



`url_for('蓝图中定义的第一个参数.函数名', 参数名=value)`

```python
@app_blueprint.route('/redirect/')
def redirect_url():
    # Django写法:HttpResponseRedirect(reverse('namespace:name'))
    # Flask写法:redirect(url_for('蓝图名称.跳转的函数名', key=value))
    return redirect(url_for('app.student', id=10))
```

## 请求与响应

>```
>服务端在接收到客户端的请求后，会自动创建Request对象
>request请求(浏览器到后端)
> 获取get传参:request.args
> 获取post传参:request.form
> request.from.get()---获取一个值
> request.form.getlist()---获取多个值
> 获取上传文件:request.files
> 获取路径:request.path
> 请求方式:request.method
>```

```python
@app_blueprint.route('/hello/', methods=['GET', 'POST', 'PATCH'])
def hello():
    if request.method == 'GET':
        # 获取get提交请求传递的参数:request.args
        # request.args[key]或request.args.get('key')
        return 'Hello World!'
    if request.method == 'POST':
        # TODO: 获取post提交的参数
        # 获取post提交请求传递的参数:request.form
        return '你好,我是小猪猪'
```

>```
>Response是由开发者自己创建的
>响应response,是后端产生返回给前端(浏览器)
>make_response(响应内容, 响应状态码(默认为200))
>响应绑定cookie, set_cookie/delete_cookie
>```

创建方法：

```
from flask import make_response

make_response创建一个响应，是一个真正的Response对象

```

状态码：

格式：make_reponse(data，code)，其中data是返回的数据内容，code是状态码

```
a）直接将内容当做make_response的第一个参数，第二个参数直接写返回的状态码

b）直接在render后加返回的状态码
```

```python
@app_blueprint.route('/make_response/', methods=['GET'])
def make_my_response():
    res = make_response('<h2>今天天气真好</h2>', 200)

    return res

```



## 异常抛出与捕获

抛出：abort(状态码)

捕获: @blue.errorhandler(状态码)

```python
@app_blueprint.route('/absort_a/', methods=['POST'])
def absorb_a():
    try:
        a = int(request.form.get('a'))
        b = int(request.form.get('b'))
        c = a/b
        return '%s/%s=%s' % (a, b, c)

    except Exception as e:
        # 异常抛出
        abort(500)


@app_blueprint.errorhandler(500)
def error_handler(error):
    # 返回错误页面
    return 'Exception is %s' % error

```

