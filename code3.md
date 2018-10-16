



```
<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<title></title>
	</head>
	<body>
		<h1>Hello, world!</h1>
		<!--
        	Write Less Do More
        	1. 解决了浏览器兼容性问题
        	2. 封装了常用操作用更少的代码做更多的事情
        	引入jQuery
        	1. 使用自己项目中的jquery.min.js
        	2. 使用CDN服务器上的jQuery文件
        	如何使用jQuery
        	window.jQuery属性 === $
        -->
		<!--<script src="https://cdn.bootcss.com/jquery/1.12.4/jquery.min.js"></script>-->
		<script src="js/jquery.min.js"></script>
		<script>
			$(function() { 
				$("h1").on("click", function() { 
					$("h1").fadeOut(2000); 
				});
			});
		</script>
	</body>
</html>
```





`jquery`

水果标签

```
<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<title></title>
		<style>
			* {
				margin: 0;
				padding: 0;
			}
			#container {
				margin: 20px 50px;
			}
			#fruits li {
				list-style: none;
				width: 200px;
				height: 50px;
				font-size: 20px;
				line-height: 50px;
				background-color: cadetblue;
				color: white;
				text-align: center;
				margin: 2px 0;
			}
			#fruits>li>a {
				float: right;
				text-decoration: none;
				color: white;
				position: relative;
				right: 5px;
			}
			#fruits~input {
				border: none;
				outline: none;
				font-size: 18px;
			}
			#fruits~input[type=text] {
				border-bottom: 1px solid darkgray;
				width: 200px;
				height: 50px;
				text-align: center;
			}
			#fruits~input[type=button] {
				width: 80px;
				height: 30px;
				background-color: coral;
				color: white;
				vertical-align: bottom;
				cursor: pointer;
			}
		</style>
	</head>
	<body>
		<div id="container">
			<ul id="fruits">
				<li>苹果<a href="javascript:void(0);">×</a></li>
				<li>香蕉<a href="javascript:void(0);">×</a></li>
				<li>火龙果<a href="javascript:void(0);">×</a></li>
				<li>西瓜<a href="javascript:void(0);">×</a></li>
			</ul>
			<input type="text" name="fruit">
			<input id="ok" type="button" value="确定">
		</div>
		<script src="js/jquery.min.js"></script>
		<script>
			// JavaScript是动态语言
			// 动态语言判定对象的类型用的是鸭子判定法(duck typing)
			// 伪数组
			var foo = {
				"length": 3,
				"0": "hello",
				"1": "goodbye",
				"2": "welcome"
			};
			for (var i = 0; i < foo.length; i += 1) {
				alert(foo[i]);
			}
			// jQuery对象的本质是一个伪数组
			// 	  - 有length属性
			//	  - 可以通过下标获取数据
			// $函数的四种用法:
			// 1. $函数的参数是一个函数 - 传入的函数是页面加载完成之后要执行的回调函数
			// 2. $函数的参数是选择器字符串 - 获取页面上的标签而且转成jQuery对象
			//	为什么要获取jQuery对象 - 因为jQuery对象有更多的封装好的方法可供调用
			//	  - 绑定/反绑定事件: on() / off() / one() 
			//	  - 获取/修改标签内容: text() / html()
			//	  - 获取/修改标签属性: attr(name, value)
			//	  - 添加子节点: append() / prepend()
			//	  - 删除/清空节点: remove() / empty()
			//	  - 修改样式表: css({'color': 'red', 'font-size': '18px'})
			//	  - 获取父节点: parent()
			//	  - 获取子节点: children()
			//	  - 获取兄弟节点: prev() / next()
			// 3. $函数的参数是标签字符串 - 创建标签并且返回对应的jQuery对象
			// 4. $函数的参数是原生JS对象 - 将原生JS对象转换成jQuery对象
			//	  - 如果bar是一个jQuery对象 可以通过bar[0] / bar.get(0)
			$(function() {
				function deleteItem(evt) {
					$(evt.target).parent().remove();
				}
				
				$("#fruits a").on("click", deleteItem);
				$("#ok").on("click", function() {
					var fruitName = $("#container input[type=text]").val().trim();
					if (fruitName.length > 0) {
						$("#fruits").prepend(
							$("<li>").text(fruitName).append(
								$("<a>").text("×").attr("href", "javascript:void(0);")
									.on("click", deleteItem)
							)
						);
					}
				});
			});
		</script>
	</body>
</html>
```



变色盒子

```
<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<title></title>
		<style>
			#container {
				width: 800px;
				height: 400px;
				margin: 10px auto;
				border: 1px solid black;
				overflow: hidden;
			}
			#buttons {
				width: 800px;
				margin: 10px auto;
				text-align: center;
			}
			#add, #fla {
				border: none;
				outline: none;
				width: 80px;
				height: 30px;
				background-color: red;
				color: white;
				font-size: 16px;
				line-height: 30px;
				cursor: pointer;
			}
		</style>
	</head>
	<body>
		<div id="container"></div>
		<div id="buttons">
			<button id="add">添加</button>
			<button id="fla">闪烁</button>
		</div>
		<script src="js/mylib.js"></script>
		<script src="js/jquery.min.js"></script>
		<script>
			$(function() {
				$("#add").on("click", function() {
					$("#container").append($("<div>").css({
						"width": "80px",
						"height": "80px",
						"float": "left",
						"background-color": randomColor()
					}));
				});
				$("#fla").on("click", function() {
					setInterval(function() {
						$("#container>div").each(function() {
							$(this).css("background-color", randomColor());
						});
					}, 200);
				});
			});
		</script>
	</body>
</html>
```



表格

```
<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<title></title>
		<style>
			#data {
				border-collapse: collapse;
			}
			#data td, #data th {
				width: 120px;
				height: 40px;
				text-align: center;
				border: 1px solid black;
			}
			#buttons {
				margin: 10px 0;
			}
		</style>
	</head>
	<body>
		<table id="data">
			<caption>数据统计表</caption>
			<tr>
				<th>姓名</th>
				<th>年龄</th>
				<th>性别</th>
				<th>身高</th>
				<th>体重</th>
			</tr>
			<tr>
				<td>Item1</td>
				<td>Item2</td>
				<td>Item3</td>
				<td>Item4</td>
				<td>Item5</td>
			</tr>
			<tr>
				<td>Item1</td>
				<td>Item2</td>
				<td>Item3</td>
				<td>Item4</td>
				<td>Item5</td>
			</tr>
			<tr>
				<td>Item1</td>
				<td>Item2</td>
				<td>Item3</td>
				<td>Item4</td>
				<td>Item5</td>
			</tr>
			<tr>
				<td>Item1</td>
				<td>Item2</td>
				<td>Item3</td>
				<td>Item4</td>
				<td>Item5</td>
			</tr>
			<tr>
				<td>Item1</td>
				<td>Item2</td>
				<td><a>Item3</a></td>
				<td>Item4</td>
				<td>Item5</td>
			</tr>
			<tr>
				<td>Item1</td>
				<td>Item2</td>
				<td>Item3</td>
				<td>Item4</td>
				<td><a>Item5</a></td>
			</tr>
		</table>
		<div id="buttons">
			<button id="pretty">美化表格</button>
			<button id="clear">清除数据</button>
			<button id="remove">删单元格</button>
			<button id="hide">隐藏表格</button>
		</div>
		<script src="js/jquery.min.js"></script>
		<script>
			$(function() {
				$("#pretty").on("click", function() {
					$("#data tr:gt(0):odd").css("background-color", "lightcyan");
					$("#data tr:gt(0):even").css("background-color", "lightpink");
				});
				$("#clear").on("click", function() {
					$("#data tr:gt(0) td").empty();
				});
				$("#remove").on("click", function() {
					$("#data tr:gt(0):last-child").remove();
				});
				$("#hide").on("click", function() {
					if (this.isHidden) {
						$("#data").show();
						this.isHidden = false;
						$(this).text("隐藏表格");
					} else {
						$("#data").hide();
						this.isHidden = true;
						$(this).text("显示表格");
					}
				});
			});
		</script>
	</body>
</html>
```



JavaScript创建对象的构造器语法

```
<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<title></title>
	</head>
	<body>
		<script>
			// JavaScript创建对象的构造器语法
			function Student(name, age) {
				this.name = name;
				this.age = age;
			}
			// 对象方法绑定在类型的prototype上
			Student.prototype.study = function(courseName) {
				alert(this.name + "正在学习" + courseName);
			};
			// 静态方法直接绑定在类型上
			Student.sayHello = function() {
				alert("大家好");
			};
			// 创建对象使用 - new+构造器函数
			var obj = new Student("骆昊", 38);
			obj.study("Linux操作系统");
			Student.sayHello();
			
			// JSON - JavaScript Object Notation
			// JSON是JavaScript中创建对象的字面量语法
			// 现在被广泛的应用于数据的存储和交换
			/*
			var obj = {
				"name": "骆昊",
				"age": 38,
				"study": function(courseName) {
					alert(this.name + "正在学习" + courseName);
				},
				"watchAv": function() {
					if (this.age < 18) {
						alert(this.name + "建议你观看《熊出没》.");
					} else {
						alert(this.name + "正在观看岛国片.");
					}
				}
			};
			obj.study("HTML");
			*/
			/*
			var obj = new Object();
			obj.name = "骆昊";
			obj.age = 15;
			obj.study = function(courseName) {
				alert(this.name + "正在学习" + courseName);
			};
			obj.watchAv = function() {
				if (this.age < 18) {
					alert(this.name + "建议你观看《熊出没》.");
				} else {
					alert(this.name + "正在观看岛国片.");
				}
			}
			
			obj.study("Python");
			obj.watchAv();
			*/
		</script>
	</body>
</html>
```

`ajax`



```
<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<title></title>
	</head>
	<body>
		<button id="load">加载</button>
		<script>
			var loadBtn = document.getElementById("load");
			loadBtn.addEventListener("click", function() {
				var xhr = new XMLHttpRequest();
				if (xhr) {
					var url = "http://api.tianapi.com/meinv/?key=772a81a51ae5c780251b1f98ea431b84&num=10";
					xhr.open("get", url, true);
					xhr.onreadystatechange = function() {
						if (xhr.readyState == 4) {
							if (xhr.status == 200) {
								var jsonObj = JSON.parse(xhr.responseText);
								if (jsonObj.code == 200) {
									for (var i = 0; i < jsonObj.newslist.length; i += 1) {
										var mm = jsonObj.newslist[i];
										var img = document.createElement("img");
										img.src = mm.picUrl;
										img.width = 300;
										document.body.insertBefore(img, loadBtn);
									}
								}
							}
						}
					};
					xhr.send();
				} else {
					alert("请不要使用垃圾浏览器!!!");
				}
			});
		</script>
	</body>
</html>
```

美女图片

```
<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<title></title>
		<style>
			#mm li {
				list-style: circle;
			}
		</style>
	</head>
	<body>
		<button id="load">换一组</button>
		<ul id="mm"></ul>
		<script src="js/jquery.min.js"></script>
		<script>
			$(function() {
				$("#load").on("click", function(evt) {
					var url = "http://api.tianapi.com/meinv/?key=772a81a51ae5c780251b1f98ea431b84&num=20";
					$.getJSON(url, function(jsonObj) {
						$("#mm").empty();
						for (var i = 0; i < jsonObj.newslist.length; i += 1) {
							$("#mm").append(
								$("<li>").append(
									$("<a target='_blank'>")
										.text(jsonObj.newslist[i].title)
										.attr("href", jsonObj.newslist[i].picUrl)
								)
							);
						}
					});
				});
			});
		</script>
	</body>
</html>
```

周公解梦

```
<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<title></title>
		<style>
			#container {
				width: 400px;
				margin: 0 auto;
				padding-top: 200px;
				text-align: center;
			}
			#container input {
				font-size: 22px;
				line-height: 30px;
				height: 30px;
			}
			#container input[type=text] {
				width: 300px;
				border: 1px solid black;
			}
			#container input[type=button] {
				color: white;
				background-color: red;
				width: 80px;
				border: none;
			}
			#result {
				width: 400px;
				margin: 10px auto;
				font-size: 18px;
			}
		</style>
	</head>
	<body>
		<div id="container">
			<input type="text">
			<input type="button" value="查询">
		</div>
		<hr>
		<p id="result"></p>
		<script src="js/jquery.min.js"></script>
		<script>
			$(function() {
				$("#container input[type=button]").on("click", function() {
					var keyword = $("#container input[type=text]").val().trim();
					if (keyword.length > 0) {
						var url = "http://api.tianapi.com/txapi/dream/"; 
						$.ajax({
							"url": url,
							"type": "get",
							"data": {
								"key": "772a81a51ae5c780251b1f98ea431b84",
								"word": keyword,
							},
							"dataType": "json",
							"success": function(jsonObj) {
								if (jsonObj.code == 250) {
									$("#result").text(jsonObj.msg);
								} else {
									$("#result").text(jsonObj.newslist[0].result);
								}
							}
						});
					}
				});
			});
		</script>
	</body>
</html>
```

