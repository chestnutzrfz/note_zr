# 爬虫介绍

爬虫有成网络蜘蛛,主要功能是抓取网络数据,用程序模拟人使用浏览器访问网站,并保存下来处理.

分为两类:  通用网络爬虫,聚焦网络爬虫

### 通用网络爬虫

是搜索引擎的中啊哟组成成分,百度搜索引擎,其实可以更形象的称为百度蜘蛛.需要遵守robots协议

`robots协议:  一种"约定俗成"的协议,不具备法律效力,全凭自觉,"君子协议"`

### 聚焦网络爬虫

面向特定需求的一种网络爬虫.会对网页内容筛选保证只抓取与需求相关的网页信息.





# 网页获取流程

- 浏览器会根据URL发送http请求给服务端

- 服务端接收到http请求后进行解析

- 服务端处理请求内容,组织响应内容

- 服务端将响应内容以http响应格式发送给浏览器

- 浏览器接受到响应内容,解析展示

  



# URL

URL即统一资源定位符,每一个URL只想一个资源,可以是一个HTML页面,一个css文档,一个js文件,一个图片等等.

URL语法格式为:

`protocol://hostname[:port]/path[?query][#fragment]`

htttp协议:

- protocol:  网络传输协议
- hostname:  只存放资源的服务器的域名或IP地址
- port:  是一个可选的整数,取值范围是0-65535.如果port被省略是就使用默认端口,如http的默认端口是80,https的端口是443
- path:  路由地址,由零个或多个/符号隔开的字符串,路由地址决定了服务端如何处理这个请求
- query:  从?开始到#为止,它们之间的部分就是参数,又称搜索部分或者查询字符串.这个部分允许有多个参数, 参数与参数之间用&作为分隔符.

绝对URL和相对URL:  我们上面看到的是一个绝对的URL,还有个叫相对URL.如果URL的路径部分以'/'字符开头,则浏览器将从服务器的顶端根目录获取该资源.常出现在网页的超链接中.





# HTTP协议

HTTP协议是超文本传输协议的缩写,http协议主要作用是要服务器和客户端之间进行数据交互(相互传输数据).https协议是安全超文本传输协议,https是http协议的安全版,对传输数据进行加密.

### http协议特点

无连接:  无连接意味着每次连接处理一个请求,服务器返回后断开连接,节省传输时间和服务器压力.

http协议是一个无状态的协议,同一个客户端的这次请求和上次请求没有对应

### HTTP请求

请求行:  具体的请求类别和请求内容

```python
GET          /         HTTP/1.1
请求类别    请求内容    协议版本
```

请求类别:   每个请求类别表示要做不同的事情

在http协议中,定义了八种请求方式.主要了解两种常用的请求方式:get和post

get:   从服务器获取数据下来,并不会对服务器资源产生任何影响的时候会使用get请求

post:   向服务器发送数据(登录),上传文件等,会对服务器资源产生影响的时候会使用post请求

### 请求头

对请求的进一步解释和描述

Referer:  表面当前这个请求是从哪个url过来的.这个一般也可以用来做反爬虫技术.如果不是从指定页面过来的,那么就不做相应的响应.

User-Agent:   请求载体的申根标识, 这个在网络爬虫中经常会被使用到.请求一个网页的时候,服务器通过这个参数就可以知道这个请求是通过 哪种浏览器发送到.如果我们是通过爬虫发送请求,那么我们的User-Agent就是pythoin,这对于那些有反爬虫机制的网站来说,可以轻易的判断你这个请求是爬虫.因此我们要经常设置这个值为一些浏览器的值,来伪装我们的爬虫.

Cookie:   对应的是一个用户的信息,http协议是无状态的,也就是同一个人发送了两次请求,服务器没有能力知道这两个请求是否来自同一个人.因此这个时候就用cookie来做标记.

请求体:   提交的内容



# HTTP响应

响应行:   反馈基本的响应情况

```python
HTTP/1.1    200       OK
版本信息     响应码   附加信息
# 常见的响应状态码
200: 请求正常,服务器正常的返回数据
301: 永久重定向
302: 临时重定向,比如在访问一个需要登录的页面的时候,而此时没有登录,那么就会重定向到登录页面
400: 请求的url在服务器上找不到.换句话说是请求url错误
403: 服务器拒绝访问,权限不够
500: 服务器内部错误
    
    服务器可以自定义返回的状态码
```

响应头:   对响应对象的描述

Content-Length:  服务器通过这个头,告诉浏览器回送数据的长度

Content-Type:   服务器通过这个头,告诉浏览器回送数据的类型



响应体:   响应的主体内容信息





# 爬虫流程

1.确定好要爬什么数据

2.确实需要爬取的URL地址

​	静态网页,数据是固定的

​	动态网页,数据不是固定的,通过JavaScript加载Ajax

3.由请求模块想URL地址发出请求,并得到网站的响应

4.从响应内容中提取所需数据

5.存储





# 控制台抓包

打开浏览器,f12打开控制台,找到network选项卡

控制台常用选项: 

​	network:   抓取网络数据包

​	all:   抓取所有的网络数据包

​	xhr:   抓取异步加载的网络数据包

​	js:   抓取所有的js文件

sources:   格式化输出并打断点地哦啊是JavaScript代码,助于分析爬虫中一些参数

抓取具体网络数据包后:  单机左侧网络数据包地址,进入数据包详情,查看右侧





# request模块的安装

`pip install request`

第三方源:

```python
清华：https://pypi.tuna.tsinghua.edu.cn/simple
阿里云：http://mirrors.aliyun.com/pypi/simple/
中国科技大学 https://pypi.mirrors.ustc.edu.cn/simple/
华中理工大学：http://pypi.hustunique.com/
山东理工大学：http://pypi.sdutlinux.org/
豆瓣：http://pypi.douban.com/simple/
```

```python
pip install request -i https://pypi.tuna.tsinghua.edu.cn/simple
```



# requests.get()

该方法用于get请求,表示想网站发起请求,获取页面响应对象:

```python
response = requests.get(url,headers=headers,params,timeout)
```

url:   要抓取的url地址

headers:  用于包装请求头信息

params:   请求时携带的查询字符串参数

timeout:   超时时间,超出时间会抛出异常





# HttpResponse响应对象

我们使用Requests模块想一个URL发起请求后会返回一个HttpRequest响应对象

响应对象属性: 

text:  获取响应对象字符串类型

content:   获取到响应对象bytes类型(抓取图片,音频,视频文件)

encoding:   查看或者指定响应字符编码

request.headers:   查看响应对象的请求头

cookies:   获取响应的cookie,经过了set-cookie动作返回cookiejar类型

json():   将json字符串类型的响应内容转换为python对象





# 数据提取

### json于jsonpath

##### json

json是一种轻量级的数据交换格式,可以将JavaScript对象表示的一组数据转换为字符串格式,以便于在网络中传输这个字符串.并且在需要的时候,还可以将它转换为编程语言所支持的数据类型

|   python   | `json` |
| :--------: | :----: |
|   `dict`   | object |
|    list    | array  |
|   `str`    | string |
| int, float | number |
|    True    |  true  |
|   False    | false  |
|    None    |  null  |

python语言内置了专门处理json数据的模块json模块,通过该模块就可以完成json与python两种数据格式的相互转换.

|      方法      |                         作用                         |
| :------------: | :--------------------------------------------------: |
| `json.dumps()` |         将 Python 对象转换成 `JSON` 字符串。         |
| `json.loads()` |         将 `JSON `字符串转换成 Python 对象。         |
| `json.dump()`  |  将 Python 中的对象转化成`JSON`字符串储存到文件中。  |
| `json.load()`  | 将文件中的 `JSON` 字符串转化成 Python 对象提取出来。 |

##### jsonpath模块

jsonpath是一种信息提取类库,是从json文档中抽取指定信息的工具,提供多种语言实现版本.



### 正则表达式

按照一定的规则从每个字符串当中匹配到我们想要的数据

r_list = re.findall('正则表达式',html,re.S)

re.S让.可以匹配任何字符

##### 元字符

| 元字符 |           含义           |
| :----: | :----------------------: |
|   .    | 任意一个字符（不包括\n） |
|   \d   |         一个数字         |
|   \s   |         空白字符         |
|   \S   |        非空白字符        |
|   []   |        包含[]内容        |
|   *    |      出现0次或多次       |
|   +    |      出现1次或多次       |

(.*?) 匹配任意字符(除了换行符)

##### 贪婪匹配和非贪婪匹配

贪婪匹配: 匹配重复的元字符,总是尽可能多的向后匹配内容.

非贪婪匹配:让匹配重复的元字符尽可能少的向后匹配内容.



##### 正则表达式分组

将每个圆括号中子模式匹配出来的结果提取出来

1.先按整体正则匹配,然后再提取分组()中的内容

2.在网页中想要什么内容就加()

3.如果有两个及以上分组(),则结果中以元租形式显示			[(),(),()]



### lxml

lxml是Python的第三方解析库,完全使用Python语言编写,对xpath表达式提供了良好的支持,能够高效的解析HTML/XML文档.

xpath即为XML路径语言, 他是一种用来确定XML文档中某部分位置的语言,同样适用于HTML文档的检索.

pip install lxml

##### 使用

导入模块:  from lxml import etree 

创建解析对象:  parse_html = etree.HTML(html)

解析对象调用xpath:  r_list = parse_html.xpath('xpath语法')

##### xpath语法

在xpath中,HTML文档是被作为节点树来对待的.树的跟被称为文档节点或者根节点.

| 表达式 |                            描述                            |
| :----: | :--------------------------------------------------------: |
|   //   | 从匹配选择的当前节点选择文档中的节点，而不考虑它们的位置。 |
|   /    |  如果是在最前面，表示从根节点选取。否则某节点下的某个节点  |
|   @    |                     选取某个节点的属性                     |
| text() |                         选取文本。                         |

谓语:谓语用来查找某个特点的节点或者包含某个指定的值的节点,被嵌在方括号中.

|         表达式          |                      描述                       |
| :---------------------: | :---------------------------------------------: |
|   /bookstore/book[1]    |  选取属于 bookstore 子元素的第一个 book 元素。  |
| /bookstore/book[last()] | 选取属于 bookstore 子元素的最后一个 book 元素。 |
|     //title[@lang]      |   选取所有拥有名为 lang 的属性的 title 元素。   |



### Beautifulsoup

和lxml一样,Beautifulsoup4也是一个HTML/XML的解析器,主要的功能是解析和提取HTML/XML数据.

安装:pip install bs4

由于BS4解析页面是需要依赖文档解析器,所以还需要安装lxml作为解析库.

##### 常见对象

Beautifulsoup4讲html文档转换成一个属性结构,某个节点都是Python对象.

tag:是HTML中的一个个标签.我们可以利用soup加标签名轻松地活动这些标签的内容,这些对象的类型是bs4.element.Tag.但是主要,它查找的是在所以内容中的第一个符合要求的标签.

NavigableString:如果拿到标签后,还想获取标签中的内容.那么可以通过tag.string获取标签中的文字

string:获取某个标签下的非标签字符串.返回来的是个字符串.如果这个标签下有多行字符,那么就不能获取到了

strings:获取某个标签下的子孙非标签字符串.返回来的是个生成器.

stripped_strings:获取某个标签下的自三非标签字符串,会去掉空白字符.返回来的是个生成器.

##### find和find_all

find:找到第一个满足条件的标签就返回.

find_all:将所有满足条件的标签都返回.

在提取标签的时候,第一个参数是标签的名字.然后如果在提取标签的时候想要使用标签属性进行过滤,那么可以在这么方法中通过关键字参数的形式,将属性的名字以及对应的值传过去.或者是使用attrs属性,将所有的属性以及对应的值放在一个字典中创给attrs属性.

有些时候,在一起标签的时候,不想提取那么多,那么可以使用limit参数.限制提取多少个.

##### select方法

使用css选择器的语法找出元素.

通过标签名查找:

soup.select('a')

通过类名查找:

soup.select('.sister')

通过id查找:

soup.select("#link1")

组合查找:

soup.select("p #link1")

通过属性查找:

soup.select('a[href=""]')



# 保存

### MySQL

##### pymysql

- 建立数据库连接:  db = pymysql.connect(...)

  - 参数host:连接的mysql主机,如果本机就是'127.0.0.1'
  - 参数port:连接的mysql主机的端口,默认是3306
  - 参数database:数据库的名称
  - 参数user:连接的用户名
  - 参数password:连接的密码
  - 参数charset:通信采用的编码方式,推荐使用utf8

- 创建游标对象:  cur = db.cursor()

- 游标方法:  cur.execute("insert....")

- 提交到数据库或者获取数据:  db.commit()

- 关闭游标对象:  cur.close()

- 断开数据库连接:  db.close()

  

##### peewee

peewee是Python标出语言下的一款ORM框架.O是object,也就是对象的意思.R是relation,关系的意思,也就是关系数据库中数据表的意思,M是mapping是映射的意思.在ORM框架中,它帮我们把累和数据表进行了 一个映射,可以让我们通过类和类对象就能操作它所对应的表中的数据.ORM框架还有一个功能,它可以根据我们设计的累自动帮我们生产数据库中的表,生气了我们自己建表的 过程.

安装:pip install peewee

```python
from peewee import *

db = MySQLDatabase("spider", host="127.0.0.1", port=3306, user="root", password="123456")


class Person(Model): 
    name = CharField(max_length=20)
    birthday = DateField(null=True)

    class Meta:
        database = db  # This model uses the "people.db" database.


if __name__ == '__main__':
    from datetime import date

    db.create_tables([Person])
```

字符类型:

|      字段类型       |  `MySQL`   |
| :-----------------: | :--------: |
|  `BigIntegerField`  |  `bigint`  |
|   `IntegerField`    |    int     |
| `SmallIntegerField` | `smallint` |
|    `FloatField`     |   Float    |
|    `DoubleField`    |   Double   |
|   `DecimalField`    |  Decimal   |
|     `CharField`     | `varchar`  |
|  `FixedCharField`   |    char    |
|     `TextField`     |    text    |
|     `BlobField`     |    blob    |
|   `DateTimeField`   | `DateTime` |
|     `DateField`     |    Date    |
|     `TimeField`     |    Time    |

##### Excel

Python内置模块中没有提供处理Excel文件的模块,需要安装第三方模块

openpyxl,集成python操作Excel的相关功能

pip install openpyxl

```
from openpyxl import load_workbook

# 拿到Excel
workbook = load_workbook("pyxl.xlsx")

# 获取sheet
# 1 获取到所有的sheet名
# print(workbook.sheetnames)
# 2. 选择sheet
# sheet = workbook["Sheet1"]
# print(sheet)
# 基于索引获取
sheet = workbook.worksheets[0]
# print(sheet)
#
#
# for name in workbook.sheetnames:
#     sheet = workbook[name]
#     cell = sheet.cell(1, 1)
#     print(cell.value)

# 获取到单元格
# cell = sheet.cell(1,1)
# cell = sheet["c1"]
# print(cell.value)

# 
# for row in sheet.rows:
#     print(row[1].value)
```

