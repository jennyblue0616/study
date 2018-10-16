JavaScript



```
JavaScript = ECMAScript + BOM +DOM

BOM-浏览器对象模型-window

DOM-文档对象模型-document

1.显示数据

a.  window.alert()
b.  document.write()
如果在文档已完成加载后执行 document.write，整个 HTML 页面将被覆盖。
c.  innerHTML写入HTML元素
d.  console.log()

2.对象
JS对象是拥有属性和方法的数据,JS对象是变量的容器,是属性和方法的容器

3.作用域
作用域为可访问的变量,对象,函数的集合

HTML DOM(文档对象模型)

- JavaScript 能够改变页面中的所有 HTML 元素
- JavaScript 能够改变页面中的所有 HTML 属性
- JavaScript 能够改变页面中的所有 CSS 样式
- JavaScript 能够对页面中的所有事件做出反应

通常，通过 JavaScript，需要操作 HTML 元素,必须首先找到该元素。有五种方法来做这件事：

4.获取元素
- 通过 id 找到 HTML 元素  document.getElementById
- 通过标签名找到 HTML 元素 document.getElementsByTagName
- 通过类名找到 HTML 元素   document.getElementsByClassName
- 返回匹配的指定 CSS 选择器的一个元素document.querySelector() - 返回文档中匹配的CSS选择器的所有元素节点列表         		  
     document.querySelectorAll() 返回 NodeList 对象。
     NodeList对象表示节点的集合,可以通过索引访问，索引值从0开始。
元素访问子节点-children
元素访问父节点-parentNode
元素访问兄弟节点-previousSibling/nextSibling

5.操作元素
  改变HTML的内容-元素.innerHTML,元素.textContent

  改变HTML的属性-元素.attribute
例:image.src="新图片的名字"  更改图片

  改变HTML的样式-元素.style.具体样式(如color)
  style属性只能写不能读,读样式通过currentStyle,读出来的值带px
  
   删除元素style.display = "none"
          style.visibility = "hidden"
   创造一个标签:document.createElement(),createTextNode() 
   
6.JS中的事件处理
- (1)在标签上使用on...属性来进行事件绑定
- (2)通过代码获取标签绑定on...属性
- (3)通过代码获取标签然后使用addEventListener() 方法
  addEventListener() 方法用于向指定元素添加事件句柄,添加的事件句柄不会覆盖已存在的事件句柄,可以向一个元素添加多个事件句柄,可以向同个元素添加多个同类型的事件句柄，如：两个 "click" 事件。
  可以向任何 DOM 对象添加事件监听，不仅仅是 HTML 元素。如： window 对象。
  当你使用 addEventListener() 方法时, JavaScript 从 HTML 标记中分离开来，可读性更强， 在没有控制HTML标记时也可以添加事件监听。
  可以使用 removeEventListener() 方法来移除事件的监听。
  语法

  element.addEventListener(event, function, useCapture);
第一个参数是事件的类型 (如 "click" 或 "mousedown").

第二个参数是事件触发后调用的函数。
- 绑定事件监听器的函数都需要传入事件的回调函数
- 程序员知道事件发生的时候需要做什么样的处理,但是不知道事件什么时候发生
- 所以传入一个函数在将来发生事件的时候由系统进行调用 ,这种函数就称为回调函数
- 回调函数的第一个参数代表事件对象(封装了所有和事件相关的信息) 对于低版本的IE 通过window.event来获取事件对象

-事件对象的属性和方法:
 - target/srcElement - 事件源(引发事件的标签)
 - preventDefault()/returnValue = False(IE)
 - 阻止事件默认行为

第三个参数是个布尔值用于描述事件是冒泡还是捕获。该参数是可选的。默认值为 false, 即冒泡传递，当值为 true 时, 事件使用捕获传递。

  事件传递有两种方式：冒泡与捕获。
事件传递定义了元素事件触发的顺序。在 冒泡 中，内部元素的事件会先被触发，然后再触发外部元素，即从里向外.
  在 捕获 中，外部元素的事件会先被触发，然后才会触发内部元素的事件，即从外向里。
  如果要阻止事件的传播行为(阻止事件冒泡)可以使用stopPropagation()  /  cancelBubble = true  (IE)


7.添加/删除元素 
  在文档中添加元素用 父.appendChild(子) 方法
  它用于添加新元素到尾部。如果我们需要将新元素添加到开始位置，可以使用 insertBefore() 方法.
  父.insertBefore(子,父.firstChild)
   
  在文档中删除元素用父.removeChild(子)
  
  在文档中替换元素用父.replaceChild(替换元素,被替换元素)
   
   
```



```
 浏览器对象模型 (BOM)
  浏览器对象模型 (Browser Object Model (BOM)) 使 JavaScript 有能力与浏览器"对话"。
  可以在JS中创建三种消息框:警告框,确认框,提示框.
  警告框:window.alert()
  确认框:window.confirm()
  提示框:window.prompt() 用于提示用户在进入页面前输入某个值
  
  (1)window.screen对象包含有关用户屏幕的信息
screen.availWidth - 可用的屏幕宽度
screen.availHeight - 可用的屏幕高度
  (2)window.location对象用于获得当前页面的地址(URL),并把浏览器重定向到新的页面。
location.hostname 返回 web 主机的域名
location.pathname 返回当前页面的路径和文件名
location.port 返回 web 主机的端口 （80 或 443）
location.protocol 返回所使用的 web 协议（http:// 或 https://）
location.href 属性返回当前页面的 URL。
  (3)window.history对象包含浏览器的历史
history.back() - 与在浏览器点击后退按钮相同
history.forward() - 与在浏览器中点击向前按钮相同
  (4)window.navigator 对象包含有关访问者浏览器的信息。
浏览器代号: navigator.appCodeName 
浏览器名称: navigator.appName
浏览器版本: navigator.appVersion 
启用Cookies: navigator.cookieEnabled 
硬件平台: navigator.platform 
用户代理: navigator.userAgent 
用户代理语言: navigator.systemLanguage 

计时器
setInterval() - 间隔指定的毫秒数不停地执行指定的代码
setTimeout() - 在指定的毫秒数后执行指定代码
clearInterval() 方法用于停止 setInterval() 方法执行的函数代码。
clearTimeout() 方法用于停止执行setTimeout()方法的函数代码。
```
跑马灯
```
<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<title></title>
		<style>
			h1 {
				font-size: 36px;
				background-color: lightgoldenrodyellow;
				color: darkolivegreen;
				width: 960px;
				margin: 0 auto;
			}
		</style>
	</head>
	<body>
		<h1 id="welcome" class="foo">欢迎来到千锋教育成都校区Python就业班▁▂▃▄▅▆▇▆▅▄▃▂▁</h1>
		<script>
			var h1= document.querySelectorAll(".foo")[0];
			// var h1 = document.querySelector(".foo");
			// var h1 = document.getElementsByClassName("foo")[0];
			// var h1 = document.getElementsByTagName("h1")[0];
			// var h1 = document.getElementById("welcome")
			function move() {
				var str = h1.textContent;
				str = str.substring(1) + str.charAt(0);
				h1.textContent = str;
			}
			window.setInterval(move, 200);
		</script>
	</body>
</html>


```
日历时间
```
<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<title></title>
		<style>
			#time {
				float: right;
				background-color: blue;
				color: yellow;
				width: 320px;
				height: 40px;
				font: 20px/40px Arial;
				text-align: center;
			}
		</style>
	</head>
	<body>
		<h1>H<sub>2</sub>O</h1>
		<div id="time"></div>
		<script type="text/javascript">
			var days = ["日", "一", "二", "三", "四", "五", "六"];
			
			function showTime() {
				var now = new Date();
				var year = now.getFullYear();
				var month = now.getMonth() + 1;
				var date = now.getDate();
				var hour = now.getHours();
				var minute = now.getMinutes();
				var second = now.getSeconds();
				var day = now.getDay();
				var div = document.getElementById("time");
				div.innerHTML = year + "年" 
					+ (month < 10 ? "0" : "") + month + "月" 
					+ (date < 10 ? "0" : "") + date + "日&nbsp;&nbsp;"
					+ (hour < 10 ? "0" : "") + hour + ":"
					+ (minute < 10 ? "0" : "") + minute + ":" 
					+ (second < 10 ? "0" : "") + second 
					+ "&nbsp;&nbsp;星期" + days[day];
			}
			showTime();
			window.setInterval(showTime, 1000);
		</script>
	</body>
</html>

```
跳转百度
```
<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<title></title>
	</head>
	<body>
		<h2><span id="counter">5</span>秒钟以后自动跳转到百度...</h2>
		<script type="text/javascript">
			var countdown = 5;
			var span = document.getElementById("counter");
			function delayGo() {
				countdown -= 1;
				if (countdown == 0) {
					// window.location - 浏览器地址栏
					// window.document - 文档对象
					// window.history - 历史记录
					// window.navigator - 浏览器
					// window.screen - 屏幕
					location.href = "http://www.baidu.com";
				} else {
					span.textContent = countdown;
					setTimeout(delayGo, 1000);
				}
			}
			setTimeout(delayGo, 1000);
		</script>
	</body>
</html>


```
