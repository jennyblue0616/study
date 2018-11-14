---
author: 于梦娇
title: flask03
---

# flask03

  首先,创建一个学生表

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
        
@blue.route('/create/')
def create():
    db.create_all()
    return '创建模型成功'
```

  ## 给学生表添加数据



`db.session.add(object)`

`db.session.commit()`

  可以写成模型的方法,要用的时候直接掉方法save()

```python 
@blue.route('/add_stu/', methods=['POST'])
def add_stu():
    #插入数据
    stu = Student()
    stu.s_name = '小兔子'
    #向数据库发送insert语句
    # db.session.add(stu)
    # commit才是提交
    # db.session.commit()
    stu.save()
    return '创建学生成功'
```

`db.session.add_all(list[object])`

`db.session.commit()`

````python
# 添加班级信息
# 学生指定班级
@blue.route('/grade/', methods=['POST'])
def grade():
    grades = ['一班', '二班', '三班']
    g_list = []
    for i in grades:
        grade = Grade()
        grade.g_name= i
        g_list.append(grade)
        # db.session.add(grade)
    db.session.add_all(g_list)
    db.session.commit()
    return '创建班级成功'
````



## 删除数据

`db.session.delete(object)`

`db.session.commit()`

```python
@blue.route('/del_stu/', methods=['DELETE'])
def del_stu():
    # 删除数据
    stu = Student.query.filter(Student.s_name == '小兔子').first()
    db.session.delete(stu)
    db.session.commit()
    return '删除学生成功'
```

## 更新数据

  有两种方法:第一种,先查询出要修改的对象,然后修改字段.第二种使用update

`Student.query.filter(Student.s_name=='a').update({'s_name':'b'})`

`db.session.commit()`



```python
@blue.route('/update/', methods=['PATCH'])
def update():
    # 第一种方式
    # stu = Student.query.filter(Student.s_name == '小雨').first()
    # stu.s_name = '小笨蛋'
    # stu.save()
    # 第二种:使用update
    Student.query.filter(Student.s_name=='小笨蛋').update({'s_name':'小雨'})
    # 保持事务完整性
    db.session.commit()
    return '更新学生成功'
```

## 查询数据



**filter(模型名.字段 == '值')**
**filter_by(字段 = '值')**

**all():获取查询的值,为列表**
**first():获取第一个查询值**

```python
@blue.route('/sel/', methods=['GET'])
def sel():
    # filter(模型名.字段=='值')
    # filter_by(字段='值')
    stu = Student.query.filter_by(s_name='小雨').first()
    # all():查询所有结果,返回结果列表
    # first():返回对象
    # 注意:不要写all().first()
```



**get():获取主键所在行的对象信息**



```python
# 查询id为1的学生,使用get()方法,获取主键所在行的对象,不存在不会报错,返回空
    # stu = Student.query.filter_by(id=1).first() 相当于get(1)
    stu = Student.query.get(1)
    

```



**order_by() :排序**

```python
 #order_by():排序,
    # 降序: -id,id desc
    # 升序: id,id asc
    stu = Student.query.order_by('-id')

```



**模糊查询:contains(),like(),startswith(),endswith()**

**%:代表一个或多个**

**_:代表一个**

**范围之内in_()**

```python
# 使用运算符
    # Django的orm中:filter(s_name__contains='a')
    # Flask的SQLAlchemy:filter(模型名.s_name.contains('a'))

    # 例子:模糊查询姓名中包含'雨'的学生信息
    stu = Student.query.filter(Student.s_name.contains('雨')).all()

    # startswith, endswith, like _和 %, contains
    stus = Student.query.filter(Student.s_name.startswith('小')).all()
    stus = Student.query.filter(Student.s_name.endswith('子')).all()

    #查询姓名中包含'雨'的学生信息,使用like,_和% ('%雨%')同contains一样
    stus = Student.query.filter(Student.s_name.like('_雨')).all()

    # in_():查询某个范围之内的对象
    stus = Student.query.filter(Student.id.in_([1,2,3,4])).all()
```



**大于__gt__,小于__lt__**

```python
# 查询id大于3的学生信息,__gt__
    # 大于 __gt__,大于等于__ge__
    # 小于 __lt__,小于等于__le__
    stus = Student.query.filter(Student.id.__gt__(3)).all()
    stus = Student.query.filter(Student.id > 3).all()
    stus = Student.query.filter(Student.id.__lt__(4)).all()
    stus = Student.query.filter(Student.id < 4).all()
```

**分页**

后端数据处理

```python
  # 分页,第一页,每页三条数据
    page = request.args.get('page', 1)
    paginate = Student.query.paginate(int(page), 3)
    # stus.items每一页的内容
    stus = paginate.items
    # return render_template('stus.html', stus=stus, paginate=paginate)
```

前端数据展示

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>

    {% for stu in stus %}
    <p>id:{{ stu.id }}  姓名:{{ stu.s_name }}</p>
    {% endfor %}
    当前一共{{paginate.pages}}页
    {% if paginate.has_prev %}
        <a href="{{ url_for('app.sel') }}?page={{ paginate.prev_num }}" >上一页</a>
    {% endif %}
	页码
    {% for i in paginate.iter_pages() %}
        <a href="{{ url_for('app.sel') }}?page={{ i }}" >{{ i }}</a>
    {% endfor %}

    {% if paginate.has_next %}
        <a href="{{ url_for('app.sel') }}?page={{ paginate.next_num }}" >下一页</a>
    {% endif %}



</body>
</html>
```



![page](..\pictures\page.png)



**与,或,非**

```python
 # 例子,查询性别为男的,且姓名中包含'小'的学生信息
    # stus = Student.query.filter(Student.gender==1).filter(Student.s_name.contains('小')).all()
    stus = Student.query.filter(Student.gender==1, Student.s_name.contains('小')).all()

    # and_且,not_非,or_或
    stus = Student.query.filter(and_(Student.gender==1,
                                     Student.s_name.contains('小'))).all()
    # 例子:查询性别为男,或姓名包含'小'的学生信息
    stus = Student.query.filter(or_(Student.gender==1,
                                    Student.s_name.contains('小'))).all()
    # 例子:查询性别不为男,且名中包含'小'的学生信息
    stus = Student.query.filter(and_(not_(Student.gender==1)),Student.s_name.contains('小')).all()

    stus_names = [stu.s_name for stu in stus]
    return str(stus_names)
```



## 一对多(1:N)

  外键定义在多(N)的一方,relationship关联关系定义在一(1)的一方

```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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

注意：表的外键由db.ForeignKey指定，传入的参数是表的字段。db.relations它声明的属性不作为表字段，第一个参数是关联类的名字，backref是一个反向身份的代理,相当于在Student类中添加了stu的属性。例如，有Grade实例dept和Student实例stu。dept.students.count()将会返回学院学生人数;stu.stu.first()将会返回学生的学院信息的Grade类实例。一般来讲db.relationship()会放在一这一边。