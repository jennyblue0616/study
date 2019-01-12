---
author:于梦娇
title:django9
---

# django9



1. 在models.py文件中

```python
from django.db import models

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=20)
    desc = models.CharField(max_length=150)
    img = models.ImageField(upload_to='article')
    create_time = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=0)

    class Meta:
        db_table = 'article'
```

2. 在app应用下urls.py文件中

```python
from django.conf.urls import url
from rest_framework.routers import SimpleRouter

from app import views

#获取路由对象
router = SimpleRouter()
# 不是视图函数,是类,路由注册一个url地址,访问url地址,调类
#127.0.0.1:8080/app/article/[id]/
router.register('article', views.ArticleView)

urlpatterns = [
    # 返回页面
    url(r'^all_article/', views.all_article)
]
# 设置访问路由地址
urlpatterns += router.urls

```

3. 在views.py文件中

```python
from django.shortcuts import render
from rest_framework import mixins, viewsets
from rest_framework.response import Response

from app.models import Article
from app.serializers import ArticleSerializer


class ArticleView(viewsets.GenericViewSet,
                  mixins.ListModelMixin,(查询所有的值)
                  mixins.DestroyModelMixin,(删除)
                  mixins.UpdateModelMixin,(更新)
                  mixins.RetrieveModelMixin,(查询具体的值)
                  mixins.CreateModelMixin):(新建)

    # 重构删除方法,软删除
    def perform_destroy(self, instance):
        instance.is_delete = 1
        instance.save()


    # 查询数据
    queryset = Article.objects.filter(is_delete=0)
    # 序列化
    serializer_class = ArticleSerializer


def all_article(request):
    if request.method == 'GET':
        return render(request, 'article.html')

```

4. 在app文件夹下新建一个serializers.py文件

```python
# 写序列化

from rest_framework import serializers

from app.models import Article


class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        # 指定序列化的模型
        model = Article
        # 序列化字段
        fields = ['id', 'title', 'desc']

```

5. 在article.html中,写ajax请求

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>文章列表页面</title>
    <script src="https://code.jquery.com/jquery-3.1.1.min.js" ></script>
    <script type="text/javascript" >
        $.ajax({
            url:'/app/article/',
            type:'GET',
            dataType:'json',
            success:function(data){
                var table_html = '<table><thead><th>id</th><th>title</th><th>操作</th></thead><tbody>'

                for(var i=0; i<data.length; i++){
                    table_html += '<tr><td>'+data[i].id
                    table_html += '</td><td>'+data[i].title
                    table_html += '</td><td><a onclick="add_article();">创建</a>'
                    table_html += '   <a  onclick="delete_article(' + data[i].id +');">删除</a>'
                    table_html += '</td></tr>'


                }
                table_html += '</tbody></table>'
                $('.art_class').html(table_html)
            },
            error:function(data){
                alert('请求失败')
            }
        })

        function delete_article(id){
            $.ajax({
                url:'/app/article/'+id+'/',
                type:'DELETE',
                dataType:'json',
                success:function(data){
                    alert('删除成功')
                },
                error:function(data){
                    alert('删除失败')
                }
            })

        }


        function add_article(){
            var form_html = '<form action="">'
            form_html += "{% csrf_token %}"
            form_html += '标题:<input type="text" name="title">'
            form_html += '描述:<input type="text" name="desc">'
            form_html += '<input type="button" value="提交" onclick="add();">'
            form_html += '</form>'
            $('.add_class').html(form_html)
        }

        function add(){
            var title = $('input[name="title"]').val()
            var desc = $('input[name="desc"]').val()
            var csrf = $('input[name="csrfmiddlewaretoken"]').val()

            $.ajax({
                url:'/app/article/',
                type:'POST',
                data:{'title':title, 'desc':desc},
                headers:{'X-CSRFToken':csrf},
                dataType:'json',
                success:function(data){
                    alert('创建成功')

                },
                error:function(data){
                    alert('创建失败')
                }
            })
        }
    </script>
</head>
<body>
    <div class="art_class"></div>
    <div class="add_class"></div>
</body>
</html>
```

HTTP请求方式

- GET:获取数据
- POST:创建数据
- PUT:修改数据(修改全部属性)
- PATCH:修改数据(修改部分属性)
- DELETE:删除

```
阿贾克斯
常规
$.ajax({
    url:'127.0.0.1:8080/app/article',
    type:'POST',
    data:{'title':'coco','desc':'123456'},
    dataType:'json',
    #data是后端返回给前端的
    success: function(data){
       
    },
    error:function(data){
    }
})
简略
  $.get(url, function(data){})
  
  $.post(url, data, function(data){
  #成功的回调函数})
```

