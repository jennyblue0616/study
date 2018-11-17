---
author:于梦娇
title:flask05
---

## flask05

### 文件上传

#### 1.模板定义

注意上传的表单中一定要添加enctype="multipart/form-data"参数,定义type='file'。

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <form action="" method="post" enctype="multipart/form-data">
        上传图片:<input type="file" name="img" >
        <input type="submit" value="提交">
    </form>
</body>
</html>
```

#### 2.图片保存

  views.py文件中,图片保存通过request.files获取页面中上传的图片,并调用save(path)方法进行保存。

```python
@blueprint.route('/upload/', methods=['GET', 'POST'])
def up_img():
    if request.method == 'GET':
        return render_template('upload.html')
    if request.method == 'POST':
        # 实现保存图片
        # 1.获取图片
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        MEDIA_ROOT = os.path.join(os.path.join(BASE_DIR, 'static'), 'media')
        upload_img = request.files.get('img')
        # 2.保存图片到文件夹中
        # D:wordspace/flask/day05/static/media/xxx
        path = os.path.join(MEDIA_ROOT, upload_img.filename)
        upload_img.save(path)

        # 3.保存图片到数据库中
        up_img = UploadImg()
        upload_path = upload_img.filename
        up_img.img = upload_path
        db.session.add(up_img)
        db.session.commit()
        return render_template('img.html', up_img=up_img)
```

#### 3.图片渲染

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <img src="/static/media/{{ up_img.img }}" >
</body>
</html>
```

### 邮箱发送



manage.py文件中

```python
from flask import Flask
from flask_script import Manager

from app.views import blueprint
from utils.config import Config
from utils.functions import init_ext

app = Flask(__name__)
app.register_blueprint(blueprint=blueprint, url_prefix='/app')

app.secret_key = 'jdhfkjlhgliufhkj'

# 配置config文件
app.config.from_object(Config)

#初始化第三方库
init_ext(app)

manage = Manager(app)

if __name__ == '__main__':
    manage.run()

```



function.py文件中

```python
from flask_mail import Mail

from app.models import db

mail = Mail()


def init_ext(app):
    mail.init_app(app)
    db.init_app(app)


def get_mysql_database(database):

    return '{}+{}://{}:{}@{}:{}/{}'.format(database['DIALECT'],
                                           database['DRIVER'],
                                           database['USER'],
                                           database['PASSWORD'],
                                           database['HOST'],
                                           database['PORT'],
                                           database['DB'])
```



在views.py文件中

```python
@blueprint.route('/send_email/')
def send_email():
    msg = Message("hello",
                  sender="522495731@qq.com",
                  recipients=["522495731@qq.com"])
    msg.body = "testing"

    mail.send(msg)
    return '发送成功'
# 通过邮箱确认账号启动
# 思路:
# 1.注册时,指定接收激活账号的邮箱地址.注册后,发送激活邮件到指定邮箱(刚注册的账号是禁用状态)
# 2.激活账号.点击邮件中的链接即可激活
# 3.实现激活.邮箱用的激活地址URL中需要有一个参数,用于指定需要激活的账号
# 比如:http://xxx.com/activate?username="小明"
# 比如:http://xxx.com/activate?ticket=dfhjkdhjkhx 随机字符串
# 表字段: username, password, status, ticket
# 从url中接收ticket字符串,从数据库中查对应的用户,改状态

# restframework提供接口
# vue框架
# 微服务,消息发送微服务,
```

config.py文件中



```python
from utils.functions import get_mysql_database
from utils.settings import DATABASES



class Config():
    SQLALCHEMY_DATABASE_URI = get_mysql_database(DATABASES)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = "smtp.qq.com"
    # MAIL_PORT = 587  # 设置邮箱端口为465，默认为25，由于阿里云禁止了25端口，所以需要修改
    # MAIL_USE_SSL = True  # 163邮箱需要开启SSL
    MAIL_USERNAME = "522495731@qq.com"
    MAIL_PASSWORD = "rofbbklpfezwcafc"

```

settings.py

```python
DATABASES = {
    'USER': 'root',
    'PASSWORD': '123456',
    'HOST': '127.0.0.1',
    'PORT': '3306',
    'DB': 'flask6',
    'DIALECT': 'mysql',
    'DRIVER': 'pymysql'
}
```

