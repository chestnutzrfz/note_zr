# 框架介绍

scrapy框架是python当中的爬虫框架.也是python中并发性能最高的爬虫框架.



安装:

- pip install wheel

- 下载twisted:https://www.lfd.uci.edu/~gohlke/pythonlibs/#twisted

- 进入到下载路径直接pip install 下载的文件名

- pip install pywin32

- pip install scrapy

  

1.爬虫项目启动,引擎想爬虫组件要其实的url,交给调度器去人队列

2.通过下载器帮我们发送请求,得到相应对象

3.返回给引擎,引擎给到爬虫组件

4.下载得到的相应对象 给到爬虫组件

5.爬虫组件对数据进行提取

​	1.数据交给管道去进行存储

​	2.还需要的根据的uel再次给调度器入队列 再发送			  		  	请求





# scrapy命令

1  文件路径栏输入cmd 打开cmd窗口,输入`scrapy startproject 项目名`创建爬虫项目



2  进入spiders文件夹输入cmd 打开cmd窗口,输入`scrapy genspider 爬虫名(爬虫文件名字) 域名(要爬的根网页路径)`

```
>>> scrapy startproject spiders
>>> cd spiders
>>> scrapy genspider 爬虫名 域名
```



3.1  scrapy项目执行: scrapy crawl 爬虫名

3.2  在有scrapy.cfg文件的文件夹里创建python文件(叫run,start都可以)   文件里写:

```python
from scrapy import cmdline

cmdline.execute("scrapy crawl 爬虫名".split())
# 爬虫名是spiders文件夹里的爬虫名
# .split() 是固定写法,
```

直接在pycharm里执行run文件即可





# 爬虫文件



### spiders文件夹里的爬虫文件

1.allowed_domains = ['域名']

只爬取这个域名里的网页,可以改为空

2.start_urls = ['域名']

起始url

3.在类中添加函数处理爬取到的数据

可以用item(先打开)(先from xx.itemsimport xxItem)来保存当前的数据

然后使用yield方法处理,

item = xxItem(名字 = 数据)   # 名字是item里创建的

yield scrapy.Request(  url,  callback=xxx,   meta={"item": item}   )

再次发送get请求, 目标url,  callback回调函数(在下面再创建一个函数xxx处理这次请求得到的数据),  meta是携带的数据

可以多次重复这个过程处理数据,最后得到数据后可以保存在item里然后yield item即可在piplines里下载数据





4.在yield scrapy.Request()里

可以添加请求头(headers=xxx)

可以添加请求体(body=json.dumps(data))  # data为请求体(字典)

可以添加方法(method='POST')即可发送post请求







### setting文件(配置文件)

1.ROBOTSTXT_OBEY = False

指的是爬虫遵不遵循robot协议,True改为False    直接注释

2.LOG_LEVEL = 'ERROR'

指执行爬虫代码只返回错误提示,不返回日志

3.加入请求头

```python
from fake_useragent import UserAgentUSER_AGENT = UserAgent().random
# 随机
```

或者在DEFAULT_REQUEST_HEADERS={}里加入请求头

4.item_pipelines

使用item

```
ITEM_PIPELINES = {
   'xxxxxxx': 300,
}
# 300指的是优先级不需要改
# 直接取消注释就行
```

5.DOWNLOAD_DELAY = 3

增加(0.5，1.5)* DOWNLOAD_DELAY 的随机延时处理

6.





### item

在item文件里的类中添加  

名字 = scrapy.Field()

即可在爬虫中使用这个中间件





### middlewares

xx



### pipelines

下载管道

先打开ITEM_PIPELINES

```
class LjPipeline:
    def open_spider(self, spider):
        self.f = open('xx.txt', 'w', encoding='utf-8')
        # open_spider(self,spider) 固定写法不		能改
        # 打开文件开始写

    def process_item(self, item, spider):
        print(item)  # 输出item显示下载速度
        self.f.write(
            json.dumps(dict(item), ensure_ascii=False) + '\n'
        )  
        # 将item转为字典又转为json文件
        # ensure_ascii=False将中文从ASCII码转			为汉字
        self.f.flush()
        # 写完后立即就会往磁盘里写，打开文件就会看见自己写的内容，优点也就是快速写入硬盘文件中
        # 将缓存区的文件写入磁盘

        return item
        # 固定写法

    def close_spider(self, spider):
        self.f.close()
        # 关闭文件


```





# scrapy + selenium



### 导包item

```
from wangyinews.items import WangyinewsItem
	第二层.item 				Item的类名
```



### 使用selenium

```
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class xxxspider(scrapy.Spider):
	def __init__(self):
        self.urls = []

        chrome_options = Options()  # 启用一个配置文件
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")  # 将谷歌修改为无可视化界面
        # 将selenium伪装为一个无头模式
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])

        # 驱动selenium
        self.browse = webdriver.Chrome(options=chrome_options)
```



### 中间件

```
# middlewares.py

# 4.2 开始篡改下载中间件的reposne
class WangyinewsDownloaderMiddleware:
	xxx
	    def process_response(self, request, response, spider):
        # 4.3 该方法可以拦截引擎发送出去的响应对象（url + status + body）

        # 下载器传递给Spider的响应对象
        # request：响应对象对应的请求对象
        # response： 当前方法拦截到的响应对象
        # spider： 像爬虫文件中对象的爬虫类提出要求

        print('0000',request.url)
        # 4.4 判断是否是四大新闻链接
        if request.url in spider.urls:
            # 4.5 获取爬虫文件中的selenium对象
            browse = spider.browse
            # 4.6 selenium像链接发请求
            browse.get(request.url)
            # 下拉
            browse.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            time.sleep(1)
            # 4.7 获取渲染后的源码
            page_text = browse.page_source
            # 4.8 将selenium渲染等到的源码打包给引擎
            '''
            url: 响应体对应的
            body:响应体（响应源码）
            request:scrapy中的请求对象，数据都是跟着请求走的
            '''
            new_reponse = HtmlResponse(url=request.url,body=page_text,encoding='utf-8',request=request)
            return new_reponse
        else:
            return response      # 这里等同于返回未篡改前的response
```



### item

```
# item.py

class xxxItem(scrapy.Item):
	name = scrapy.Field()
```

```
# spider.py

item = xxxItem()
            item['title'] = titles	# 在item里写入数据
            item['url'] = urls		# ['']里的必须在item.py里写入
            yield scrapy.Request(url=urls,callback=self.parse_content,meta={"ite":item})	# 请求url   # 回调函数   		# meta携带的数据 ite自己定

yield item     # spider.py 写到函数的最后
```



### 快捷使用

```
from scrapy import cmdline

if __name__ == '__main__':
    cmdline.execute(['scrapy','crawl','spider'])
    # 直接在当前文件右击运行即可
```



### xpath

```
.extract()
将selector对象转换为list内容
```

