title : python 函数

----

# Python 函数



写程序六个字原则:高内聚 低耦合(high cohesion low coupling)

高内聚:写一个函数只做好一件事情
低耦合:一个函数尽量不要跟其他函数绑在一起

```
def calc(items, fn):
    """计算函数,将+,-,*,/运算与函数解耦合"""
    result = items[0]
    for item in range(1, len(items)):
        result = fun(result, items[index])
    return result
```



在python中函数是一等公民,函数可以赋值给变量,可以作为方法的参数和返回值
自定义规则就是解耦合操作

生成器() 浪费时间,调一次计算一次 存的是数据的产生方式,是一种算法
生成式[] 浪费空间

时间和空间是无法兼具的

```
五个人分鱼,A把鱼分成5份,扔掉了多余的一条,拿走其中的一份,B把剩下的鱼又分成5份,扔掉多余的一条,拿走一份,C,D,E操作相同,问这堆鱼最少有多少条?
fish = 0
while True:
    enough = True
    amount = fish
    for _ in range(5):
        if (amount - 1) % 5 == 0:
            amount = (amount - 1) // 5 * 4
        else:
            enough = False
            break
        
    if enough:
        print(fish)
        break
    fish += 1
```





## 函数中的参数



```
*args-可变参数 元祖 不知道参数个数可以通过args对参数打包 *作用是打包
**kwargs-关键字参数keyword arguments 字典 函数接收带参数名和参数值的参数
def foo3(a, *, b, c):
    return a + b + c
*前面的参数是位置参数,传参时可以不用指定参数名
*后面的参数是命名关键字参数,传参时必须指定参数名,否则报错
```




## 递归函数



经典问题:
骑士周游问题
汉洛塔
八皇后问题

```
汉洛塔问题
def move(num, a, b, c):
    #把n-1个盘子从a搬到c
    move(num-1, a, c, b)
    #把最大的盘子从a搬到b
    print(f'{a}---->{b}')
    #把n-1个盘子从c搬到b
    move(num - 1, c, b, a)
    
num = int(input('盘子个数:'))
move(num, 'A', 'B', 'C')
```



```
斐波那契数列(优化)
def fib(num, temp={}):
    if num in (1, 2):
        return 1
    try:
        return temp[num]
    except KeyError:
        temp[num] = fib(num - 1) + fib(num - 2)
        return temp[num]
        
def fib2(num):
    a, b = 1, 1
    for _ in range(num - 1):
        a, b = b, a+b
    return a
    
上楼梯(优化)
def walk(num, temp={}):
    if num <= 0:
        return 1 if num == 0 else 0
    try: 
        return temp[num]
    except KeyError:
        temp[num] = walk(num - 1) + walk(num - 2) + walk(num - 3)
        return temp[num]


def walk2(num):
    s1, s2, s3 = 1, 2, 4
    for _ in range(num - 1):
        s1, s2, s3 = s2, s3, s1 + s2 + s3
    return s1
```

爬楼梯思想

当有一个10层的楼梯,一次可以爬一层或两层,首先可以先假设一下:

爬1层---1种方法

爬2层---2种方法

爬3层---3种方法

爬4层---5种方法

爬5层---8种方法

...

可以看出规律是an = an-1 + an-2,那么到第十层的方法数就是到第九层方法数加上到第八层的方法数,以此类推





> 总结
>
> 递归函数最重要的就是:
>
> 1.找到递推规律
> 2.找到收敛条件,知道什么时候让函数结束





##装饰器函数
  装饰器函数是用一个函数装饰另一个函数,给它增加额外的功能,而不需要书写重复的代码.
  装饰器函数的参数是被装饰的函数,返回的是起装饰作用的函数
  调用被装饰的函数时,其实执行的是装饰器中返回的函数
  函数添加装饰器的语法就是在函数前写上@装饰器函数

```
import time
def record(fn):
    
    def wrapper(*args, **kwargs):
        start = time.time()
        ret_value = fn(*args, **kwargs)
        end = time.time()
        print(f'{end - start}秒')
        return ret_value
        
    return wrapper
   
@record
def fac(num):
    result = 1
    for n in range(1, num + 1):
        result *= n
    return result
 #装饰器的本质是执行了下面的代码
 # fac = record(fac)
```









## 面向对象

面向对象有三步:

1.定义类-把同类型公共的事物总结出共同特征

(1)数据抽象:找到和对象相关的属性,找名词

(2)行为抽象:找方法,找动词

2.创建对象

3.给对象发消息,让对象做事情



共同的属性和行为写在父类中,特有的写在子类中

```
from abc import ABCMeta, abstractmethod
#把类声明成抽象类
class Employee(metaclass=ABCMeta):
 
    def __init__(self, name):
        self.name = name
        
    @abstractmethod  //说明这个方法是抽象方法,装饰器,要求子类必须实现
    def salary(self):
        pass
 
class Manager(Employee):
    
    @property//把方法改成属性
    def salary(self):
        return 15000
        
class Programmer(Employee):

    def __init__(self, name):
        self.name = name
        slef.work = 0
        
    @property
    def salary(self):
        return 200 * self.work
        
class Salesman(Employee):
  
    def __init__(self, name):
        self.name = name
        self.sale = 0
        
    @property
    def salary(self):
        return 1800 + self.sale * 0.05
        
def main():
    emps=[
       Manager("刘备"), Manager("曹操"),
        Programmer("诸葛亮"), Programmer("荀彧"),
        Salesman("貂蝉")
    ]
    for emp in emps:
        #isinstance函数可以在运行时进行类型识别
        if isinstance(emp, Programmer):
            emp.work = int(input(f'请输入{emp.name}本月工作时间:'))
        elif isinstance(emp, Salesman):
            emp.sale = int(input(f'请输入{emp.name}本月销售额:'))
        print('%s: %.2f元' % (emp.name, emp.salary))
        
        
if __name__ == '__main__':
    main()
```

重写:子类把父类已经有的方法重新实现一遍,不同的子类给出不同的实现版本,就可以实现多态

多态:同样的方法,干的事情不同