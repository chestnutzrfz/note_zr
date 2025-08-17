# 面向对象

面向对象：一种编程范式，编程规范，编程模式

面向过程：以对象为核心的编程，把问题拆分成一个个小步骤			         	   完成并且拼接起来。 

面向对象：以对象为核心的编程，在解决问题的时候是思考如何设计这个问题。python是一个完全面向对象的语言

对象：一个拥有属性以及行为的实体；

属性：描述这个对象的特征；

行为：描述这个对象所能完成的事情。

不同编程范式部分好坏与对立。





# 类和对象

实行一个对象是通过类产生的：

类：类相当于生活中的一个类别，一个比较抽象的概念。

对象：对象就是一个通过类产生的一个拥有属性以及行为的实体，是对应类里面的一个个体。先有类再有对象

定义类：

```python
class 类名：
	代码
    
# 每个单词首字母大写
# 定义类之后，执行代码，类里面的代码也会一起执行
# 定义在类中的变量称为属性
```



```python
# 定义一个类

class People:
    
# 类属性  （类属性是所有对象共有的属性）

	age = 23
    name = 'zr'
    height = 1.8
    
# 类实例化，类的实例赋值之后，该变量名称就是一个对象

aa = People()
print(aa)
print(aa.name)
da = People()
People.name = 'zrrr'
print(da.name)

# 查看类属性  __dict__

print(People.__dict__)
```



### 属性定义：

```python
class People:
    '''
    我是类文档
    就相当于类的说明书
    '''
    # 类属性（所有对象共有的）
    height = 1.53
    weight = 200
    
# 实例化类
zr = People()
print(zr.weight)


# 创建对象独有的属性，如果属性存在，则是修改属性值的操作
# 对象名.属性名 = 属性值
zr.weight = 90
zr.weight = 52
print(zr.weight)
# 使用对象.__dict__得到的是对象的属性
print(zr.__dict__)
# 修改类属性
# 类名.属性名 = 属性值
People.weight = 91
print(zr.weight)
# 动态的增加类属性
People.age = 20
print(zr.age)
```



### _\_init__方法

_\_init__称为初始化，实例化方法，魔法方法，构造方法。该方法在初始化对象的时候被调用。通常情况下用于设计对象的初始化属性，为类对象设置好默认值。

该方法在实例化对象的时候会自动调用执行。

```python
class Animal:
    '''动物类'''

    # 初始化方法
    def __init__(self , name , age):
        # 属性
        self.age = age
        self.name = name
        

cat = Animal('胖橘' , 1)
print(cat.name)
print(cat.age)

dog = Animal('啸天',1.5)
print(dog.name)
```

### self

类中每个方法在创建的时候都会自带的一个self参数 ， self其实就是一个形参可以定义成其他的名字 。 但是不建议。该参数必须是在第一个位置

self：表示对象本身

在使用/调用对应方法的时候  ， 类会自动将对象传递给self。

```python
class Animal:
    '''动物类'''

    # 初始化方法
    def __init__(self , name , age):
        # 属性
        self.age = age
        self.name = name

    def sleep(self):
        print(f'{self.name}在太阳下睡懒觉')

cat = Animal('胖橘' , 1)
dog = Animal('啸天',1.5)
dog.sleep()
# print(cat.name)
# print(cat.age)
# print(dog.name)
```

# 封装

面向对象的三大特性：封装、继承、多态



封装：把功能代码 ， 数据封装到某一个地方，需要的时候进行调用 ， 提过程序的安全性。即把属性以及方法放到类中 ，通过类对象的操作或者调用。

通过封装，可以将一些不想给用户看到的功能进行隐藏 ， 用户只能访问公开的功能，可以提高数据的安全性 ， 也对后期的维护降低成本。

封装的好处：便于分工 ， 便于复用 ， 可扩展性强。

```python
class People:
    '''人类'''

    # 初始化方法
    def __init__(self , name , age , weight , job):
        self.name = name
        self.age = age
        self.weight = weight
        self.job = job

    def eat(self):
        print(f'{self.name}狼吞虎咽的大干一场')
        self.weight += 2

    def drink(self):
        print(f'{self.name} 喝了两吨水')
        self.weight += 0.5

    def run(self):
        print(f'{self.name} 跑了两公里')
        self.weight -= 0.5

ac = People('zr' , 24 , 73 , "睡觉")
print(f'现在的体重为：{ac.weight}')
ac.eat()
print(f'现在的体重为：{ac.weight}')
ac.eat()
ac.eat()
ac.eat()
ac.eat()
print(f'现在的体重为：{ac.weight}')
ac.run()
ac.run()
ac.run()
ac.run()
ac.run()
ac.run()
print(f'现在的体重为：{ac.weight}')
```

### 属性查找

在实例化属性中不同的对象 ， 调用的属性不会产生影响互不干扰

对象寻找对应的属性，先从自身的实例属性开始查找 ， 如果没有再从类属性查找。

不同的对象之间的实例属性是互不相通 ， 都是独有的 ， 两者之江无法相互访问

```python
class Cat:

    # 类属性
    category = '猫'
    age = 2
    # 初始化方法
    def __init__(self , name , category):
        # 实例属性
        self.name = name
        self.category = category

    def sleep(self):
        print(f'{self.name}在太阳下睡懒觉')


pj = Cat('胖橘' , '波士猫')
pj.age = 1
print(pj.name)
print(pj.category)

ch = Cat('翠花','加菲猫')
print(ch.name)
print(ch.age)
print(ch.category)

# ha = Cat('二哈')
# ha.category = '狗'
# print(ha.category)
```



### 属性隐藏

在类中定义一些数据或者功能不希望被外部访问到以及操作的时候 ， 可以将数据以及功能进行隐藏。

在Python中没有绝对的隐藏 ， 是可以通过一些方法对其进行访问的。

在类中的三种隐藏方法：

##### 属性或者方法名前加上双下划线

双下划线开头的属性 ， 是对象的隐藏属性，隐藏属性在类内部进行访问

```python
class People:

    def __init__(self , name , age):
        self.name = name
        self.__age = age    # 将age属性进行隐藏

    def __speak(self):
        print(f'我今年{self.__age}')

ac = People('阿宸', 24)
# print(ac.name)
# 获取对象属性
# print(ac.__dict__)
# 对象名称._类名__属性名
print(ac._People__age)
ac._People__speak()
```



##### 使用property（）函数

property可以设置、获取 ， 删除对象的某一个属性值 ， 也可以限制用户对属性的设置与获取

```python
# property 属性
property(fget = None , fset = None , fdel = None , doc = None)

# fget = 是获取属性值的方法
# fset = 是设置属性值的方法
# fdel = 是删除属性值的方式
# doc = 是属性信息的描述。如果省略，会把fget方法的docstring
```

```python
class People:

    def __init__(self , name , age):
        self.name = name
        self.__age = age    # 将age属性进行隐藏

    def speak(self):
        print(f'我今年{self.__age}')

    def get_age(self):
        print('===get被访问=====')
        return self.__age

    def set_age(self , value):
        print('===set被访问=====')
        self.__age = value

    def del_age(self):
        del self.__age

    # 赋予对象属性权限
    age = property(fget=get_age , fset=set_age , fdel=del_age)

ac = People('阿宸', 24)
# print(ac.name)
# 获取对象属性
# print(ac.__dict__)
# 对象名称._类名__属性名
# print(ac._People__age)
# ac._People__speak()
print(ac.age)
ac.age = 22
print(ac.age)
del ac.age
# print(ac.age)
```

##### @property

属性隐藏：在属性名前加上双下划线 

赋予对象的属性的权限：property（fget = 获取(查看) , fset = 设置(修改) , fdel = 删除）

@property是property提供的

```python
@property  装饰的方法是获取属性值的方法 ， 被装饰的方法的名字会被作为属性名 ， 方法名尽量跟隐藏的属性名一致
@属性名.setter 装饰的方法是设置属性值的方法
@属性名.deleter 装饰的方法是删除属性值的方法
```



```python
class Student:
    def __init__(self , grade):
        self.name = 'ac'
        self.__grade = grade

    @property
    def grade(self):
        return self.__grade

    @grade.setter
    def grade(self , value):
        self.__grade = value

    @grade.deleter
    def grade(self):
        del self.__grade


hzx = Student(98)
print(hzx.grade)
hzx.grade = 150
print(hzx.grade)
del hzx.grade
print(hzx.grade)
```





# 继承

在python中是在多个类中的一种所属关系 ， 被继承的类称为父类 ， 接收的类称为子类；在继承中子类是默认继承父类中的属性以及方法

继承可以解决类与类之间的代码冗余。

在python3中都会默认继承object类 ， 即object是python中所有类的父类（基类 ， 超类）。



### 单继承

一个子类继承一个父类 ， 子类默认继承父类中的所有方法 ， 属性

```python
class Father:

    def __init__(self , name):
        self.name = name
        self.clothes = '龙袍'
        self.job = '批奏折'

    def xingwei(self):
        print('××满门抄斩')

    def love(self):
        print('后宫佳丽三千')

    def eat(self):
        print('山珍海味')


class Son(Father):
    pass

ql = Son('乾隆')
print(ql.name)
ql.xingwei()
ql.love()
ql.eat()
```

### 重写父类中的方法

在子类中重新定义父类的方法 ， 子类在实例化之后会默认的访问自身的方法。

```python
class Father:

    def __init__(self , name , age):
        self.name = name
        self.age = age

    def eat(self):
        print(f'{self.name}在狼吞虎咽的吃饭')

    def money(self):
        print('在土耳其')


class Gril(Father):

    def eat(self):
        print(f'{self.name}在优雅 , 高贵的吃饭')

    # super()
    def money(self):
        print('在北京故宫')
        # 方法一,点名道姓
        # Father.money(self)
        # 方法二 , 通过super()
        super().money()


mq = Gril('默契' , 18)
mq.eat()
mq.money()
```



属性查找：子类对象自身——>子类中——>父类中



### 多层继承

被继承类都有属于自己的父类

```python
class Car:

    def __init__(self , wheel):
        self.wheel = wheel

    def xingzhuan(self):
        print('几个钢管')


class Train(Car):

    def xingzhuan(self):
        super().xingzhuan()
        print('几块铁皮')


class Gaotie(Train):



    def xingzhuan(self):
        super().xingzhuan()
        print('子弹头')




# hc = Train('轮毂')
# hc.xingzhuan()

# gt = Gaotie('轮毂')
# gt.xingzhuan()

class A:
    # name = '老黄A'

    pass

class B(A):
    # name = '老黄B'

    pass

class C(B):

    # name = '老黄'
    pass
    # def __init__(self):
    #     self.name = 'ac'


q = C()
print(q.name)
```

### 多继承

多继承：一个子类有多个父类

在多继承中出现相同的属性或者方法 ， 继承的顺序从左到右

```python
class Zoo:
    pass

class Zoo1:
    pass


class Horse(Zoo1 , Zoo):

    def body(self):
        return '体型健壮'


class Donkey(Zoo):

    def body(self):
        return  '提型娇小'

    def labour(self):
        return  '勤快能干'

class Mule(Horse , Donkey):
    pass

M = Mule()
print(M.body())
print(M.labour())
# 查看继承的顺序
print(Mule.__mro__)
print(Mule.__base__)
# 在多继承中查看所有的父类
print(Mule.__bases__)
```



# 多态

不同的对象， 调用同一个方法 ， 表现出不同的形态。

多态的实现：1、必须要有类的继承；2、子类对父类的方法进行重写

```python
class A:

    def func(self):
        print('我只能简单的读')

class B(A):

    def func(self):
        super().func()
        print('我不仅会读还会写')

ac = A()
lh = B()
ac.func()
lh.func()
```



# 检查类型

```python
type()	# 检查单个的数据类型
issubclass(cls , class_tuple)	# 检查类是否为后者的子类（检查前者是否继承后者）
isinstance(obj , cls)	# 检查对象是否为类中的
```

```python
res = 'zr是个大帅哥'

# print(isinstance(res , int))

# print(issubclass(str, object))


class Father:
    pass

h = Father()
print(isinstance(h, Father))
print(isinstance(res, Father))

class Son(Father):
    pass

# print(issubclass(Father, Son))
# print(issubclass(Son, Father))
```



# 内置方法

### _\_str__

对象信息的格式化

```python
class Person:

    def __init__(self , name , job):
        self.name = name
        self.job = job

    def __str__(self):
        return f'{self.name}在人民广场 ， {self.job}'
    
ac = Person('阿宸' , '卖煎饼')
hzx = Person('黄泽鑫' , '卖手抓饼')
print(ac)
print(hzx)
```



### _\_del__

当检测到对象没有在继续引用时 ， 就会自动的将对象所占用的内存空间清除

```python
class Person:

    def __init__(self , name , job):
        self.name = name
        self.job = job

    def __str__(self):
        return f'{self.name}在人民广场 ， {self.job}'

    def __del__(self):
        print(f'{self.name}对象没有引用被清除')



ac = Person('阿宸' , '卖煎饼')
hzx = Person('黄泽鑫' , '卖手抓饼')
print(ac)
del ac
print('='*20)
print(hzx)
print('在听课的各位都是靓仔 ， 靓女')
print('很棒！！！')
```



# 绑定与非绑定

### 类方法

通过@classmethod进行方法装饰 ， 使用在对类属性的修改

类方法操作的是类属性 ， 同cls进行对类的绑定

```python
# 类方法（绑定）

class Student:

    # 类属性
    id = 0

    # 实例属性
    def __init__(self , name):
        self.name = name
        self.count()

    @classmethod
    def count(cls):
        cls.id += 1
        return cls.id

ac = Student('阿宸')
print(ac.id)
hzx = Student('黄泽鑫')
print(hzx.id)
print(Student.id)
```



### 静态方法（非绑定）

通过@staticmethod进行方法装饰 ， 不需要绑定self以及cls

静态方法与定义在类外面的函数是一致的 ， 相当于寄生在类中 ， 放在类中 ，方便管理（维护）。

```python
import time

class Student:

    # 类属性
    id = 0

    # 实例属性
    def __init__(self , name):
        self.name = name
        self.count()

    @classmethod
    def count(cls):
        cls.id += 1
        return cls.id

    @staticmethod
    def str_time():
        print(f'{time.strftime("%Y/%m/%d")}')
class B(Student):
    pass

a = B('ll')
a.str_time()

ac = Student('阿宸')
print(ac.id)
hzx = Student('黄泽鑫')
print(hzx.id)
print(Student.id)
```



# 反射

反射：通过字符串的形式来操作对象属性。



### 对象反射

1、getattr 获取指定的对象属性

```python
变量名 = getattr(对象 , '对象属性'  , 设置默认值)
# 设置默认值:指当在对象中查找不到对应的对象顺序ing是返回的内容 ， 如果没有设置默认是并且属性不存在就会报错。
```

2、setattr去对象中设置一个对象属性

```python
setattr(对象,'对象属性' , 值)
```

3、hasattr判断对象是否有对应的对象属性

```python
变量名 = hasattr(对象 ， '对象属性')
# 返回bool类型
```

4、delattr删除指定对象的属性

```python
delattr(对象,'对象属性')
```

```python
class A:

    def __init__(self , name , age):
        self.name = name
        self.age = age

    def say_hi(self):
        print(f'hi , {self.name}靓仔你好')


ac = A('阿宸' , 24)
# print(ac.name)
# ac.say_hi()
# 变量名 = getattr(对象 , '对象属性')
# nn = input('请输入要查看属性名：')
# n = getattr(ac , nn , '属性方法找不到')
# print(n)

# setattr(对象,'对象属性' , 值)
setattr(ac , 'name' , '马晨旺')
setattr(ac , 'height' , 1.89)
print(ac.name)
print(ac.__dict__)


# 变量名 = hasattr(对象 ， '对象属性')

bol = hasattr(ac , 'weight')
print(bol)
res = hasattr(ac , 'height')
print(res)

# delattr(对象,'对象属性')

# delattr(ac , 'say_hi')    # 报错 ， 不能删除方法
delattr(ac , 'age')
print(ac.__dict__)
```

实例：

```python
class User:

    def login(self):
        print('这是微信登录页面')

    def register(self):
        print('这是一个微信注册')

    def speak(self):
        print('这是聊天页面')


# 未使用反射
ac = User()
# choose = input('请输入你要操作的功能：')
# if choose == 'login':
#     ac.login()
# elif  choose == ' register':
#     ac.register()
# elif choose == 'speak':
#     ac.speak()
# else:
#     print('输入有误')


# 使用反射
lh = User()
choose = input('请输入你要操作的功能：')
if hasattr(lh , choose):
    fun = getattr(lh , choose)
    fun()
else:
    print('输入有误')
```



# 异常处理

异常：就是在程序执行的过程中有逻辑等其他的错误导致 ， 程序终止运行。

异常处理：在程序执行的过程中 ， 发现错误之火对其进行处理 ， 让程序可以正常执行不为此被迫停止运行。

### 异常错误

1 ， 语法错误 —— SyntaxError

2、逻辑错误

```python
# TypeError	  		不同的类型数据之间的无效操作
# ValueError  		值类型错误
# IndentationError  缩进错误 ， 缩进不一致
# AttributeError    没有找到对应的属性
# IndexError 		下标索引超出范围
# NameError       	名字未定义
# KeyError			在字典中找不到对应的键
```

### 异常处理

语法格式：

```python
try:
    代码块（感觉有问题的代码）
except 异常类型:
    判断到对应的异常执行的代码
else:
    代码块没有异常执行的代码
finally:
    不管有没有异常都会执行
```

在异常类型后面加上as 变量名 ， 即将异常信息赋值给变量 ， 可以获取异常错误的信息

Exception：可以捕获所有的异常

```python
try:
    res = '阿宸是个大帅哥'
    print(res[60])
except Exception:
    print('字符串没有那么长度')
else:
    print('一切正常')
finally:
    print('管你是谁 ， 老子就是要执行')
```

### 定义异常

1、assert (断言)

发送的AssertionError异常错误

```python
assert 判断表达式 ， 返回异常信息（当判断表达式为False时执行）


x = 100
y = 200

assert x > y , '大脑发育不完全 ， 小脑完全不发育'
print(x > y)
```

2、raise

```python
raise Exception(异常信息)


money = int(input('请输入支付金额：'))
if money < 650:
    raise Exception(f'money不能小于 650 。当前money的值为{money} , 支付失败')
else:
    print('支付成功')
```



