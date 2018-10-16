

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
		<script src="js/mylib.js"></script>
		<script>
			function deleteItem(evt) {
				evt = evt || window.event;
				evt.target = evt.target || evt.srcElement;
				var li = evt.target.parentNode;
				li.parentNode.removeChild(li);
			}
			
			var delAnchors = document.querySelectorAll("#fruits a");
			for (var i = 0; i < delAnchors.length; i += 1) {
				bind(delAnchors[i], "click", deleteItem);
			}
			
			var okBtn = document.getElementById("ok");
			var fruitInput = document.querySelector("#container>input[type=text]");
			var fruitsUl = document.getElementById("fruits");
			bind(okBtn, "click", function() {
				var fruitName = fruitInput.value.trim();
				if (fruitName.length > 0) {
					var li = document.createElement("li");
					li.innerHTML = fruitName;
					li.style.backgroundColor = "rgb(100, 130, 90)";
					var a = document.createElement("a");
					a.innerHTML = "×";
					a.href = "javascript:void(0);";
					bind(a, "click", deleteItem);
					li.appendChild(a);
					// fruitsUl.appendChild(li);
					fruitsUl.insertBefore(li, fruitsUl.firstChild);
				}
			});
		</script>
	</body>
</html>
```





广告位招租

```
<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<title></title>
		<style>
			#adv {
				width: 200px;
				height: 200px;
				color: yellow;
				background-color: blue;
				position: fixed;
				right: 10px;
				top: 10px;
			}
			#adv button {
				float: right;
			}
		</style>
	</head>
	<body>
		<div id="adv">
			广告位招租
			<button id="closeBtn">关闭</button>
		</div>
		<script src="js/mylib.js"></script>
		<script>
			var closeBtn = document.getElementById("closeBtn");
			bind(closeBtn, "click", function(evt) {
				// 元素访问子节点 - children
				// 元素访问父节点 - parentNode
				// 元素访问兄弟节点 - previousSibling / nextSibling
				// evt = evt || window.event;
				// evt.target = evt.target || evt.srcElement;
				// evt.target.parentNode.style.display = "none";
				// closeBtn.parentNode.style.visibility = "hidden";
				var advDiv = closeBtn.parentNode;
				var currentStyle = advDiv.currentStyle? 
					advDiv.currentStyle : 
					document.defaultView.getComputedStyle(advDiv);
				var width = parseInt(currentStyle.width) + 50;
				var height = parseInt(currentStyle.height) + 50;
				advDiv.style.width = width + "px";
				advDiv.style.height = height + "px";
				// alert(currentStyle.width);
				// alert(currentStyle.height);
				// alert(currentStyle.backgroundColor);
			});
		</script>
	</body>
</html>
```



变色方块

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
				cursor: pointer;
			}
			.small {
				width: 80px;
				height: 80px;
				float: left;
			}
		</style>
	</head>
	<body>
		<div id="container">
		
		</div>
		<div id="buttons">
			<button id="add">添加</button>
			<button id="fla">闪烁</button>
		</div>
		<script src="js/mylib.js"></script>
		<script>
			bind(window, "load", function() {
				var container = $("container");
				bind($("add"), "click", function() {
					var div = document.createElement("div");
					div.className = "small";
					div.style.backgroundColor = randomColor();
					container.insertBefore(div, container.firstChild);
				});
				var isFlashing = false;
				var timerId = 0;
				bind($("fla"), "click", function() {
					if (isFlashing) {
						clearInterval(timerId);
					} else {
						timerId = setInterval(function() {
							var divs = document.querySelectorAll("#container>div");
							for (var i = 0; i < divs.length; i += 1) {
								divs[i].style.backgroundColor = randomColor();
							}
						}, 200);
					}
					$("fla").innerHTML = isFlashing ? "闪烁" : "暂停"; 
					isFlashing = !isFlashing;
				});
			});
		</script>
	</body>
</html>
```



移动方块

```
<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<title></title>
		<style>
			#one {
				position: fixed;
				width: 300px;
				height: 300px;
				left: 50px;
				top: 50px;
				background-color: lightgreen;
			}
			#two {
				position: fixed;
				width: 200px;
				height: 200px;
				right: 50px;
				bottom: 50px;
				background-color: lightpink;
			}
			#three {
				position: fixed;
				width: 250px;
				height: 250px;
				left: 50px;
				bottom: 50px;
				background-color: darkgrey;
			}
		</style>
	</head>
	<body>
		<div id="one"></div>
		<div id="two"></div>
		<div id="three"></div>
		<script src="js/mylib.js"></script>
		<script>
			var draggables = [];
			
			function makeDraggable(div) {
				draggables.push(div);
				div.isMouseDown = false;
				div.originX = 0;
				div.originY = 0;
				div.oldX = 0;
				div.oldY = 0;
				div.start = function(evt) {
					for (var i = 0; i < draggables.length; i += 1) {
						draggables[i].style.zIndex = 0;
					}
					this.style.zIndex = 10;
					this.isMouseDown = true;
					var currentStyle = document.defaultView.getComputedStyle(this);
					this.originX = parseInt(currentStyle.left);
					this.originY = parseInt(currentStyle.top);
					this.oldX = evt.pageX;
					this.oldY = evt.pageY;
				};
				div.move = function(evt) {
					if (this.isMouseDown) {
						var dx = evt.pageX - this.oldX;
						var dy = evt.pageY - this.oldY;
						this.style.left = this.originX + dx + "px";
						this.style.top = this.originY + dy + "px";
					}
				};
				div.stop = function() {
					this.isMouseDown = false;
				};
				bind(div, "mousedown", div.start);
				bind(div, "mousemove", div.move);
				bind(div, "mouseup", div.stop);
				bind(div, "mouseout", div.stop);
			}
			
			makeDraggable($("one"));
			makeDraggable($("two"));
			makeDraggable($("three"));
		</script>
	</body>
</html>
```

