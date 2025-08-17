# scrapy

## scrapy基本流程

1. 在需要生成scrapy项目的位置打开文件夹进入cmd控制台

2.  创建scrapy项目

    ```python
    >>> scrapy startproject 项目名
    >>> cd 项目名
    >>> scrapy genspider 爬虫名 域名
    ```

3. 启动scrapy爬虫

    ```python
    1. scrapy 项目执行: scrapy crawl 爬虫名
    2. 在scrapy的根目录创建python文件
    写入:
    from scrapy import cmdline
    cmdline.execute("scrapy crawl 爬虫名".split())
    只需执行该文件即可启动scrapy爬虫
    ```

## scrapy爬虫文件构成

### spider(爬虫名)

新创建的spider中有以下内容:

```python
import scrapy


class LearningSpider(scrapy.Spider):
    name = "learning"	# 爬虫名
    allowed_domains = ["jy.hrbnu.edu.cn"]	# 允许爬取的域名,可为空
    start_urls = ["http://jy.hrbnu.edu.cn/frontpage/hrbnu/html/recruitmentinfoList.html?type=1"]
	# 起始url 创建的时候写的
    def parse(self, response):
        pass	# 自己添加parse方法
```

### items

```python
class LearnScrapy1Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()	# 可以添加例如这行代码, 让scrapy中的文件都可以使用这个中间件,可以暂存数据 方便在多个文件中传递   定义数据结构
    pass
```

### middlewares

使用中间件需要在settings.py中配置

```python
DOWNLOADER_MIDDLEWARES = {
    'myproject.middlewares.CustomDownloaderMiddleware': 543,
}
```

#### 下载中间件

下载器中间件用于处理scrapy的request和response的钩子框架，可以全局的修改一些参数，如代理ip，header等

使用下载器中间件时必须激活这个中间件，方法是在settings.py文件中设置DOWNLOADER_MIDDLEWARES这个字典，格式类似如下：

```python
DOWNLOADERMIDDLEWARES = {
    'myproject.middlewares.Custom_A_DownloaderMiddleware': 543,
    'myproject.middlewares.Custom_B_DownloaderMiddleware': 643,
    'myproject.middlewares.Custom_B_DownloaderMiddleware': None,
}
```

数字越小，越靠近引擎，数字越大越靠近下载器，所以数字越小的，`processrequest()`优先处理；数字越大的，`process_response()`优先处理；若需要关闭某个中间件直接设为`None`即可

##### user-agent中间件

```python
from faker import Faker

class UserAgent_Middleware():

    def process_request(self, request, spider):
        f = Faker()
        agent = f.firefox()
        request.headers['User-Agent'] = agent
```

##### 代理IP中间件

```python
class Proxy_Middleware():

    def process_request(self, request, spider):

        try:
            xdaili_url = spider.settings.get('XDAILI_URL')

            r = requests.get(xdaili_url)
            proxy_ip_port = r.text
            request.meta['proxy'] = 'https://' + proxy_ip_port
        except requests.exceptions.RequestException:
            print('获取讯代理ip失败！')
            spider.logger.error('获取讯代理ip失败！')
```

- `process_response(request, response, spider)`
    当请求发出去返回时这个方法会被调用，它会返回 
    1.若返回Response对象，它会被下个中间件中的process_response()处理
    2.若返回Request对象，中间链停止，然后返回的Request会被重新调度下载
    3.抛出IgnoreRequest，回调函数 Request.errback将会被调用处理，若没处理，将会忽略
- `process_exception(request, exception, spider)`
    当下载处理模块或process_request()抛出一个异常（包括IgnoreRequest异常）时，该方法被调用
    通常返回None,它会一直处理异常
- `from_crawler(cls, crawler)`
    这个类方法通常是访问settings和signals的入口函数

#### spider中间件

spider中间件用于处理response及spider生成的item和Request

启动spider中间件必须先开启settings中的设置

```python
SPIDER_MIDDLEWARES = {
    'myproject.middlewares.CustomSpiderMiddleware': 543,
    'scrapy.spidermiddlewares.offsite.OffsiteMiddleware': None,
}
```

- `process_spider_input(response, spider)`
    当response通过spider中间件时，这个方法被调用，返回None
- `process_spider_output(response, result, spider)`
    当spider处理response后返回result时，这个方法被调用，必须返回Request或Item对象的可迭代对象，一般返回result
- `process_spider_exception(response, exception, spider)`
    当spider中间件抛出异常时，这个方法被调用，返回None或可迭代对象的Request、dict、Item

### pipelines

管道文件。接收数据(items)  进行持久化操作

Pipeline是一个独立的模块,用于处理从Spider中提取的Item对象,实现对数据的进一步处理、存储和清洗等操作

持久化流程：

①　爬虫文件爬取到数据解析后，需要将数据封装到items对象中。

②　**使用yield关键字将items对象提交给pipelines管道，**进行持久化操作。

③　在管道文件中的process_item方法中接收爬虫文件提交过来的item对象，然后编写持久化存储的代码**，将item对象中存储的数据进行持久化存储（在管道的process_item方法中执行io操作,进行持久化存储）**

④　settings.py配置文件中开启管道

#### 在settings.py中配置

```python
ITEM_PIPELINES = {
    'myproject.pipelines.ExamplePipeline': 300,
    'myproject.pipelines.AnotherPipeline': 200,
}
```

较小的优先级值表示更高的优先级，Pipeline将按照优先级顺序依次处理Item对象。

为了优化性能，可以在配置中调整Pipeline的优先级，将最耗时的处理放在最后执行，从而提高整体速度

### settings

#### 设置全局变量

​		在settings.py文件中，我们可以定义一些全局变量，这些变量在整个爬虫过程中都可以使用。例如，我们可以定义一个USER_AGENT变量，用来设置请求的User-Agent头信息：
USER_AGENT = 'xxxx'

#### 配置下载延迟

​		在settings.py文件中，可以通过设置DOWNLOAD_DELAY参数来配置下载延迟，以控制爬取速度。DOWNLOAD_DELAY的单位是秒，可以设置为1或更大的值。例如：
DOWNLOAD_DELAY = 1

#### 配置UA池

​		为了防止网站对爬虫的识别，我们可以设置一个User-Agent池，让每个请求随机选择一个User-Agent进行发送。可以在settings.py文件中设置USER_AGENT_POOL，如下所示：
```python
USER_AGENT_POOL = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebK...
]
```

然后，在Spider中随机选择一个User-Agent进行请求发送：

```python
from scrapy import Spider
from scrapy.utils.project import get_project_settings
from scrapy.utils.httpobj import urlparse_cached

class MySpider(Spider):
    name = 'my_spider'
    def __init__(self, name=None, **kwargs):
    self.settings = get_project_settings()

def start_requests(self):
    # ...
    yield scrapy.Request(url, headers={'User-Agent': self.settings['USER_AGENT_POOL'][random.randint(0, len(self.settings['USER_AGENT_POOL'])-1)]})
```

#### 设置代理

如果需要通过代理来进行爬取，可以在settings.py文件中设置PROXIES参数。例如：

```python
PROXIES = [
    'http://proxy1.example.com:8888',
    'http://proxy2.example.com:8888',
    'http://proxy3.example.com:8888',
]
```

然后，在Spider中随机选择一个代理进行请求发送：

```python
from scrapy import Spider
from scrapy.utils.project import get_project_settings
from scrapy.utils.httpobj import urlparse_cached

class MySpider(Spider):
    name = 'my_spider'
    def __init__(self, name=None, **kwargs):
    self.settings = get_project_settings()

def start_requests(self):
    # ...
    yield scrapy.Request(url, meta={'proxy': self.settings['PROXIES'][random.randint(0, len(self.settings['PROXIES'])-1)]})
```

#### 其他爬虫相关配置项

在settings.py文件中，还可以设置其他的爬虫相关配置项，如日志级别、保存路径、爬取深度等。以下是一些常见的配置项：

##### 日志级别
LOG_LEVEL = 'INFO'

##### 爬虫名称
BOT_NAME = 'my_bot'

##### 爬取深度限制
DEPTH_LIMIT = 3

##### 是否遵循robots.txt
ROBOTSTXT_OBEY = True

##### 是否启用缓存
HTTPCACHE_ENABLED = True

##### 缓存过期时间
HTTPCACHE_EXPIRATION_SECS = 0

##### 缓存存储路径
HTTPCACHE_DIR = 'httpcache'

##### 缓存存储方式
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
这些只是settings.py文件中一些常见的配置项，你可以根据需要添加或修改更多的配置项。以下是更多可能用到的配置项：

##### 开启并配置自定义的扩展

Scrapy框架允许开发者编写自定义的扩展来增强爬虫的功能。在settings.py文件中，可以通过EXTENSIONS参数来启用和配置这些扩展。例如，启用并配置自定义的扩展MyExtension：
EXTENSIONS = {
    'myextension.MyExtension': 500,
}

##### 配置重试次数

在爬虫过程中，可能会发生请求失败的情况，可以通过配置RETRY_TIMES和RETRY_HTTP_CODES参数来控制自动重试的次数和HTTP响应状态码。例如，设置最大重试次数为3次，仅在遇到500和502的情况下进行重试：
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502]

##### 配置并发请求数量

通过并发发送请求可以提高爬取效率，可以通过配置CONCURRENT_REQUESTS参数来设置同时发送的请求数量。例如，设置同时发送10个请求：
CONCURRENT_REQUESTS = 10

##### 配置下载器中间件和爬虫中间件

Scrapy框架提供了下载器中间件和爬虫中间件，用于在请求和响应的处理过程中进行自定义的操作。可以通过配置DOWNLOADER_MIDDLEWARES和SPIDER_MIDDLEWARES参数来启用和配置这些中间件。例如，启用并配置自定义的下载器中间件MyDownloaderMiddleware和爬虫中间件MySpiderMiddleware：

```python
DOWNLOADER_MIDDLEWARES = {
    'myproject.middlewares.MyDownloaderMiddleware': 543,
}
SPIDER_MIDDLEWARES = {
    'myproject.middlewares.MySpiderMiddleware': 543,
}
```

##### 配置请求头信息

可以通过设置DEFAULT_REQUEST_HEADERS参数来配置默认的请求头信息。例如，设置Referer和Cookie：

```python
DEFAULT_REQUEST_HEADERS = {
    'Referer': 'http://www.example.com',
    'Cookie': 'session_id=xxxxx',
}
```

##### 配置是否启用重定向

可以通过配置REDIRECT_ENABLED参数来控制是否启用请求的重定向。例如，禁用重定向：
REDIRECT_ENABLED = False

##### 配置去重过滤器

Scrapy框架内置了去重过滤器，用于过滤已经爬取过的URL。可以通过配置DUPEFILTER_CLASS参数来选择使用的去重过滤器。例如，使用基于Redis的去重过滤器：
DUPEFILTER_CLASS = 'scrapy_redis.dupefilter.RFPDupeFilter'
