# 0.1安装pycharm

```
官网: 	https://www.jetbrains.com/pycharm/download/
安装时全选
```

<img src="https://img-blog.csdnimg.cn/img_convert/4756750710efe4562c985522bdca4cd2.jpeg" alt="image-20230521115448712" style="zoom: 67%;" />

### 0.2安装python

```
官网:  https://www.python.org/downloads/release/python-378/
根据自己电脑选择
一定要添加环境变量
```



# 1.安装django

```
# terminal里
pip install django==2.2 -ihttps://pypi.tuna.tsinghua.edu.cn/simple

# 离线下载
```

# 2.创建django项目

```
# terminal里
django-admin startproject 项目名
```

# 3.启动项目

```
# terminal里
python manage.py的路径 runserver IP:端口
```

# 4.创建一个应用

```
# terminal里
python manage.py startapp app名
```

### 4.1修改app下的views.py

```
# views.py里
from django.http.response import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse('ok1')

def abc(request):
	return HttpResponse('abc1')
	
# 返回文本
```

### 4.2新建app下的urls.py

```
# 在新建的app下新建一个叫urls.py的文件    里面写

from django.urls import path
from . import views


app_name = 'app01'

urlpatterns = [
    path('index/',views.index),
    path('abc/',views.abc),
]

```

### 4.3修改项目名下的urls.py

```
# 在项目名下的urls.py下修改

from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('app01/', include('app01.urls')),
]

# 新建的app名字叫做app01,相当于所有在app01中的url都去app01/下找
```

### 4.4运行

```
运行后
在地址栏输入http://127.0.0.1:8000/app01/abc
即可看到abc1
```

# 5.数据库model

```
# 修改app下的models.py
from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)   # 最大值为255,必须有最大值
    price = models.FloatField()				
    qty = models.IntegerField()
    memo = models.CharField(max_length=2083)

# 创建名为Product的表,  有四个字段 
```

# 6.注册app

```
# 在项目名\settings.py中添加app

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app01',					# 添加,app名字相同
]
```

# 7数据库ORM

```
可以更改使用的数据库,使用python的语言  --> 创建数据表(使用sql语言)

django 自带的数据库  sqlite3  小型数据库	实际项目中不会用
如果用sql语言写,更换一次数据库就需要更换所有的sql语句
```

```
在terminal中执行python manage.py makemigrations
生成迁移文件    记录了你现在model的操作   日志   不会执行

在terminal中执行python manage.py migrate
将代码转换成sql语句, 数据迁移的命令
```

```
# 在app里的models.py文件中添加
# 再创建一个表

class Offer(models.Model):
    code = models.CharField(max_length=10)
    description = models.CharField(max_length=255)
    discount = models.FloatField()
```

# 8.Admin管理

```
# 在terminal中
python manage.py createsuperuser

# 输入username和password
```

### 8.1修改admin.py

```
# 在app的admin.py中修改

from django.contrib import admin
from .models import Product

# Register your models here.
admin.site.register(Product)


# 运行后 在127.0.0.1:8000/admin/中就可以看到Product了,点add即可添加商品
```

### 8.2定制admin

```
# 显示商品列表 修改app下的admin.py

from django.contrib import admin
from .models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','price','qty')
# Register your models here.
admin.site.register(Product,ProductAdmin)
```

### 8.3练习增加Offer

```
# 在admin.py中

from django.contrib import admin
from .models import Product,Offer

class OfferAdmin(admin.ModelAdmin):
    list_display = ('code','discount')
    
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','price','qty')
# Register your models here.


admin.site.register(Product,ProductAdmin)
admin.site.register(Offer,OfferAdmin)
```

# 9.处理用户界面html

```
# 在项目名下创建templates文件夹
# 在templates下创建index.html文件

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
	<h1>Products</h1>
    <ul>
        <li>Item 1</li>
        <li>Item 2</li>
        <li>Item 3</li>
    </ul>
</body>
</html>
```

### 9.1修改app里的views.py

```
# 在settings里修改
# settings里TEMPLATES中的DIRS:[os.path.join(BASE_DIR,'templates')](写入templates路径)
```

```
# 在views.py中

from django.shortcuts import render


def index(request):
    return render(request,'index.html')
    
# 返回templates/index.html的html代码
```

### 9.2把商品参数传进来

```
# 修改app里的views.py

# Create your views here.
from django.shortcuts import render
from .admin import Product

def index(request):
    products = Product.objects.all()
    return render(request,'index.html',{'products':products})

# 将Products中的数据传到html中
```

### 9.3DTL语句

```
#DTL语句
### 动态渲染HTML页面

本质: 用python操作文件  利用字符串的替换

模板语言   DTL

在html里  {{ }} 两个花括号里面写变量名

在view里函数里定义  变量=' xxxxx '   在返回值后写context={'html里的变量' : 函数里的变量}

如:   

html里    {{a}}

views里  def index(request):

				a = 'aaaaa'

				return render(request,'html路径',context={'a':a, })

结果:   显示 aaaaa

django的模板

{{ 和具体的数据相关 }}
{% 和逻辑相关 %}      --> 称为标签
```



```
# 修改项目下的templates\index.html

    <ul>
        {% for product in products %}
            <li>{{ product.name }} (${{ products.price }})</li>
        {% endfor %}
    </ul>
    
# 将product中的数据传到html中
```

### 9.4模板的继承

```
# 到templates文件夹下创建一个base.html

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

{% block body %} {{ block.super }} 子模板的内容 {% endblock body %}
# 也想要父模板的内容,加上自己的内容
```

```
# base.html

{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    {% block body %} {% endblock %}
    <link rel="stylesheet" href="/static/csss/image.css">
    <h1>Products</h1>
    <ul>
        {% for product in products %}
            <li>{{ product.name }} (${{ product.price }})</li>
            <img class="image" src="{% static product.memo %}" alt="">
        {% endfor %}
    </ul>

</body>
</html>
```

```
# index.html

{% extends "base.html" %}
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    {% block body %} {{ block.super }} body的内容 {% endblock %}

</body>
</html>
```

### 9.5显示图片

```
# 在项目下创建名为'static'的文件夹

在settings里  添加:

STATICFILES_DIRS = [
os.path.join(BASE_DIR,'static')
]

# 添加static的路径
```

```
# 在index.html里添加

{% load static %}
<img src="{% static product.memo %}" alt="">

# 将product中的memo值传到html中,显示图片
```

### 9.6样式的修改

```
css/js  样式    -->  对html语句的修饰 更加美观

1.写在html文件中    牵扯太多   不适合项目开发

2.写在一个单独的文件中   推荐  项目开发

存放位置:

static文件夹

连接css和js时,href和src后  路径从static开始找

如:   <link rel="" href="/static/...">  	# href里是css文件的位置

或 <link src="" href="{% static "bootstrap/css/bootstrap.css" %}">
# 在第一行加上{% load static %}
```

```
# 在index.html中添加

<link rel="stylesheet" href="/static/csss/image.css">
# 给img标签加一个类
<img class="image1" src="{% static product.memo %}" alt="">
```

```
# 在static文件夹中创建一个csss文件夹 下创建一个image1.css文件 添加

.image {
  max-width: 500px;
  max-height: 500px;
  overflow: hidden;
  object-fit: cover;
  display: inline-block;
  vertical-align: bottom;
}
# 来限制图片的大小
```

# 10.局域网访问

```
# 修改settings.py
ALLOWED_HOSTS=['*']


# 使用python manage.py runserver 0.0.0.0:8000

使用其他同在一个局域网内的设备就可以访问了
打开windows命令行，输入ipconfig查看一下服务器ip
然后再你的设备上，打开浏览去，输入服务器ip地址:8000/products
比如我的服务器ip是192.168.1.41,则在其他同局域网内设备浏览器地址栏输入
192.168.1.41:8000/products即可看到我们刚刚做的网页
```





