按钮

```
<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<title></title>
	</head>
	<body>
		<div id="buttons">
			<button>Button1</button>
			<button>Button2</button>
			<button>Button3</button>
			<button>Button4</button>
			<button>Button5</button>
		</div>
		<script src="js/mylib.js"></script>
		<script type="text/javascript">
			// var buttons = document.getElementById("buttons").children;
			var buttons = document.querySelectorAll("#buttons>button");
			for (var i = 0; i < buttons.length; i += 1) {
				// 如果希望在事件回调函数中获得事件源(引发事件的标签)
				// 应该通过事件对象的target属性去获取事件源
				bind(buttons[i], "click", function(evt) {
					evt = evt || window.event;
					evt.target = evt.target || evt.srcElement;
					evt.target.innerHTML = "欧耶";
				});
			}
		</script>
	</body>
</html>

```

```
<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<title></title>
	</head>
	<body>
		<button id="button1">按钮1</button>
		<script src="js/mylib.js"></script>
		<script>
			var button1 = document.getElementById("button1");
			// 绑定事件的回调函数(callback function)
			// 你知道事件发生的时候要做什么但不知道事件什么时候发生
			// 这个时候都是通过绑定回调函数将来由其他地方来调用该函数
			bind(button1, "click", sayHello);
			bind(button1, "click", sayGoodbye);
			bind(button1, "click", function() {
				unbind(button1, "click", sayHello);
			});
			
			function sayHello() {
				alert("你好呀!");
			}
			
			function sayGoodbye() {
				alert("下次再见!");
			}
		</script>
	</body>
</html>


```

阻止跳转百度 preventDefault

```
<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<title></title>
	</head>
	<body>
		<a id="about" href="http://www.baidu.com">关于</a>
		<script src="js/mylib.js"></script>
		<script>
			var a = document.getElementById("about");
			bind(a, "click", function(evt) {
				evt = evt || window.event;
				if (evt.preventDefault) {
					evt.preventDefault();
				} else {
					evt.returnValue = false;
				}
				console.log("Hello, world!");
			});
		</script>
	</body>
</html>

```

捕获

```
<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<title></title>
		<style>
			#one {
				width: 400px;
				height: 400px;
				background-color: red;
			}
			#two {
				width: 300px;
				height: 300px;
				background-color: green;
			}
			#three {
				width: 200px;
				height: 200px;
				background-color: blue;
			}
			#two, #three {
				position: relative;
				left: 50px;
				top: 50px;
			}
		</style>
	</head>
	<body>
		<div id="one">
			<div id="two">
				<div id="three"></div>
			</div>
		</div>
		<script src="js/mylib.js"></script>
		<script>
			bind(document.body, "click", function() {
				alert("I am body!");
			});
			
			var one = document.getElementById("one");
			bind(one, "click", function(evt) {
				alert("I am one!");
				evt = evt || window.event;
			});
			
			var two = document.getElementById("two");
			bind(two, "click", function() {
				alert("I am two!");
			});
			
			var three = document.getElementById("three");
			bind(three, "click", function(evt) {
				alert("I am three!");
				evt = evt || window.event;
				if (evt.stopPropagation) {
					evt.stopPropagation();
				} else {
					evt.cancelBubble = true;
				}
			});
		</script>
	</body>
</html>


```

猜数字

```
<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<title></title>
		<style type="text/css">
			#num, #ok, #hint {
				font-size: 22px;
			}
			#num, #ok {
				width: 80px;
				vertical-align: middle;
			}
			#ok {
				height: 30px;
				line-height: 30px;
				background-color: red;
				color: white;
				border: none;
				outline: none;
				cursor: pointer;
			}
		</style>
	</head>
	<body>
		<input id="num" type="number">
		<input id="ok" type="button" value="确定">
		<p id="hint"></p>
		<script src="js/mylib.js"></script>
		<script>
			var answer = parseInt(Math.random() * 100 + 1);
			var okBtn = document.getElementById("ok");
			var numInput = document.getElementById("num");
			var hintPara = document.getElementById("hint");
			
			function guess() {
				var thyAnswer = parseInt(numInput.value);
				if(numInput.value == thyAnswer) {
					var hint = "你猜的是" + thyAnswer + ". ";
					if (thyAnswer > answer) {
						hint += "小一点";
					} else if (thyAnswer < answer) {
						hint += "大一点";
					} else {
						hint += "恭喜你猜对了!";
						okBtn.disabled = true;
						numInput.disabled = true;
					}
					hintPara.innerHTML += hint + "<br>";
				} else {
					alert("你是猴子派来的逗比吗!?");
				}
				numInput.value = "";
				numInput.focus();
			}
			
			bind(okBtn, "click", guess);
			bind(numInput, "keydown", function(evt) {
				evt = evt || window.event;
				console.log(evt.keyCode);
				console.log(evt.which);
				if (evt.keyCode == 13 || evt.which == 13) {
					guess();
				}
			});
		</script>
	</body>
</html>


```

作业1-轮播图片

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
			#adv {
				width: 940px;
				margin: 0 auto;
			}
			#adv ul {
				width: 120px;
				height: 30px;
				margin: 0 auto;
				position: relative;
				top: -30px;
			}
			#adv li {
				width: 30px;
				height: 30px;
				list-style: none;
				float: left;
				color: #ccc;
				cursor: pointer;
			}
			#adv li:first-child {
				color: lightseagreen;
			}
		</style>
	</head>
	<body>
		<div id="adv">
			<img src="img/slide-1.jpg" alt="">
			<ul>
				<li class="dot">●</li>
				<li class="dot">●</li>
				<li class="dot">●</li>
				<li class="dot">●</li>
			</ul>
		</div>
		<script src="js/mylib.js"></script>
		<script>
			function changeImage() {
				index += 1;
				index %= 4;
				var counter = 20;
				var opacity = 1.0;
				setTimeout(function() {
					if (counter > 0) {
						counter -= 1;
						opacity -= 0.05;
						// 通过image标签的style属性修改opacity样式调整透明度
						img.style.opacity = opacity;
						setTimeout(arguments.callee, 30);
					} else {
						img.src = "img/slide-" + (index + 1) + ".jpg";
						resetDotColor();
						dotItems[index].style.color = "lightseagreen";
						counter = 0;
						opacity = 0;
						setTimeout(function() {
							if (counter < 20) {
								counter += 1;
								opacity += 0.05;
								img.style.opacity = opacity;
								setTimeout(arguments.callee, 20);
							}
						}, 20);
					}
				}, 30);	
			}
			function resetDotColor() {
				for (var i = 0; i < dotItems.length; i += 1) {
					dotItems[i].style.color = "white";
				}
			}
			var index = 0;
			var advDiv = document.getElementById("adv");
			var img = document.querySelector("#adv>img");
			var dotItems = document.querySelectorAll("#adv li");
			for (var i = 0; i < dotItems.length; i += 1) {
				dotItems[i].index = i;
				bind(dotItems[i], "click", function(evt) {
					evt = evt || window.event;
					evt.target = evt.target || evt.srcElement;
					index = evt.target.index;
					img.src = "img/slide-" + (index + 1) + ".jpg";
					resetDotColor();
					evt.target.style.color = "lightseagreen";
				});
			}
			var timerId = setInterval(changeImage, 3000);
			bind(advDiv, "mouseover", function() {
				clearInterval(timerId);
			});
			bind(advDiv, "mouseout", function() {
				timerId = setInterval(changeImage, 3000);
			});
		</script>
	</body>
</html>

```

作业2-大图小图

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
				margin: 10px 20px;
			}
			#container li {
				float: left;
				list-style: none;
				width: 60px;
				height: 60px;
			}
		</style>
	</head>
	<body>
		<div id="container">
			<img src="img/picture-1.jpg" alt="">
			<ul>
				<li><img src="img/thumb-1.jpg" alt=""></li>
				<li><img src="img/thumb-2.jpg" alt=""></li>
				<li><img src="img/thumb-3.jpg" alt=""></li>
			</ul>
		</div>
		<script src="js/mylib.js"></script>
		<script>
		
		</script>
	</body>
</html>
```