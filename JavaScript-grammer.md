# JavaScript

```
1.注释
 单行注释在前面加//,多行注释/**/
2.标识符
 数字,字母,下划线和$符组成,数字不能开头,大小写敏感
3.基本数据类型
 Number(数字-包含所有的数字)
 Boolean(布尔类型)
 String(字符串)
 Array(数组)
 Object(对象)
 NaN(不存在的数字),null(空),undefined(变量没有赋值的时候)
4.字面量
 Number:所有的数字  Boolean字面量:只有true和false String字符串:用单引号或者双引号引起来的字符集  Array字面量:相当于python中的列表  Object对象字面量:key相当于属性名,value相当于属性值 相当于python中的字典加对象  typeof:查看数据类型
5.js中的语句:
a.一条语句结束后可以写分号,也可以不写,如果一行写多条语句就必须写分号
b.js中没有缩进语法要求,需要使用代码块的时候使用{}
6.变量的声明
 var 变量名=初值 驼峰式命名
7.运算符
 数学运算符,比较运算符,逻辑运算符,赋值运算符,三目运算符
 数学运算符:+、-、*、/、%、**(js7中才有的)、++、--
 比较运算符:>,<,==,!=,>=, <=, ===, !==, >==, <==
 相等(==):只判断值是否相等  完全相等(===):判断值和类型是否相等
 逻辑运算符：&&(与)，||(或), !(非)
 赋值运算符：=， += ，-=， *=， /=， %=
 语法：表达式1?值1:值2  ---> 判断表达式1的值是否为真，为真整个  运算的结果就是值1，否则是值2
8.分支结构
 (1)if语句 
 if(条件语句){
  	 代码段
  }
  
  if(条件语句){
 	代码段1
 }else{
 	代码段2
 }
 
 if(条件语句1){
 	代码段1
 }else if(条件语句2){
 	代码段2
 }else{
 	代码段3
 }
 (2)switch语句
 switch(表达式){
 	case 值1:{
 		代码段1
 		
 	}
 	case 值2:{
 		代码段2
 		
 	}
 	...
 	default:{
 		代码段3
 	}
 	执行过程:先计算表达式的值，然后再用这个值去和后边case关键字后面的值一一对比，看是否相等。找到第一个和表达式的值相等的case,然后将这个case作为入口，一次执行后边所有的代码，直到遇到break或者switch结束。如果没有找到和表达式的值相等的case就执行default后面的代码.default可有可无，case可以有若干个
9.循环结构
 (1)for循环
  for(var 变量 in 序列){
 	循环体
 }
 
 for(表达式1；表达式2；表达式3){
 	循环体
 }
 先执行表达式1，然后再判断表达式2的结果是否为true,如果为true，就执行循环体。执行完循环体再执行表达式3。然后再判断表达式2的结果是否为true，依次循环，知道表达式2的结果为false为止
 (2)while循环
 while(条件语句){
 	循环体
 }
 do{
 	循环体
 }while(条件语句)
 先执行一次循环体，然后再判断条件语句是否为true,为true又执行循环体，依次类推，直到条件语句为false，循环就结束
10.函数
 function 函数名(参数列表){
 	函数体
 }
 注意：js中不能同时返回多个值（有元祖语法的语言才支持多个返回值）
 js中，函数也可以作为变量
11.数据类型
new 类型名(值) ---> 可以将其他的类型的数据转换成相应类型的值
1.数字类型(Number)：不能转换的结果是NaN
2.布尔(Boolean):所有为0为空的转换成布尔是false，如NaN,null和undefined都是false;其他的都是true
3.字符串(String):unicode编码
获取单个字符：通过字符串[下标]
js中的下标支持0到长度-1，不支持负值,不支持切片
4.数组 有序，可变的，元素的类型可以是任意类型的数据
增:数组.push() 
删:数组.pop()删除最后一个元素  数组.shift()删除第一个元素  splice(删除的开始下标, 删除的元素的个数)
splice(被删除的下标/添加的开始下标, 添加个数, 被添加的元素列表)

```

