# web框架本质

最基本的需求实现

根据不同的url返回不同的内容

服务器程序和应用程序

实现返回HTML页面

动态渲染数据

总结



### 最基本的需求实现

在浏览器中输入一个url就可以访问到数据-->基于socket实现的数据交互,

浏览器是socket的客户端发送一个请求给指定的socket服务端



```
import socket

# 1 创建服务器对象
server = socket.socket()
# 2 绑定ip端口
server.bind(('127.0.0.1',8000))
# 3 监听
server.listen()
# 4 开机
while True:
	# 等待链接
	conn,addr = server.accept()
	# 收发消息
	data = conn.recv(1024)  # 最大接受1024个bytes
	print(data)
	conn.send(b'hello')
	# 关闭
	conn.close()
# 关机
server.close()
```



在浏览器的导航栏输入`127.0.0.1:8000`

出现问题,

```
原因:
网站和用户收发消息有个格式依据不能随便写
即http协议
浏览器本质是socket的客户端会对接无数的socket服务端,
浏览器不识别 没有遵守http协议

```

```
import socket

server = socket.socket()
server.bind(('127.0.0.1', 8000))  
server.listen()
while True:
    conn, client_addr = server.accept()
    data = conn.recv(1024)  
    print('客户端的数据', data)
    # 服务端响应的数据需要符合HTTP响应格式
    conn.send(b'HTTP1.1 200 OK\r\n\r\n') # 新增一行代码
    conn.send(b'HELLO')
    conn.close()
server.close()
```





### 根据不同的URL路径返回不同的内容

思路:  可以利用客户端发送的数据  拿到url再判断

```
import socket

server = socket.socket()
server.bind(('127.0.0.1', 8000))
server.listen()
while True:
    conn, client_addr = server.accept()
    data = conn.recv(1024)
    data = data.decode().split('\r\n') # 进行切割
    url = data[0].split(' ')[1] # 拿到了url
    conn.send(b'HTTP1.1 200 OK\r\n\r\n')
    # 根据请求的url不同做判断，返回不同的内容
    if url == '/index':
        response = 'index'
    elif url == '/test':
        response = 'test'
    else:
        response = '404 Not Found!'
    # 返回指定的内容
    conn.send(response.encode())
    conn.close()
server.close()
```

当url越来越多,要写的判断也越来越多,可以利用函数做优化

```
import socket

# url对应的请求方法
def index(request):
    return 'index'

def test(request):
    return 'test'

# 定义一个方法  当所有的请求都找不到的时候，就返回错误
def handler404(request):
    return '404 Not found!'

# 定义一个对应关系
urlpatterns = [
    ('/index',index),
    ('/test',test),
]

server = socket.socket()
server.bind(('127.0.0.1', 8000))
server.listen()
while True:
    conn, client_addr = server.accept()
    data = conn.recv(1024)
    data = data.decode().split('\r\n') # 进行切割
    url = data[0].split(' ')[1] # 拿到了url
    conn.send(b'HTTP1.1 200 OK\r\n\r\n')
    # 遍历列表，根据请求的url来执行对应的处理函数
    for line in urlpatterns:
        if url == line[0]:
            response = line[1](data)
            break
    else:
        response = handler404(data)
    # 返回指定的内容
    conn.send(response.encode())
    conn.close()
server.close()
```



随着url和处理方法越来越多,这份文件也越来越大,可以利用模块对功能进行拆分,放到不同的模块中去,实现解耦合

```
# manage.py
import socket

from urls import urlpatterns    # 导入urls模块中的urlpatterns

# 定义一个方法  当所有的请求都找不到的时候，就返回错误
def handler404(request):
    return '404 Not found!'

server = socket.socket()
server.bind(('127.0.0.1', 8000))
server.listen()
while True:
    conn, client_addr = server.accept()
    data = conn.recv(1024)
    data = data.decode().split('\r\n') # 进行切割
    url = data[0].split(' ')[1] # 拿到了url
    conn.send(b'HTTP1.1 200 OK\r\n\r\n')
    # 遍历列表，根据请求的url来执行对应的处理函数
    for line in urlpatterns:
        if url == line[0]:
            response = line[1](data)
            break
    else:
        response = handler404(data)
    # 返回指定的内容
    conn.send(response.encode())
    conn.close()
server.close()
```

```
# urls.py
import views # 导入views.py

# 定义一个对应关系
urlpatterns = [
    ('/index',views.index),
    ('/test',views.test),
]
```

```
# views.py
# url对应的请求方法
def index(request):
    return 'index'

def test(request):
    return 'test'
```

以后我们需要添加更多的请求路径就去url.py中添加一个对应关系,然后去views.py中添加处理的函数



### 服务器程序和应用程序

自己写的socket部分不完善,很多问题没有解决

真实开发web程序来说,一般分为两部分:  服务器程序和应用程序

服务器程序负责对socket服务器进行封装,并在请求到来时,对请求的各种数据进行整理

应用程序则负责具体的逻辑处理,为了方便应用程序的开发,就出现了众多的web框架,不同的框架有不同的开发方式,但是无论如何,开发出的应用程序都要和服务器程序配合,才能为用户提供服务

这样服务器程序就要为不同的框架提供不同的支持,这样不好,对服务器来说,需要支持各种不同框架,对框架来说,只有支持它的服务器才能被开发出的应用使用.

这时候,标准化就十分重要,设立一个标准只要服务器程序和应用程序都支持这个标准,就可以配合使用.

`WSGI`(Web Server Gateway Interface)就是一种规范,它定义了使用python编写的web应用程序与web服务器程序之间的接口格式,实现web应用程序与web服务器程序之间的解耦

常用的`WSGI`服务器有`uwsgi`,`Gunicoen`,而python标准库提供的独立`WSGI`服务器叫`wsgiref`



### 可以利用wsgiref模块来替换我们写的web框架的socket server部分

```
# manage.py
from wsgiref.simple_server import make_server

from urls import urlpatterns


def handler404(request):
    return '404 Not found!'


def run(data,start_response):
    # 设置HTTP响应的状态码和头信息
    start_response('200 OK', [('Content-Type', 'text/html;charset=utf8'), ])
    url = data['PATH_INFO']
    for line in urlpatterns:
        if url == line[0]:
            response = line[1](data)
            break
    else:
        response = handler404(data)
    return [response.encode()]


if __name__ == '__main__':
    server = make_server('127.0.0.1',8000,run)
    server.serve_forever()
```



### 实现返回HTML页面

返回HTML页面,本质就是打开一个html文件,读取文件内容并返回

```
# views.py
def index(request):
    # 为了方便管理，我们将所有的html页面放在一个叫做templates的文件夹里面
    with open('templates/index.html','r',encoding='utf-8') as f:
        data = f.read()
    return data
```

创建一个叫做templates的文件夹,在其中创建index.html文件即可



### 动态渲染数据

在html页面中实现动态的数据展示

思路:  html文件就是字符串 ,利用字符串的替换功能即可实现

```
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<h1>我是index.html页面！</h1>
<h2>现在的随机数是:{{ a }}</h2>
</body>
</html>
```

```\
# views.py
import random

def index(request):
    with open('templates/index.html','r',encoding='utf-8') as f:
        data = f.read()
    # 定义一个随机数
    num = str(random.randint(1,99))
    # 利用Python字符串的替换，将指定的符号换成我们真实要展示的数据
    return data.replace('{{ a }}',num)
```



### 总结

至此,我们已经实现了一个简易的web框架,我们只需要在urls.py文件中书写请求路径和处理函数的对应关系,并在views.py中书写处理函数,利用字符串的替换可以实现动态的数据渲染效果

manage.py 是我们程序的入口文件,利用这个文件来运行整个程序

urls.py 是我们的路由文件,里面书写url和处理函数的对应关系

views.py是我们的视图文件,里面书写url的处理函数,必须接受一个形参,这个形参里面是请求相关数据



# win11

win11 系统不稳定有很多bug

开发:  不使用最新的技术  最新不稳定

推荐使用win10



# `Django`的路由

### 下载`Django`

pip install django==2.2

注意:  python解释器的版本要大于3.5

2.2 为长期稳定支持版



### 创建`Django`项目

`cmd`  输入  `django-admin startproject` 项目名

会在当前路径下创建一个文件夹--> `Django`项目

项目的目录结构:

​	名字

​		名字	

​				`__init__.py`  # 这是一个包

​				`urls.py`    #  url和视图函数的映射关系

​				`settings.py`   #  配置信息

​				`wsgi.py`   # 实现协议的

​		manage.py     # 这个文件  启动文件  管理文件  入口文件



我们经常去操作的文件:

​	urls.py

​	settings.py

启动项目:

​	python  manage.py的路径  runserver IP:端口

​							runserver 表示启动(命令)

启动后生成db.splite3 文件  是一个数据库文件可删



### 入门三板斧

##### 增加一个功能

​	1.增加对应关系

​	2.写一个视图函数



返回字符串

```
from django.http import HttpResponse

def index(request):
    return HttpResponse('index')
```



##### 返回html页面

​	1.创建templates文件夹,将html文件放在里面

​	2.`settings`里TEMPLATES中的`DIRS`:`[os.path.join(BASE_DIR,'templates')]`(写入templates路径)

通常只会写这一种

```
from django.shortcuts import render

def index(request):     	# request包含和请求相关的
    return render(request,'index.html')
```



##### 跳转

```
from django.shortcuts import redirect

def index(request):
    return redirect('https://www.baidu.com')
```



### Django app

随着视图函数越来越多 `Django`推荐用一个个的应用(`app`) 来表达

创建:   python manage.py startapp 名字

创建应用(文件夹)

`__init__`   这是个包

views.py     视图文件,写视图函数的(经常操作)



### Django流程

浏览器发一个请求流程



### 路由

1.`settings`里ROOT_`URLCONF`='  '表示在哪里找映射关系  即`urlpatterns`=[..]

推荐在`app`里的 views里写视图函数



2.在urlpatterns里path('xxx/')后面用<>包起来一个参数,

urlpatteerns 必须是列表,如果是集合就会报错

在views里定义xxx函数,形参request和那个参数,就可以直接使用那个参数,

参数名字必须一致



3.转换器在2里的<>里可以加入如`<int:id>`就可以不识别其他的类型了

转换器包括:   str(默认,非空,匹配任意)  int   slug(由英文中的横杠'-',或者下划线'_',连接英文字符或者数字而成的字符串)   uuid(匹配uuid字符串,即独一无二的随机字符)   path(匹配非空的英文字符串,可以包括斜杠)

根据主键的内容使用转换器限制



4.`query`,即`url`里?后面的,可以用参数request得到,方法:   `request.GET` ,得到一个字典,根据字典的键来得到值



5.奇怪的需求

比如:   只要4位数的数字     可以利用正则来实现    

```
from django.urls import re_path
urlpatterns = [
    re_path(r'year/(?P<year>[0-9]{4}$)',views.year)
]
# 和path用法一样,前面可以写正则表达式
```



6.指定默认参数   默认不传的时候为1

```
import xxx
urlpatterns=[
	path('book/',views.book),    # 只能再写一个指向同一个函数
	path('book/<int:id>',views.book)
]


def book(request,id=1):
	xxxx
```



7.路由分发      

任何的技术问题没有什么是加一层解决不了的,如果有那就加两层

拆分

项目越来越大代码多了    要考虑拆分

一个`app`里用一个文件专门写`url`映射

```
# app01/urls
from django.urls import path
from . import views
urlpatterns = [
    path('index/',views.index),
]

# django/urls
from django.urls import path,include
urlpatterns = [
    path('app01/',include('app01.urls')),
    # 所有和app01有关的都去app01/urls里找了
    # 相当于拼接
]
即:   http://127.0.0.1:8000/app01/index/
```



8.路由反转

跳转的时候, 跳转后的网页的url更改了   为了防止更改多个地方可以设置个名字

```
urlpatterns = [
    path('home/',views.index,name='index'),
    path('login/',views.login)    #  login函数跳转到index网页
]
# 设置名字后无论'home/'改成什么都可以直接跳转且跳转后的网址改变

from django.urls import reverse

def login(request):
	return redirect(reverse('index'))

def index(request):
	return HttpResponse(indexs)

浏览器输入127.0.0.1:8000/login 进入网址为home的indexs网站
```



```
# 跳转到有参数的网站
import ...

# urls
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',views.login),
    path('laos/<id>',views.lao,name='lao'),
]
# 输入login跳转到laos<id>

# views
def login(request):
    return redirect(reverse('lao',kwargs={'id':111}))

def lao(request,id):
    return HttpResponse(f'lao if={id}')
   
输入login跳转到laos/111
```

```
# 查询字符串的参数?后面的
# 只能通过字符串拼接实现

import ...

# urls
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',views.login),
    path('laos/<id>',views.lao,name='lao'),
]
# 输入login跳转到laos<id>

# views
def login(request):
    return redirect(reverse('lao',kwargs={'id':111})+ '?name=121')

def lao(request,id):
    return HttpResponse(f'lao if={id}')
   
输入login跳转到laos/111?name=121
```



9.

随着程序的完善,名字越来越多,所以用到了别名

但是别名也越来越多,程序是团队写的,多个人写更容易冲突

唯一的解决方式是任意的别名都是独一无二的

通常在别名前加应用名称app01_xxx,  low

Django推荐   在url里    urlpatterns前加一行

app_name = 'app01'

在view里   函数里   跳转时reverse后面加 app01:

return redirect(reverse('app01:lao')



### 报错

##### 端口错误

Error: [WinError 10013] 以一种访问权限不允许的方式做了一个访问套接字的尝试。

是指端口被占用,关闭端口的程序或换个端口即可



酷狗音乐是8000端口的   关闭酷狗音乐的后台即可



##### 页面错误

输入`http://127.0.0.1:8000/`后页面报错   Page not found(404)

第一次 没有输入路由的时候会返回主页(小火箭)  输入路由的时候就默认不是第一次使用,主页会报错



# Django的模板

### venv

黄色的文件夹     如果出现venv 文件夹说明创建了一个虚拟环境

相当于又安装了一个python



### 动态渲染HTML页面

本质: 用python操作文件  利用字符串的替换

模板语言   DTL



##### DTL

在html里  {{ }} 两个花括号里面写变量名

在view里函数里定义  变量=' xxxxx '   在返回值后写context={'html里的变量' : 函数里的变量}

如:   

html里    {{a}}

views里  def index(request):

​					a = 'aaaaa'

​					return render(request,'html路径',context={'a':a, })

结果:   显示 aaaaa



如果数据很多 可以在html里写很多值,在context里直接加



##### locals

会返回局部作用域下所有的名字 如

a = '22'

b='11'

...

return render(request,'html',locals())

会将a,b...全部显示



##### loader

from django.template import loader 

def xxx  :

temp = loader.get_template('html路径')

res = temp.render(locals())

return HttpResponse(res)

一般不用



##### 展示HTML页面

1.让Django知道HTML页面在哪里

​		1.在app里创建文件夹templates   (必须叫这个)

​		在文件夹里面创建html文件

​		2.创建一个文件夹,名字任意,一般还是叫templates,在哪里都可以,

​		在settings里告诉django    settings里的TEMPLATES中的DIRS:[os.path.join(BASE_DIR,'templates')]      (列表里可以写多个,默认只写一个)

​		django在查找模板的时候,  settings里的TEMPLATES中的DIRS列表依次遍历

如果DIRS里所有路径都找了,都没有,就会去INSTALLED APPS里所有的app里的templates找,还找不到就会报错(模板找不到)

如果'APP_DIRS'=False就不会找app里,(默认是True)



### app返回html

要显示app 里templates里 html页面   需要在settings里注册

在settings里的 INSTALLED_APPS=[ ]    里加入'app名字' 如 'app01'

(或者app01.apps.App01Config)    



### 名字冲突

在自己的app01里创建一个文件夹app01然后放入html   查找的时候查'app01/xxx.html' 就不会出现重名导致的问题

在templates里创建文件夹app01里放入html  就不会出现查找的时候重名的问题



### 模板的注释

模板的注释和html注释不一样

dtl  是将所有的内容读取然后字符串的拼接替换

注释:   {# 注释 #}  

快捷键:  Ctrl+/



dtl不止可以渲染字符串

字典, 列表, 函数(不能带括号,自动调用), 类(不能带参数), 等python中常用的变量都可以渲染

字典 可以在html里使用(.键)的语法,不能使用内置的方法名,如keys等, 如果使用了不存在的名字也不会报错

列表 可以使用(.索引)的语法

函数 绝对不能加参数,不会报错,没用

类 可以使用(.属性)的语法



django的模板

{{ 和具体的数据相关 }}

{% 和逻辑相关 %}      --> 称为标签



### 内置标签

##### 判断

{% if 666 %}   --> 转换bool值

​		{% elif  xx %}

​				xxx

​		{% else %}

​				xxx

{% endif %}

没有缩进要求



##### 循环

for ( 然后摁tab键 )

{% for foo in request %}

​		xxx

{% for foo in request  reversed%}   -->倒过来遍历

​		xxx

{{{ forloop.counter }}}

会展示出当前循环的所有索引值 , 1开始

{{ forloop.first}}

会判断当前循环是不是第一次,返回bool

{{ forloop.last}}

会判断当前循环是不是最后一次,返回bool

{% empty %}   

​	xxx			--> 遍历后没有元素会返回xxx

{% endfor %}   --> 结束

很接近python语法



##### a标签

添加app01里test的方法

`<a href="{% url 'app01:test' %}">点击</a>a>`



##### with标签

索引特别长的时候

使用with标签

{% with xxx.xx.x as a%}

{% with aa=xxx.xx.x%}

{{a}}

{{aa}}       -->输出结果相同为xxx.xx.x

{% endwith %}



##### verbattim标签

{% verbatim %}

{{xxx}}   			---> 输入{{xxx}}

{% endverbatim %}



### 过滤器

即函数

在模板中使用的函数

对数据进行操作  --> 函数



add , default , length ,   ......

{{  xxx|过滤器的名字:参数}}

{{xxx|add:3}}      --> 结果加3

{{xxx|default:参数}}		--> 如果xxx为空的时候赋值为参数

{{xxx|default_if_none:参数}}   --> 如果xxx为none是输入

{{xxx|length}}    --> 输入xxx的长度

{{xxx|data:"格式"}}       --> 按格式输出时间

views的函数里写: 	yijvhua='dsafdsafdsa'

{{yijvhua|truncatechars:5}} 		---> 如果超过指定的长度就会切割会拼接三个点作为省略号



### 自定义过滤器

1.app必须注册

2.在app里创建一个包 里面有`__init__`的文件夹 包必须叫templatetags   包里面创建python文件,名字随意  

3.文件里写

导入模块  from django import template

创建一个模板库对象  register = template.Library()

创建函数  def 名字(xxx,xx):      --> 必须有形参  xxx就是原来的数据本身,xx是传递的参数

​						return xxx

将函数注册到模板库中	 	register.filter('名字',名字)   		--> 左边是 使用时在|左边的名字,右边是函数名字,一般写成一样的避免误会

```
register.filter('名字',名字)
这行代码利用装饰器来实现
更推荐使用装饰器:
@register.filter(指定name)
```

使用: 	

{% load 文件名%}

使用



### 自定义标签

过滤器最多只能接受一个参数

想要接受多个参数

额外定义一个函数

1.app必须注册

2.在app里创建一个包 里面有`__init__`的文件夹 包必须叫templatetags   包里面创建python文件,名字随意  

3.文件里写

导入模块  from django import template

创建一个模板库对象  register = template.Library()

创建函数  def xxx(a,b,c)

​						return a+b+c

将函数注册到模板库中	 	register.simple_tag('名字',名字)			--> 左边是 使用时在|左边的名字,右边是函数名字,一般写成一样的避免误会

```
register.simple_tag('名字',名字)
这行代码利用装饰器来实现
更推荐使用装饰器:
@register.simple_tag(指定name)
```

使用: 	

{% load 文件名%}

使用



### 重复引用代码

一个html 文件多次使用

引入模板:

{% include '要引入的html的路径' %}

 路径是从templates开始找的



### django 是如何根据URL去查找关系的

本质:  遍历urlpatterns 列表,从上往下依次去找(会自动在后面拼接一个'/'),找到了就去执行对应的函数,就不再继续往下找了,全部都没找到就会报错

url中? 后面的是查询字符串不会参与路由的匹配



### 模板的继承

有的网站页面都差不多, 大量的html代码都相似, 差不多

```
模板的继承
继承

父模板  挖坑 函数 形参  面向对象 方法

字模板  填坑 函数 实参  面向对象 重写

一般设置3个坑
	1.head css js
	2.body
	3.js底部样式 title
挖坑:  
{% block title %} 父模板 {% endblock %}

{% block body %} 父模板的内容 {% endblock %}
定义了一个内容块
填坑:
{% extends '父模板的路径' %}   # 必须写在第一行

{% block title %} 字模板 {% endblock %}

{% block body %} 子模板的内容 {% endblock %}

坑多了之后会不明显
在endblock后写名字  title,body

{% block body %} {{ block.super }} 字模板的内容 {% endblock body %}
# 也想要父模板的内容,加上自己的内容

```



### 样式和js

##### css/js

1.写在html文件中    牵扯太多   不适合项目开发

2.写在一个单独的文件中   推荐  项目开发



存放位置:

static文件夹

连接css和js时,href和src后  路径从static开始找

如:   `<link rel="stylesheet" href=" /static/bootstrap/css/bootstrap.css">`



或 `<link src="stylesheet" href="{% static "bootstrap/css/bootstrap.css" %}">`

`# 在第一行加上{% load static %}`

也可以不加这一行, 换为在settings里:

TEMPLATES中 OPTIONS下 写: 

'builtins' :['django.templatetags.static']即可



在settings里  添加:

STATICFILES_DIRS = [

os.path.join(BASE_DIR,'static')

]

settings里  

当你的路由是static开头的 就会去STATIC_URL这个列表中的路径下去找文件

STATIC_URL = '/static/'





# django的视图

### 规定

没有位置的规定,  推荐写在应用的views.py中

有参数的规定,  必须至少有一个形参 , 推荐叫request

​		形参中保存了所有http请求相关的信息

有返回值的规定,  必须有返回值,  且返回值必须是HttpResponse的对象或者子对象

​		请求有规范,响应也有规范,  如果是上面的对象, 就会自动满足http规范



### 规则

请求相关:

必然和request形参有关联, request用 字典 数据类型保存更合适  类似字典的数据格式

取出数据时推荐使用.语法

基本规则

request.method       请求方法    结果是大写的请求方法

request.path		路由   不携带查询字符串

request.path_info		路由	只有路径参数这一部分 同上



request.GET		QueryDict 伪字典,  保存查询字符串参数  结果是个伪字典,是对象

​			当同一个参数有多个值   .get 方法只能取最后一个值

​			当有多个值时  .getlist 可以全部取到

​			递交表单的时候, 多个参数名字一样, (多选框) 只能用getlist

request.POST	post请求的数据 	表单中非文件的内容

### Forbidden(403)

post请求时    报错

出现的原因是csrf攻击  , web攻击手段

权限不够   403阻止访问

url已知  参数也已知   就可以通过爬虫发送请求

解决:   判断请求是不是自己的

​		在html里加入一行   {% csrf_token %}   自动将参数隐藏, 返回时自动判断



在settings里MIDDLEWARE中的 'django.middleware.csrf.CsrfViewMiddleware' 注释掉就不会出现报错     但是极其不安全		不建议

post请求必须有csrf验证



### 文件上传

必须是post请求 , 表单form标签加enctype="multipart/form-data"

接收文件:   post接收不到   要通过request.FILES.get('my_file')  接收

文件保存:   with open(my_file.name, 'wb') as fp:

​						for chuck in my_file.chunks():

​								fp.write(chuck)

### 接收字节

request.body	

将请求数据放到字节中,

原始的请求体数据bytes

Ajax提交数据



### 响应

##### HttpResponse

HttpResponse(content=响应体.content type=响应体数据类型, status=状态码)

 

##### json

data={'a':12}

JsonResponse(data)

自动将python数据类型转换成json数据类型

如果有中文想要进行展示:   JsonResponse(data,json_dumps_params={'ensure_ascii':False})

如果返回的非字典:     ,safe=False

JsonResponse继承与HttpResponse



### 类视图

之前所有的视图都是函数形式

只有get,post限制

通过类的方式来进行        比较推荐写类视图

类	 好处:

可以继承,	给函数加装饰器

获取url请求方式 --> 在类里找对应的请求方法

```
# 视图
class Index(View):
	# 任意的属性,方法   通常get post
	# 一旦涉及get请求, 会走到这里,
	# 更好的区分了请求方法的不同
	def get(self,request):
		return HttpResponse('get')
	def post(self,request):
		return HttpResponse('post')

# url
urlpatterns = [
	path('index',views.Index.as_view(),name=''),
	
]
```

```
# 装饰器   3种方式
# 1. 重写dispatch 方法
def dispatch(self,request,*args,**kwargs):
	print('开始')
	obj = super(Index,self).dispatch(request,*args,**kwargs)
	print('结束')
	
# 2. 通过django的一个模块去添加装饰器,加在函数上
from django.utils.decorators import method_decoratot

def deco(func):
	def wrapper(*args,**kwargs):
		print('这是装饰器')
		res=func(*args,**kwargs)
		return res
	return wrapper
@method_decorator(deco)
def get(xxx)
	xxx
	
# 3. 加在类上
@method_decorator(deco,name='dispatch')
class Index(View):
	xxx

所有的方法都加上了, 不常用
```



### 自定义错误页面

页面比较丑, 不想用默认的  可以自定义

前提:   必须关闭调试模式   --> 没有了报错相关信息



开发环境   需要看到错误信息,  去调试代码

生产环境   要实际上线了   错误信息绝对不能展示   防止被攻击



settings里:

DEBUG = False

ALLOWED_HOSTS = [ ] 	  如果为'*'  即允许所有的IP访问

调试模式为False  必须设置 哪些IP 允许访问

```
# 在templates中自定义错误页面
# 404.html
{% extends 'base.html' %}
{% block title %}404错误页面{% endblock title %}
{% block body %}404错误页面{% endblock body %}
```





# django的模型

处理和数据库相关的

MySQL  -->  关系型数据库

前提条件:    	安装好MySQL    

MySQL中创建database

django去操作数据库		--> 数据库已经建立好了

​	1. python去操作mysql		原生的方式

​	2. ORM的方式 	(重点,难点)

配置信息:  settings里

```
# 原
DATABASES={
	'default' : {
		'ENGINE':'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR,'db.splite3'),
	}
}
```

```
# 更改成mysql
DATABASES={
	'default' : {
	# 引擎
	'ENGINE':'django.db.backends.mysql',
	# 数据库的名字
    'NAME': 'test1',
    # 用户名
    'USER':'root',
    # 密码
    'PASSWORD':'zrzrzr',
    # host主机地址
    'HOST':127.0.0.1,
    # PORT端口
    'PORT':3306
	}
}
```

django 自带的数据库  sqlite3  小型数据库	实际项目中不会用

第一次使用会报错	django中使用mysql   需要先安装mysql的驱动

pymysql		纯python代码写的   可以和python代码更好的衔接	

mysqlclient		MySQL-python的分支  支持python3   c语言写的,效率更高

MySQL-python	c语言写的	只支持python2	旧 不用



使用mysqlclient:      pip install mysqlclient



使用pymysql:   需要额外的配置 1.安装   2. 在`__init__.py`里写:

import pymysql

pymysql.install_as_MySQLdb()

还报错   -->   修改django的源码 		不推荐



### ORM

1. 关系型数据库种类很多

2. 不同种类的关系型数据库   sql语言  不是一模一样的

3. 有的人写sql语句  写的不好   

   

切换数据库		很多代码需要更改		-->   orm诞生

object 				 对象

relationship  	 关系

mapping		    映射



好处:  

面向对象思想    	    数据库

  类    		-->			  	表

属性   		-->	 		字段

对象 		 -->			数据,记录

一一对应

1.自动化进行

2.不需要sql语句

3.更换数据库简便



缺点: 

1.慢		性能差距微乎其微

2.很复杂的sql语句   无能为力   高度定制化不行



### 操作数据库

##### 创建表

在对应app的models.py      	必须写在这里      必须注册

```
from django.db import models

class Book(models.Model):
    # 必须继承自models.Model
    # 自动创建表名 app名字_类名
    name = models.CharField(max_length=32)
    # 决定字段名   数据类型  varchar类型  最大长度
    # 按照规范 应该有个字段   主键  id
    # 按照规范的话就会自动创建主键的字段
    # 真正的创建数据表  1.app里的migrations的包用来存放数据迁移的文件的
    # 将代码转换成sql语句, 数据迁移的命令: python manage.py makemigrations
```

生成迁移文件    记录了你现在model的操作   日志   不会执行

方便复盘

执行:   	python manage.py migrate

pycharm专业版看数据库工具:

pycharm右边数据库   -->  加号  --> 数据源  --> mysql -->登录

可以看到创建了11张表  --> 注册app时 的所有app里的model也创建表了, 一共10个表



##### 属性的命名

遵守变量名的命名规范

不能使用连续的下划线__



##### 常用参数

```
from django.db import models

class Book(models.Model):
    name = models.CharField(max_length=32)
    # 什么类型的字段   很多
    #  AutoField     (Field字段)
    #  自增长  int  一般不写 django默认创建 id的主键字段
    # IntegerField   int 整型
    # FloatField   浮点
    # DecimalField   小数  (max_digits=6,decimal_places=2)  总位数6位,小数位2位
    # BooleanField	布尔(5.7中没有但是有tinyint,8.0中有)
    # CharField	   varchar  必须设置(max_length=32)最多32个字符
    # TextField   longText 保存大量文本数据 
    # FileField   文件上传字段  varcahr 
    # 上传一个文件1.变成二进制保存成mysql   2.将这些文件保存在某个地方,将路径保存在mysql 推荐 
    
    # DateField   日期    
    # TimeField   时间	
    # DateTimeField  日期加时间   多  
    # auto_now=True 和 auto_now_add=True 和 default参数三选一   
    # auto_now 保存数据的时候  使用当前的时间  修改时间
    # auto_now_add 第一次添加数据的时候 加入这个参数 使用当前时间  创建时间
    # default增加数据 给字段加个值, 不给加值的时候加默认值
    # 时间有时区的划分, django默认UTC(settings里的TIME_ZONE的值)(标准时与东八区时间差8h)(改为Asia/Shanghai)
    # settings里的USE_TS改为False 不然还会差8h
    
    # primary_key=True  设置主键
    # unique=True  设置唯一值
    # db_index  普通的索引   加快查询效率
    # null  设置允许为空
    # db_column   鸡肋 设置这个字段叫什么
    
    # 默认表名的取名:  应用名_表名小写
    # 不想叫这个名字:  再创建一个类 
    class Meta:			# 必须交Meta
    	db_table='book'  # 设置表名
    	ordering =['pirces']  # 设置排列字段
    	# ordering =['-pirces']  # 设置降序排列字段
    	
    	# select * from book order by pirces desc
    	
    	
    	# 后增加字段的时候为了防止出现错误(前面没加这个字段的值) 两个方法1.设置可以为空null(一般不用,影响查询效率)2.设置默认值
```

注意事项:    增加一个字段后   将一行字段注释代表删除这个字段

要想真正的在数据库中创建表,字段  需要的是 python manage.py migrate

python manage.py makemigrations  只是记录   和上一步的对比



### 数据迁移的回退

python manage.py migrate 应用名 0001 initial

不推荐,   对于数据表的创建 一开始就要确定好

会造成数据混乱





### 单表操作 

增加一条数据     		实例化一个类		orm的特点

简单测试

1.  交互式的环境 		-->  临时的

python manage.py shell

2. 永久的

   创建一个文件			让他和django产生关联

   ```
   import os
   
   os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'day7.settings')
   # manage.py  文件的第一行代码抄下来
   # 相当于导入了django的配置文件,  配置信息
   
   
   # 得到django
   import django
   django.setup()
   # 下面代码才能用上django
   
   
   from app01.models import Book
   # 这行代码放到后面
   
   ```

   

##### 增加数据

 orm操作  object  是models.Model提供的管理器

Book.objects.create(title='xxx',sales=666)



第二种

Book(title='aaa',sales=333).save()

很多的变形		--  面向对象的思想

```
res = Book(title='aa',sales=333)
res.save()

res = Book()
res.title = 'gg'
res.sales = 999
res.save()
```

orm 面向对象 简化



##### 查询数据

```
最基本的查询: 
select * from 表名
-->   Book.object.all()		--> 结果是个伪列表
# 查所有
# 在models里定义一个函数
    # def __str__(self):
        # return self.title
    # 让查询到的数据更好看	返回时执行
	# 返回的是一个QuerySet对象
	
# 查单条数据
Book.object.get(title='xxx')
# 注意: get只能用于一条数据  如果数据不是一条就会报错
# 只有一条数据  主键id
Book.object.get(pk=1)
# 不管有没有定义主键  pk自动带入主键名	推荐

# filter  查询
Book.object.filter(title='xxx')
# 返回的也是QuerySet对象
# 一般用filter查询  不管结果是多少条都不会报错
# 结果放在一个类似列表的数据中


```



```
QuerySet好处:   支持链式查询写法
# a = b.c.d.e ...
class A():
	sql = 'select a from table where a'
	age = 18
	name = ''
	def get_age(self):
		sql = 'select * from table where a'
		return self
	def get_name(self):
		name=''
		return self
		
a = A()
a.get_age().get_name().get)age()....

面向对象

支持列表的索引  --> [1] , [2:4] 
操作列表的索引一样的操作,但是不能使用负数索引

django 取第一行  .first()
django 取最后一行  .last()

```



```
#多个条件查询
# filter()里用,隔开

# 再来个.filter()

# filter 只能实现and
```



##### 删除数据

先找到数据

```
# res = Book.object.get(pk=1).delete()

# res = Book.object.get(pk=1)
# res.delete()

# 注意: res = Book.object.filter(xxx=xxx).delete()
# 由于filter可以查到多条数据  如果查出来的结果有多条 就等于批量删除数据
# .first().delete() 删第一条
# 用索引[] 删除中间的数据

# 结合实际 
```



##### 修改数据

先找到数据

```
res = Book.object.get(pk=1)
res.title = 'xxx'
res.save()

Book.object.filter(pk=1).update()  # 直接更改 常用与批量修改

Book.object.get(pk=1).update(title='xxx')  #错误,get得到的是值不能.update()使用
```



##### 重点查询

```
all()  select *   返回queryset

get()  查主键 结果不是一条就报错 

filter()  查询条件  where 字段=值 and 字段=值

first()  返回结果的第一条数据

last()  返回结果的最后一条数据

count()   统计有多少条结果

order_by()  根据字段去排序  字段前加-降序

exclude()  排除在外  和filter相反  鸡肋

values()  只获取某个字段

values_list()  返回结果是列表套元组 了解

distinct()  去重  一模一样的数据,带有主键的话是不一样的

reverse()  反转  必须先order_by().reverse()  鸡肋

existe()   判断能不能查出结果  结果True或False 鸡肋
```



```
Book.object.all().count()   #查一共多少条结果 结果是数字,可以指定条件
# 列表的len方法   可以有  但是不推荐

Book.object.order_by('sales')
# 根据某个字段排序 

Book.object.values('id')
# 结果类似列表里套字典,字典键是'id',值是具体数据

Book.object.values('titles')distinct()
# 只有'titles'重复就去除
```



```
# 根据条件查询

# 模糊查询
# 属性名称__运算符 = 值
# 包含
Book.object.filter(title__contains='xxx')
# 类似于like'% xx%'   不区分大小写   
# 通用:运算符前加i区分大小写

# 以xx开头 like'%xx'
Book.object.filter(title__startwith='xx')

# 以xx结尾 like'xx%'
Book.object.filter(title__endwith='xx')

# xx大于xx
Book.object.filter(sales__xx)
xx  gt  大于
xx  gte  大于等于
xx  lt  小于
xx  lte  小于等于

# xx是xx或者xxx
Book.object.filter(title__in=['xx','xxx'])
# 和or查询有区别   or可以指定不同的查询条件 

# 查询xx是处于1到999之间的数
Book.object.filter().filter()
Book.object.filter(xx__range=[1,999])  # 必须是数值字段   between and

# 时间相关
# 查询年份是2023年的数据
Book.object.filter(register_time__year='2023')
# 月  month
# 星期  week_day  周日是第一天 周五是6
# 注意  时区问题  在settings里USE_TZ 改为False

# 是否为空
Book.object.filter(title__isnull=True)
```





# 表关系

表关系依赖于外检字段

### 一对一 	

外键字段随便在哪边,一般在查询频率高的表里 	有外键字段的叫主表,没有的叫从表

```
# 作者表
class Author(models.Model):
    name = models.CharField(max_length=32)
    age = models.IntegerField()
    # 外键
    author_detail = models.OneToOneField('app01.AuthorDetail',on_delete=models.CASCADE)
    # 1.外键字段 _id 不需要会默认在 后面拼接一个_id
    # 2.OneToOneField   一对一字段   参数,和哪张表对应, on_delete表示数据被删除时怎么办
    # models.CASCADE 级联操作 数据一起被删除 同生共死  常用
    # models.PROJECT 收到保护  不能删除
    # SET_NULL  设置为null
    # DO_NOTHING  不做任何事
    # SET(值,函数)


# 作者详情表
class AuthorDetail(models.Model):
    phone = models.CharField(max_length=11)
    addr = models.CharField(max_length=32)

```

```
# 一对一的增删改查

# 增加数据
# 主表: 有外键字段的
# 先有一个文章详情
form appp01.models import Author,AutherDetail
res = AutherDetail.objects.create(phone='12121',addr='home')
# 根据实例对象添加
Auther.objects.creaete(name='xx',age=18,author_detail=res)
# 直接根据主键添加
Auther.objects.creaete(name='xx',age=18,author_detail=1)
# 或者下面的方式  更加灵活
author = Auther.objecct.get(pk=1)
author.author_detail = res
author.author_detail_id = res
author.save()
# 从表: 没有外键字段的


# 删除数据
Author.objects.get(pk=1).delete()
# 删除和修改  与单表操作没有区别


# 查询数据  不同  更加方便  主表查从表  .的方法
Author.objects.get(pk=1)  # 查出第一个作者
# 查phone
author.author_detail.phone
# .方法已经到达了author_detail 这张表了
# 链式查询的好处    面向对象


# 跨表查询
# 主表   外键字段__属性
author = Author.objects.filter(name='xx').first()
# 查phone=33的author
author = Author.objects.filter(author.detail__phone='33').first()
# 还可以继续拼__
author = Author.objects.filter(author.detail__phone__content='123').first()

# 查名字是xx的详情表
# 从表   没有外键字段   类名小写__属性
detail = Author.Detail.object.filter(author__name='xx').first()
detail.phone ...
# 作者姓名
detail.author.name
```





### 一对多(多对一)

 外键字段在多的一方

```
# 一对多   图书和出版社
# 规定  一个出版社可以出版多本书   一本书只能由一个出版社出版
# 主表(多的):	图书			从表:  出版社
```

```
class Book(models.Model):
	name = models.CharField(max_length=11)
	# 外键    一对多
	publish = models.ForeignKey('Publish',on_delete=models.CASCADE)
	
class Publish(models.Model):
	name = models.CharField(max_length=11)



from app01.models import Book,Publish
# 新增数据
res = Publish.objects.create(name='xxx')
# book = Book.objects.create(name='xxx',publish_id=1)
Publish.objects.create(name='xxx',publish=res)

# 新增或修改
book = Book.objects.get(pk=1)
book.publish = res
book.save()

# 删除和修改与单表操作没有区别

# 主表找从表
# 查出xxx书的出版社   	外键字段.
book = Book.objects.filter(name='xxx').first()
book.publish.name

# 查xxx出版社名字包含了xx的书   类名小写__属性
Book.object.filter(publish__name__content='xx')

# 从表找主表
# 关联的类名小写__set
publish = Publish.object.filter(pk=1).first()
publish.book_set.name.all()			# 一对多结果可能是多条 得到的结果是QuerySet对象  可以链式使用.filter方法
# 查书名有xxx的		类名小写__属性
publish = Publish.object.filter(book__name__contains='xxx').first
```



### 多对多

了解

通过第三张表来实现

```
# 演员和电影
# 外键放在哪里都可以 一般放在查询频率高的
```

```

查询   类名小写_setclass Actor(models.Model):
	name = models.CharField(max_length=11)
	duoduiduo = models.ManyToManyField('movies')
    # 外键  不需要加删除关系
    
class Movies(models.Model):
	name = models.CharField(max_length=11)
	

# 操作
# 和一对多相似
# 新增数据
from app01.models import Actors,Movies
# 主表
actor = Actors.object.create(name='xxx')   	# 有点区别  操作第三张表
movie = Movies.object.create(name='xxx')
actor.duoduiduo.add(movie) 			# 主表新增数据 新增各自的数据再进行关联 主键通过外键字段.add(另外一张表的对象)
# 从表 创建关联  并新增数据
movie.actors_set.create(name='xxx')		# 类名小写_set   QuerySet对象

# 删除
movie = Movies.object.filter(name='xxx').first()
actor = Actors.object.filter(name='xxx').first()
movie.actors.remove(actor)    # 删除对应关系

查询   类名小写_set
```





```
# 有个数据表  Book  有个字段 price
# 需求  给每一本书的价格+5
class Book(models.Model):
	price = models.IntegerField()
	class Meta:
		db_table = 'book'  # 表名叫book
```

### F表达式

### Q表达式

```
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'day9.settings')
import django
django.setup()

from app01.models import Book

# for i in range(1,5):
#     Book(price=i).save()

books = Book.objects.all()
# print(books)

# 以前
# for book in books:
#     book.price += 5
#     book.save()

from django.db.models import F   # 放在后面
from django.db.models import Q

# 简化  F表达式
# Book.objects.update(price=F('price')+5)    # F表达式

# 取主键id为1的结果的第一条数据
# book = Book.objects.filter(pk=1).first()

# 取主键id为1且价格是11的第一条数据
# book = Book.objects.filter(pk=1,price=11).first()

# Q表达式
# 取主键id为1或者价格大于11的第一条数据
# book = Book.objects.filter(Q(pk=1)|Q(price__gt=11)).first()  # 或
# print(book)

# 取价格不大于12的结果
# book = Book.objects.filter(~Q(price__gt=12)).first()  # 取反

# 取主键id为1且价格是11的第一条数据
# book = Book.objects.filter(Q(pk=1)&Q(price__gt=11)).first()  # 且
```



### 统计查询

```
# select count(*) from user;
# orm:
from django.db.models import Count,Max,Min,Avg,Sum
User.objects.aggregate(Count('id'))
User.objects.aggregate(Max('id'))
User.objects.aggregate(Min('id'))
User.objects.aggregate(Avg('id'))
User.objects.aggregate(Sum('id'))

# select type,count(id) from group by type;  # 分组查询
User.objects.values('type').annotate(Count('id'))

```



# django文件上传

```
# models.py

from django.db import models

class Book(models.Model):
	price = models.IntegerField()
	class Meta:
		db_table = 'book'  # 表名叫book



class Info(models.Model):
	name = models.CharField(max_length=32)
	desc = models.FileField(upload_to='info/%y%m%d')       # 保存的是文件存放的路径
    # upload_to表示设置文件上传后保存在哪里
    # 找settings  MEDIA_ROOT  这是文件上传的路径   会拼接upload_to后面的路径
    # 在settings里设置 MEDIA_ROOT = os.path.join(BASE_DIR,'media')
    # 以后所有上传的文件都在这个路径里面   年月日
    # 配合模型层使用的  商品 用户...

	# desc = models.ImageField(upload_to='image/%y%m%d')
	# 限制必须上传的是图片		好像不对没有限制
	# 必须安装好  pillow模块
```

```
# views.py

from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

# 文件上传   HTMl页面  表单  上传
from app01.models import Info


class InfoView(View):

    def get(self,request):
        return render(request,'app01/info.html')

    def post(self,request):
        # 接收上传的文件保存在服务端
        # 比较low的方式
        # myfile = request.FILES.get('myfile')         #接收
        # with open(myfile.name,'wb')as f:
        #     for chuck in myfile.chunks():
        #         f.write(chuck)

        # 快捷方式
        myfile = request.FILES.get('myfile')
        Info.objects.create(desc=myfile,name='zrzr')

        return HttpResponse('文件上传成功')
```

文件上传成功 --->  要展示出来

```
# index.html

{% extends 'base.html' %}
{% block title %} 文件上传 {% endblock title%}
{% block body %}
<div>
    <h1>展示图像</h1>
    <img src="路径" alt="">
</div>
{% endblock body %}


# views

def index(request):
    res = Info.objects.get(pk=2)
    return render(request,'app01/index.html',locals())
```

结果找不到图像路径

network里图片上传404

```
# settings


STATIC_URL = '/static/'    # 相当于一个令牌django看到就会去下面匹配 

# 配置静态资源的路径
STATICFILES_DIRS = [
    os.path.join(BASE_DIR,'static')
]

# 要加上这一条
MEDIA_URL = '/media/'	# 上传文件的url



# urls

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app01.urls'))
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)  
# 加入


# index.html

{% extends 'base.html' %}
{% block title %} 文件上传 {% endblock title%}
{% block body %}
<div>
    <h1>展示图像</h1>
    <img src="{{ res.desc.url }}" alt="">    # res.desc.url才能找到,比较繁琐   必须是.url
</div>
{% endblock body %}
```



### 文件下载download

```
# views


from django.http import HttpResponse, FileResponse
from day9 import settings

def download(request):
    res = Info.objects.first()
    # 拼接出文件的路径
    path = os.path.join(settings.MEDIA_ROOT,f'{res.desc}')
    res = FileResponse(open(path,'rb',))
    res['content_type'] = "application/octet-stream"
    res['Content-Disposition'] = f'attachment; filename={os.path.basename(path)}'
    return res
```



### cookie

http协议  --> 无状态     一个请求一个响应    需要登录的网页

让服务端去记住你是谁

cookie 存放在浏览器中    标记着你是谁你   没有任何安全措施  可以随意的修改查看

敏感信息  容易泄露		-->  有了session   

```
# views


def set(request):
    # 设置cookie
    # 对cookie的操作必须基于HttpResponse对象
    # 获取cookie
    # 删除cookie
    
    res = HttpResponse('cookie111')
    res.set_cookie('key','value',max_age=10)    # 设置/修改cookie
    request.COOKIES.get('key')                  # 获取cookie
    res.delete_cookie('key')                    # 删除cookie
    
    return res
```



### session

基于cookie			放在服务端

```
# views


def session(request):
    # 对session的操作
    # 注意: session是保存在服务端的   默认django将session保存在数据库中  所有要想操作session必须先执行数据迁移 表
    # 获取
    # 设置
    # 删除
    
    res = HttpResponse('session')
    data = request.session.get('key')
    # 判断一个session是否存在
    data = request.session.exists('key')
    # 设置依赖 的是request
    request.session.set_expiry(10)     # 设置过期时间  不设置默认设置两周自动过期
    request.session['key'] = 'value'
    request.session.clear()         # 清空所有数据   表中的数据不会删除
    request.session.flush()         # 删除数据表中的数据     推荐
    # session  依赖cookie  

    return res
```





# 组件



### 中间件

```
在浏览器中输入网址,敲下回车,看到了内容
流程:

浏览器向django项目发送请求  查找url  找不到就报错
发送给视图层  找到网页    发送给模型层  模型层向数据库(django项目外)请求数据
数据返回模型层  返回视图层  返回到模板层  经过处理后  返回到浏览器


浏览器 --> urls.py --> views.py --> models.py --> mysql --> models.py --> views.py --> templates --> 浏览器
```

```
# views

# 中间件  
# csrf_token   防止跨站伪造攻击的   本质 利用cookie和session来实现
#
# 请求来 加一些限制 做什么事情 做一些限制 响应走
# 写一些代码加限制
# 方式:  函数   类
# 写的位置随意
# 可以单独建立一个文件

# 利用中间件来做限制  
path_list = [
    '127.0.0.1',
    ]
# 闭包函数
def my(response):                   # 必须有个形参,响应
    def middleware(request):        # 必须有个形参,这个形参就是http请求的相关信息
        # 这里的代码都会在视图函数真正执行之前执行
        a = request.META['REMOTE_ADDR']  # 从request中取出访问我这个网站的ip
        if a in path_list:
            return HttpResponse('您的ip可能是爬虫,被封了')
        res = response(request)     # 当这行代码执行,就表示真正的执行了视图函数
        # 这里的代码都会在视图函数真正执行之后执行,并且是在返回响应之前执行
        print('finish')
        return res
    return middleware
```

```
# 利用类来实现
class My:
    def __init__(self,response):
        self.response = response
    def __call__(self, request):
        # 这里的代码都会在视图函数真正执行之前执行
        a = request.META['REMOTE_ADDR']  # 从request中取出访问我这个网站的ip
        if a in path_list:
            return HttpResponse('您的ip可能是爬虫,被封了')
        res = self.response(request)  # 当这行代码执行,就表示真正的执行了视图函数
        # 这里的代码都会在视图函数真正执行之后执行,并且是在返回响应之前执行
        print('finish')
        return res
```



```
# settings

MIDDLEWARE = [
	
	
	
    'app01.views.my',    # 路径 my是函数名
]
```



### admin后台管理组件

django提供的对模型的增删改查的方法

不要过于依赖

后台管理!  

客户: 买东西  orm语句

商家: 上架商品 定价 admin

用处不同   

```
# admin.py

from app01.models import Book,Publish

admin.site.register(Book)
admin.site.register(Publish)
# 设置中文
# settings
LANGUAGE_CODE = 'en-us'  # 英文
LANGUAGE_CODE = 'zh-hans' # 中文
TIME_ZONE = 'UTC'   # 时区
TIME_ZONE = 'Asia/Shanghai' # 中国时间
# 改完时间 这个要改为False
USE_L10N = False

# 字段中的参数  verboss_name='名字'  # admin中变为中文
# 后面加
def __str__(self):
	return self.name
```

```\
创建超级用户
python manage.py createsuperuser	
输入用户名,邮箱,密码
```





```
# 显示中文

# __init__.py

default_app_config = 'app01.apps.App01Config'



# models.py

class App01Config(AppConfig):
    name = 'app01'
    verbose_name = '图书系统的管理'
    
# apps.py

class Book(models.Model):
    name = models.CharField(max_length=32)
    price = models.IntegerField()
    publish = models.ForeignKey('Publish',on_delete=models.CASCADE)
    class Meta:
        verbose_name = '书'
        verbose_name_plural = verbose_name

class Publish(models.Model):
    name = models.CharField(max_length=32)
    addr = models.CharField(max_length=32)
    class Meta:
        verbose_name = '出版社'
        verbose_name_plural = verbose_name
```



```
# 可以使用 django


# 在settings里注册app中
import 
INSTALLED_APPS = [
	'simpleui',   			# 一定要在admin前面   功能是一样的 只是页面好看了
	'django.contrib.admin',
	xxx
]
```

```
# 高度的定制化
# admin.py
class BookAdmin(admin.ModelAdmin):
	list_display = ['name','price','publish']  		# 展示name,price,外键
	search_fields = ['name','price']   		# 搜索框
	list_display_links = ['name','price']  	# 点击跳转
	list_per_page = 10      	# 数据多的时候 每页展示多少条 默认展示100条  分页的效果
	
admin.site.register(Book,BookAdmin)
admin.site.register(Publish)
	
```



### auth组件

```
# app 数据库迁移  生成10张表  原理: settings里找app models.Model
# 网站中什么是重要的:  用户数据  
# 
# 用户注册   -->  没有用户注销   -->  您的用户已注销 --> 数据库里的数据没删
# 用户注册  登录  改密码  验证  退出登录 很通用的功能
# django  默认自带  上面的功能
# auth组件
# 
# python manage.py migrate  创建表  其中auth_user为django生成的
# 可以帮助快速用简单的代码实现用户相关功能
```



```
# views

# 使用
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
def index(request):
    # 1.注册用户
    # User.objects.create_user('zrzr','2857901781@qq.com','123456')  # 用户名 邮箱(可无) 密码
    # 用户名唯一索引  不能重复使用,会报错      密码  自动加密
    # 2.修改密码
    # user = User.objects.get(pk=1)   # 找到对象
    # user.set_password('321123')     # 修改密码,对密码加密
    # user.password = '321231'        # 也可以修改密码, 不能,这样密码就是明文了没加密,登录验证通不过
    # 3.登录验证   判断是否能登录成功
    # 登录成功  返回用户对象
    # 登录失败  返回为None
    res = authenticate(username='zrzr',password='123456')
    print(res)
    # 保持登录  本质: 设置一个cookie让服务端知道你登录过了  记住你
    # 登录成功后应该设置一个cookie 或session 让浏览器得到一个标志
    # 可以这么写
    # res = HttpResponse('首页')
    # res.set_cookie('zrzr',True)
    # 可以简化
    login(request,res)  # 本质 会给你设置一个cookie将你的用户模型对象加入到request中
    # logout(request)   # 只需要写一个logout 就可以注销  注销后返回user为AnonymousUser 匿名用户
    # 所以  你在任何地方都可以直接操作request, 得到你的用户对象了
    
    return HttpResponse('index')
def info(request):
	print(request.user)    		# 在任何地方都可以使用user
    return HttpResponse('info')
```

```
# 不足:  字段已经定义好了
# 头像, 电话号, 地址 ...
# 1. 再建一张表 进行一对一关联
# 2. 拓展用户模型  去models.py


# models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
# 如果是拓展用户模型   必须继承自 AbstractUser
class UserInfo(AbstractUser):
    phone = models.CharField(max_length=11)
# auth 组件是django默认自带的   想用你拓展的  必须 告诉django
# 去settings


# settings.py

# 告诉django使用自己拓展的用户模型类
# AUTH_USER_MODEL = 'app名字.模型类名'
AUTH_USER_MODEL = 'app01.UserInfo'

# 执行数据迁移     会报错  拓展用户模型会改变django自带的auth模型的结构
# 如果想自定义拓展用户模型  必须在第一次migrate时就确定好
# auth_user 已经创建好了,再去拓展就会报错
# 删除时 所有app下的migrations文件夹里除了__init__ 其他全部删除
# 

# 第一件事   先确定好数据库  表 字段 规范
# 字段 表名 表关系  不能改了

```





# Redis

```
mysql 核心作用:  存取数据
关系型数据库
有点:
	可以更好的存储数据
	数据和数据之间可以存在关联
弊端:
	读写性能差 	性能弊端出现    数据太大	
	本质:  文件 --> 电脑硬盘  读写性能低	
	
	
sql产品
	关系型数据库  mysql  性能瓶颈问题  (盘io导致)
nosql产品
	本质:据库  存取数据    数据和数据间没有关系
	性能快很多   使用内存	基于内存
	弊端:  丢失  不能永久保存  
Redis   持将数据保存在外存中  两者相结合
		存取数据快  支持数据持久化  只能存取简单结构数据
数据放mysql  常用简单的数据放Redis中 作为缓存 加快查询速度
	数据结构 key:value 键值对  基本结构  只能存放这种
	速度: 写入8.1w/s   读取11w/s
```

```
# redis使用


# 修改redis.windows.conf配置文件

# 将239行的dir \ 修改成自己的路径 
# 设置数据默认存放位置   请确保这个路径是已经存在的
dir D:\Redis_data  

# 设置redis密码 443行
# requirepass foobared
requirepass zrzrzr

# 找到redis安装路径 输入cmd  输入这行指令
redis-server --service-install redis.windows.conf --loglevel notice --service-name Redis

# 将redis加入到Windows服务中
# 环境变量   略

# cmd管理员运行
net start redis
redis-cli -a zrzrzr
```

```
学习Redis相关命令

redis-cli -a 密码 -p 默认端口是6379 -h ip默认是127.0.0.1
如果没有密码 也可以进入 但是没权限 做不了任何事情
测速redis 成功连接
ping
得到PONG 成功

exit 或者quit  退出
命令不区分大小写 推荐大写
redis 有16个数据库  0-15  默认使用0号库  切换库  select 索引
redis 对数据采取键:值 形式保存   redis所有的数据类型指的都是值的数据类型
string list hash set zset 五大数据类型 常用string
操作数据类型的方法很多  一般就用string
string:
	增: set 键 值
		append a 666
		自增  incr a
		自减  decr a
		指定字长  incrby a 100
		setex 键 秒数 值 设置一个键,同时设置过多少秒就被删除
		mset 键 值 键 值 同时设置多个键值对
	删: del 键
		可以删多个 空格隔开
	改: set 键 值
		有就改 没有就新建
	查: get 键
		支持正则表达式 
		查看是否存在  exit xx  存在1 不存在0
		查看类型  type 
		mget 键 键 键  同时获取多个键
   	切换数据库: select 索引
	查看当前库下都有哪些键: keys *
	
	设置过期时间  expire a 6   (秒)
	查看有效时间  ttl a    	 (秒)
	清除当前库中的所有数据(慎用)  FLUSHDB
	删除所有库中的所有数据(慎用)  FLUSHAL
```

```
# list类型
# 元素是字符串类型
# 列表头尾增删快 中间增删慢 增删元素是常态
# 元素可重复
# 最多可包含 2^32 -1 个元素
# 索引同python列表

LPUSH 键 值1 值2 值3
# 从左边插入数据 返回list长度
RPUSH 键 值1 值2 值3
# 从右边插入数据 返回list长度
LINSERT 键 BEFORE 现有元素 新元素
LINSERT 键 AFTER 现有元素 新元素
# 在指定元素前插入新元素  成功返回列表长度 没有找到返回-1 不存在或为空 返回0
LRANGE 键 start stop			0 -1   [1:3]

# 获取列表长度   		LLEN 键
# 从列表左侧头部弹出一个元素     LPOP 键
# 从列表右侧尾部弹出一个元素  	RPOP 键

# 设置指定索引位置的元素值
# 索引从左侧开始 第一个元素为0
# 索引可以是负数 表示尾部开始计数
LERT 键 索引 值
```

```
hash类型		数据类型	
1.由field和关联的value组成的键值对
2.field和value是字符串类型
3.一个hash中最多包含2^32-1个键值对

hset 键 name zr	 # 设置一个字段
hmset 键 name zr  # 设置多个字段
hlen 键  # 返回字段个数
hexists 键 # 判断键是否存在 
hget 键 # 获取值
hkeys  # 返回所有键 
hvalues # 返回所有值
```

```
set类型    无序集合  自动去重
sadd  键名 数据 数据
snumber 键名  # 查看数据
srem 键 数据 数据  # 删除一个或者多个元素 不存在自动忽略
sismember 键 数据 # 元素时候存在
srandmember 键 数量 # 随机返回集合中的数据  默认一个
spop 键 # 删除数据

zset类型   有序集合
多了一个权重
```

### python 操作redis

```
# 下载模块 
pip install redis
```

```
import redis
# 创建Redis连接对象
# decode_responses 默认为False,得到的结果为字节类型
# 设置为True，则为字符串类型
# conn = redis.Redis(password='491521',decode_responses=True)

# 更好的方式
# 使用connection pool来管理对一个redis server的所有连接，
# 避免每次建立、释放连接的开销。
# 默认，每个Redis实例都会维护一个自己的连接池。
# 可以直接建立一个连接池，然后作为参数Redis，
# 这样就可以实现多个Redis实例共享一个连接池

# 拿到一个redis的连接池
pool = redis.ConnectionPool(password='491521',decode_responses = True,max_connections=10)
# 从池子中拿一个链接
conn = redis.Redis(connection_pool=pool)
print(conn)
# 字符串类型的操作
conn.set('name', 'laoyang', 60)
print(conn.get('name'))
conn.mset({'a':'a1','b':'b1'})
print(conn.mget(['a','b']))
conn.append('a','追加')
print(conn.get('a'))
conn.set('laoyang',18)
conn.incr('laoyang')
print(conn.get('laoyang'))
conn.incrby('laoyang',10)
print(conn.get('laoyang'))
conn.decr('laoyang')
print(conn.get('laoyang'))
conn.decrby('laoyang',10)
print(conn.get('laoyang'))

# 键命令
print(conn.delete('a'))
print(conn.keys('*'))
print(conn.exists('a'))
```

### `pipeline`操作`redis`

`Redis`的` C - S `架构：

- 基于客户端-服务端模型以及请求/响应协议的`TCP`服务。
- 客户端向服务端发送一个查询请求，并监听`Socket`返回。
- 通常是以阻塞模式，等待服务端响应。
- 服务端处理命令，并将结果返回给客户端。

存在的问题：

- 如果`Redis`服务端需要同时处理多个请求，加上网络延迟，那么服务端利用率不高，效率降低

管道`pipeline`

- 可以一次性发送多条命令并在执行完后一次性将结果返回。
- `pipeline`通过减少客户端与`Redis`的通信次数来实现降低往返延时时间。

实现的原理

- 实现的原理是队列。

- `Client`可以将三个命令放到一个`tcp`报文一起发送。

- `Server`则可以将三条命令的处理结果放到一个`tcp`报文返回。

- 队列是先进先出，这样就保证数据的顺序性

  

  ```
  # 批量执行redis命令，减少通信io
  import redis
  
  # 1. 创建连接池并连接到redis
  pool = redis.ConnectionPool(password='491521',decode_responses = True,max_connections=10)
  conn = redis.Redis(connection_pool=pool)
  # 2. 创建Redis管道
  pipe = conn.pipeline()
  # 3. 将Redis请求添加到队列
  pipe.set('fans',50)
  pipe.incr('fans')
  pipe.incrby('fans',100)
  # 4. 执行请求
  pipe.execute()
  ```

  

  
