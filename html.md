# HTML

1.概述

HTML是结构标准, CSS是表现标准, JS是行为标准

HTML结构标准中规定了网页上能够显示的内容,如文字,图片,视频等,CSS是表现标准规定网页内容的布局和样式,JS行为标准规定网页的内容的动态变化.

2.HTML

HTML(超文本标记语言),广义的h5指的是html5+CSS3+JS,html文件结构由不同的标签组成,标签的分类有双标签和单标签两种,标签里面可以是任何内容,大小写不敏感

```
<标签名 属性名1=属性值1>标签内容</标签名>
空格符:&nbsp;
强制换行:<br />
<h1>我是标题1</h1>

<p>段落</p>

<b>加粗</b>
<strong>加粗,强调</strong>
<i>倾斜</i>
<em>倾斜,强调</em>

水平线单标签<hr />

列表标签:ul,ol,dl
	ul:无序列表
	ol:有序列表
	dl:自定义列表

图片标签单标签<img>,属性:src(图片地址),title(图片标题),alt(加载失败的信息)

超链接标签
<a> </a>,属性:href(跳转目标对应的地址),target(跳转方式),默认是当前页面,设置为_blank是在新的页面去刷新

表格标签
table标签:表格整体(一个table标签代表一个表格)
tr标签:行(一个tr标签代表表格中的一行)
td标签:单元格(一个td代表一个单元格)
th标签:表头
属性
 a.border:设置表格边框的宽度(table属性)
 b.bordercolor:设置边框的颜色(table属性)
 c.background:设置背景图片
 d.bgcolor:设置背景颜色(可以作用于table\tr\td)
 e.cellspacing:设置单元格之间的间隙(默认是1)
 f.cellpadding:设置内容和单元格之间的间距
 g.width:一般作用于某一个单元格,影响的是这个单元格对应的那一列
 h.height:一般作用于行
 i.align:设置对齐方式(可以作用于table\tr\td)
	作用于table,让整个表格在浏览器中居中
	作用于tr/td,让内容在单元格中居中
细线表格是设置table属性cellspacing=1,bgcolor黑色,tr的bgcolor白色
复杂表格的制作过程:先确定表格中最多多少行,然后再数每一行有多少个单元格,然后确定每个单元格是否有合并现象,如果单元格有行的合并就设置单元格的rowspan属性如果有列的合并就设置单元格的colspan属性
	
表单标签:form标签,用来获取input标签中的数据,通过属性method对应的方式发送请求,发给属性action对应的请求

input标签单标签,type属性决定标签的形式
(1)text是文本输入框
属性:name,value,placeholder(占位符,提示信息),maxlength(约束字符个数)
提交input中的数据给服务器的时候,是以name值=value值来提交的
(2)password是密码输入框
(3)radio是单选按钮
name属性:如果多个单选按钮只选一个,那么这些按钮对应的name值必须一致
value属性:设置为这个按钮选中后提交对应的值
checked属性:设置默认选中
(4)checkbox是复选按钮  同一组的数据对应的name值一样
(5)button是普通按钮 value属性:按钮上显示的内容
(6)submit是提交按钮
(7)reset是重置按钮 将input标签的值回到初始状态
(8)file是文件域

select标签:下拉菜单,菜单中的选项通过option列举
可以通过optgroup标签对下拉菜单进行分组,通过label属性对分组进行命名

textarea标签:多行文本域
name:提交的数据对应的名字
	rows:默认一屏的行数
	cols:默认的列数
	placeholder:设置占位符
	disabled:禁用
	maxlength:约束能输入的最大的字符个数

button标签 按钮

div标签是空白标签,用来分组,div是块级标签,span是行内标签

块级标签:一个标签占一行
	h1-h6, p, 列表标签(ul,ol,dl), table,hr等
			
行内标签:一行可以放多个行内标签
	img, a,input,select,textarea等
```

