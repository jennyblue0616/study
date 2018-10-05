```
jQuery
  jQuery 是一个 JavaScript 库,极大地简化了 JavaScript 编程。
  write less do more
  jQuery 的功能概括:解决了浏览器兼容性问题,封装了常用的操作
引入jQuery
  1.使用自己项目中的jQuery.min.js
  2.使用CDN服务器上的jQuery文件
  通过网站www.bootcdn.cn下载jQuery,保存到网页的同一目录下,就可以使用

$函数的四种用法
  1.$函数的参数是一个函数-传入的函数是页面加载完成之后执行的回调函数
  2.$函数的参数是选择器字符串-获取页面上的标签并且转成jQuery对象
  为什么要获取jQuery对象-因为jQuery对象有更多封装好的方法可供调用
  绑定/反绑定事件:on()/off()/one()
  获取/修改标签内容:text()/html() 有参数是修改,没有是获取
  获取/修改标签属性:attr(name,value)
  添加子节点:append后面()/prepend前面()
  删除/清空节点:remove()/empty()
  修改样式表:css({'color':'red','font-size':'18px'})修改多组样式
  获取父节点:parent()
  获取子节点:children()
  获取兄弟节点:prev()/next()
  3.$函数的参数是标签字符串-创建标签(加尖括号)并且返回对应的jQuery对象
  4.$函数的参数是原生JS对象-将原生JS对象转换成jQuery对象
  
jQuery 选择器
$("*")	选取所有元素
$("ul li:first-child")	选取每个 <ul> 元素的第一个 <li> 元素
$("[href]")	选取带有 href 属性的元素
$("a[target='_blank']")	选取所有 target 属性值等于 "_blank" 的 <a> 元素
div p 是div包含p
div>p 父级是div的p
div+p div和p紧挨着
div,p 二者并列
```

```
AJAX
AJAX 是与服务器交换数据的技术，它在不重载全部页面的情况下，实现了对部分网页的更新。
Asynchronous-异步请求(没有中断浏览器的用户体验)
Javascript
And
XML-extensible markup language
异步请求拿到的数据是JSON---->通过DOM操作对页面进行局部刷新
异步加载数据 + 局部刷新页面
API应用程序编程接口appliciation programming interface

$.getJSON(url,function(jsonObj){})
jsonObj是一个json对象,jsonObj浏览器给的
回调函数不会自己调,别人会调
function(){}里写返回数据后要做的操作
jsonObj相当于evt

HTTP响应状态码
2xx成功
3xx重定向 
401未授权
403被禁用
405请求方式不对
5xx服务器出问题
```

