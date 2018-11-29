---
title:flask04
author:于梦娇
---

## flask04

### 多对一查询(正向,反向)

  models.py文件中

```python
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    s_name = db.Column(db.String(10), unique=True, nullable=False)
    gender = db.Column(db.Boolean, default=1)
    grade_id = db.Column(db.Integer, db.ForeignKey('grade.id'), nullable=False)

    #__tablename__用于指定模型映射的表名,如果没有指定,则表名为模型名的小写

    def save(self):
        db.session.add(self)
        db.session.commit()


class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g_name = db.Column(db.String(10), unique=True, nullable=False)
    student = db.relationship('Student', backref='g')

```

在views.py文件中

```python
@blue.route('/sel_grade_by_stu/', methods=['GET'])
def sel_grade_by_stu():
  #通过学生查询班级
  stu = Student.query.filter(Student.s_name=='小雨').first()
  #学生对象.backref
  grade = stu.g.g_name
  return '获取班级成功'
  
  
@blue.route('/sel_stu_by_grade/', methods=['GET'])
def sel_stu_by_grade():
  #通过班级查询学生
  grade = Grade.query.get(1)
  stus = grade.student
  return '获取学生成功'
```



### 多对多关系

  定义课程表,和学生表建立多对多的关联关系,需要自己建立中间表,中间表的两个字段都需要建立外键.

```python
s_c = db.Table('s_c',
               db.Column('s_id', db.Integer,db.ForeignKey('student.id')),
               db.Column('c_id', db.Integer,db.ForeignKey('course.id')))


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    c_name = db.Column(db.String(10), nullable=False, unique=True)
    student = db.relationship('Student', secondary=s_c, backref='cou')

    __tablename__ = 'course'
```

  首先需要一个students.html页面,加载学生的信息,并添加课程和删除课程的按钮功能

```
# 在views.py文件中,定义一个视图函数,返回学生对象信息
@blue.route('/all_stu/', methods=['GET'])
def all_stu():
    stus = Student.query.all()
    return render_template('students.html', stus=stus)
```

在students.html页面中,解析学生对象信息

```html

{% extends 'base.html' %}

{% block content %}
<table>
    <thead>
        <th>id</th>
        <th>姓名</th>
        <th>班级</th>
        <th>课程</th>
        <th>操作</th>
    </thead>
    <tbody>
    {% for stu in stus %}
        <tr>
            <td>{{ stu.id }}</td>
            <td>{{ stu.s_name }}</td>
            <td>{{ stu.g.g_name }}</td>
            <td>
                {% for c in stu.cou %}
                    {{ c.c_name }}
                {% endfor %}
            </td>
            <td>
                <a href="{{ url_for('app.cous', id=stu.id) }}">添加学生课程</a>
                |
                <a href="{{ url_for('app.del_stu_cou', id=stu.id ) }}" >删除学生课程</a>
            </td>
        </tr>
    {% endfor %}
    </tbody>
</table>

{% endblock %}
```



然后再写一个返回课程信息的方法,在选择课程后,在同一页面实现提交数据,在中间表中加入数据,通过关联关系backref='cou',进行关联,append方法进行添加

```python
@blue.route('/cous/<int:id>/', methods=['GET', 'POST'])
def cous(id):
    #返回课程信息
    if request.method == 'GET':
        cous = Course.query.all()
        return render_template('cous.html', cous=cous)

    if request.method == 'POST':
        #向中间表s_c中加入数据
        cou_id = request.form.get('cou_id')
        s_id = id
        # 获取对象
        stu = Student.query.get(s_id)
        cou = Course.query.get(cou_id)
        #学生.backref.append(课程) 关系指定
        stu.cou.append(cou)
        # cou.student.append(stu) 与上面的实现方法相同
        db.session.commit()
        return redirect(url_for('app.all_stu'))
```

cous.html页面

```html
{% extends 'base.html' %}

{% block content %}
    <form action="" method="post">
        <select name="cou_id">
            {% for cou in cous %}
            <option value="{{ cou.id }}">
                {{ cou.c_name }}
            </option>
            {% endfor %}
        </select>
        <input type="submit" value="提交">
    </form>
{% endblock %}
```

  删除所选课程,调用ajax

```python
@blue.route('/del_stu_cou/<int:id>/', methods=['GET', 'DELETE'])
def del_stu_cou(id):
    if request.method == 'GET':
        stu = Student.query.get(id)
        cous = stu.cou

        return render_template('s_c.html', cous=cous, s_id=id)
    if request.method == 'DELETE':

        c_id = request.form.get('c_id')
        s_id = request.form.get('s_id')
        # 获取对象
        stu = Student.query.get(s_id)
        cou = Course.query.get(c_id)
        # 删除学生和课程的关联关系
        stu.cou.remove(cou)
        db.session.commit()
        return jsonify({'code':200, 'msg':'请求成功'})
```

  在s_c.html页面中,ajax向后端传入两个参数,课程的id和学生的id



```python
{% extends 'base.html' %}

{% block js %}
    <script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
    <script>
        function del_cou(c_id, s_id){
            $.ajax({
                url: '/app/del_stu_cou/'+s_id+'/',
                dataType: 'json',
                type: 'DELETE',
                data: {'c_id':c_id, 's_id':s_id},
                success:function(data){
                    if(data.code == '200'){
                        location.href='/app/all_stu/'
                    }
                },
                error:function(data){
                     alert('删除失败')
                }
            })
        }
    </script>

{% endblock %}

{% block content %}
    {% for c in cous %}
        <p>
            {{ c.c_name }}
            <a onclick="del_cou({{ c.id }},{{ s_id }})" href="">删除</a>
        </p>
    {% endfor %}

{% endblock %}
```

## 钩子函数

  钩子的概念源于Windows的消息处理机制,通过设置钩子,应用程序可以对所有消息事件进行拦截,然后执行钩子函数,对消息进行想要的处理.

**回调函数和钩子函数的区别** 
根本上，他们都是为了捕获消息而生的，但是钩子函数在捕获消息的第一时间就会执行，而回调函数是在整个捕获过程结束时，最后一个被执行的。

回调函数其实就是调用者把回调函数的函数指针传递给调用函数，当调用函数执行完毕时，通过函数指针来调用回调函数。

对于前端来说，钩子函数就是指在执行所有函数前，先执行了的函数，此概念（或者说现象）跟AOP（面向切面编程）很像,可以与django中的中间件对比记忆.



 在Web开发中经常会对所有的请求做一些相同的操作，如果将相同的代码写入每一个视图函数中，那么程序就会变得非常臃肿。为了避免在每个视图函数中定义相同的代码，可以使用钩子函数。如下有三个常见的钩子:

1. before_request: 被装饰的函数会在每个请求被处理之前调用。
2. after_request: 被装饰的函数会在每个请求退出时才被调用。在程序没有抛出异常的情况下，才会被执行。
3. teardown_request: 被装饰的函数会在每个请求退出时才被调用。不论程序是否抛出异常，都会执行。

```python
@blue.before_request
def before_request():
    print('before_request')


@blue.before_request
def before1_request():
    print('before1_request')


@blue.after_request
def after_request(response):
    print('1')
    return response


@blue.after_request
def after_request(response):
    print('after_request')
    return response

# 响应完成之后
@blue.teardown_request
def teardown_request(exception):
    print('teardown_request')

```

before_request是从前往后的顺序进行执行的,after_request是从后往前的顺序执行.teardown_request是无论如何都会执行,但是如果有错误,只有before_request会执行,after_request不会执行

  各函数的执行顺序为，被before_request装饰的函数会在请求处理之前被调用。而after_request和teardown_request会在请求处理完后才被调用。区别就在于after_request只会在请求正常退出的情况下才会被调用，并且atfer_request函数必须接受一个响应对象，并返回一个响应对象。而teardown_request函数在任何情况下都会被调用，并且必须传入一个参数来接收异常对象。

### g

g是应用上下文,可以在before_request设置一个g.cursor = cursor
在hello():

​	g.cursor.execute(sql)拿到

g是当前请求的全局变量

 应用全局对象（g）是Flask为每一个请求自动建立的一个对象。g的作用范围只是在一个请求（也就是一个线程）里，它不能在多个请求中共享数据，故此应用全局变量（g）确保了线程安全。

```python

import pymysql

from flask import Flask, g

app = Flask(__name__)


@app.route('/hello/')
def hello():
    # 获取学生表中的数据
    sql = 'select * from student;'
    result = g.cursor.execute(sql)
    data = g.cursor.fetchall()
    return 'hello'


@app.before_request
def before_request():
    # TODO: pymysql连接数据库
    conn = pymysql.Connection(host='127.0.0.1', port=3306,
                       user='root', password='123456',
                       database='flask6')
    # 游标
    cursor = conn.cursor()
    g.cursor = cursor
    g.conn = conn
    # cursor.execute(sql)
    print('数据库在此连接')

@app.teardown_request
def teardown_request(exception):
    # 关闭数据库的连接
    g.conn.close()

if __name__ == '__main__':
    app.run()
```









### flask-wtf表单验证

安装Flask-WTF

`pip install flask-wtf`



在views.py文件中,当HTTP请求为GET时，将表单验证对象返回给页面。

当HTTP请求为POST时，通过方法validate_on_submit()方法进行字段校验和提交判断，如果校验失败，则可以从form.errors中获取错误信息。

如果验证通过，则从form.字段.data中获取到字段的值。

```python
from flask import Blueprint, request, render_template, url_for
from werkzeug.utils import redirect
from werkzeug.security import generate_password_hash,check_password_hash

from app.form import RegisterForm
from app.models import User, db

blue = Blueprint('user', __name__)


@blue.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'GET':
        return render_template('register.html', form=form)

    if request.method == 'POST':
        if form.validate_on_submit():
            #验证是否必填
            #验证用户是否注册,验证密码和确认密码是否一致
            user = User()
            user.username = form.username.data
            user.password = generate_password_hash(form.password.data)
            db.session.add(user)
            db.session.commit()
            return '注册成功'
        else:
            return redirect(url_for('app.register'))
```

在form.py文件中定义需要验证的username、password和password2字段，并实现如下校验:

1. 校验密码password2和password相等(EqualTo)
2. 校验用户名是否存在field.data
3. 校验用户名的长度是否符合规范

```python
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,ValidationError
from wtforms.validators import DataRequired, EqualTo

from app.models import User


class RegisterForm(FlaskForm):

    username = StringField('用户名', validators=[DataRequired()])
    password = StringField('输入密码', validators=[DataRequired()])
    password2 = StringField('确认密码', validators=[DataRequired(),
                                                EqualTo('password', '密码不一致')])

    submit = SubmitField('提交')

    def validate_username(self, field):
        # 验证用户是否注册
        user = User.query.filter_by(username=field.data).first()
        if user:
            raise ValidationError('用户已经注册')
        if len(field.data) > 6:
            raise ValidationError('用户名不能超过6字符')
        if len(field.data) < 2:
            raise ValidationError('用户名不能少于2字符')
```

在register.html文件中

>1. 定义字段名: {{ form.字段.label }}
>
>2. 定义input输入框: {{ form.字段 }}
>
>3. 展示错误信息: {{ form.errors.字段 }}
>
>4. 跨站请求伪造: {{ form.csrf_token }}



```html
{% extends 'base.html' %}

{% block content %}

    <form action="" method="post">
        {{ form.csrf_token }}
        {{ form.username.label }}:{{ form.username }}
        <br>
        {{ form.password.label }}:{{ form.password }}
        <br>
        {{ form.password2.label }}:{{ form.password2 }}
        <br>
        {{ form.submit }}
      
      	{% if form.errors %}
            姓名错误信息:{{ form.errors.username }}
            密码错误信息:{{ form.errors.password2 }}
        {% endif %}
    </form>

{% endblock %}
```

常见字段类型

```
字段类型	说明
StringField	普通文本字段
PasswordField	密码文本字段
SubmitField	提交按钮
HiddenField	隐藏文本字段
TextAreaField	多行文本字段
DateField	文本字段，datetime.date格式
DateTimeField	文本字段，datetime.datetime格式
IntegerField	文本字段，整数类型
FloatField	文本字段，小数类型
BooleanField	复选框，值为True或False
RadioField	单选框
SelectField	下拉列表
FileField	文件上传字段
```

验证器

```
验证器	说明
DataRequired	确保字段有值(并且if判断为真)
Email	邮箱地址
IPAddress	IPv4的IP地址
Length	规定字符长度
NumberRange	输入数值的范围
EqualTo	验证两个字段的一致性
URL	有效的URL
Regexp	正则验证
```