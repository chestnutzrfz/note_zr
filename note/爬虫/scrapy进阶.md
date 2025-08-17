# scrapy进阶

#### scrapy使用

1 文件路径栏输入cmd 打开cmd窗口,输入scrapy startproject 项目名创建爬虫项目
2 进入spiders文件夹输入cmd 打开cmd窗口,输入scrapy genspider 爬虫名(爬虫文件名字) 域名(要爬的根网页路径)

> scrapy startproject spiders
>cd spiders
> scrapy genspider 爬虫名 域名

3.1 scrapy项目执行: scrapy crawl 爬虫名
3.2 在有scrapy.cfg文件的文件夹里创建python文件(叫run,start都可以) 文件里写
>from scrapy import cmdline
>cmdline.execute("scrapy crawl 爬虫名".split())
#爬虫名是spiders文件夹里的爬虫名
#.split() 是固定写法,

#### scrapy 爬虫文件外部快捷启动

一般启动
from scrapy import cmdline
cmdline.execute("scrapy crawl xx".split())    # xx为爬虫文件名

##### 定时启动

```
from apscheduler.schedulers.blocking import BlockingScheduler
import subprocess
def start_scrapy():
	subproccess.Popen('scrapy crawl xx')		# 生成一个新的进程 避免进程冲突
#创建定时任务对象
s = BlockingScheduler(timezone='Asia/Shanghai')
#添加一个定时任务
s.add_job(start_scrapy,'interval',seconds=10)  		# 时隔10s运行
s.add_job(start_scrapy,'date',run_date='2024-02-07')	# 固定日期运行
s.add_job(start_scrapy,'cron',hour=22,minute=30,second=30)		# 固定时间运行
s.start()  		# 启动任务对象
```

###  scrapy 爬虫文件中使用yield

 ```
 yield scrapy.Request(
	 url=xx, 		# 指向指定再次发送请求的url
	 headers=xx,			# 构造headers
	 body=xx,			# 构造新请求的请求体
	 method=‘post’,			# 不写默认request请求
	 callback=xx 			# 设置回调函数
	 meta=｛“item”：item｝	# 设置回调函数携带的数据
	 )
 ```

## scrapy settings文件中的设置

 - ROBOTSTXT_OBEY = False			# 一般改为False   让爬虫不支持robots协议 
 - LOG_LEVEL = 'ERROR'			# 让pycharm中仅显示发生的错误   忽略警告
 - ITEM_PIPELINES = {  'XX.pipelines.xxPipeline':300,}		# 启用scrapy中的指定item文件 如果需要使用item必须启用
 - USER_AGENT = UserAgent().random			# 先导包，让爬虫中未指定的useragent为随机值（仅一次爬虫中都一样）
 - DOWNLOAD_DELAY = 1 		# 增加(0.5，1.5)*DOWNLOAD_DELAY 的随机延时处理，伪装一下防止被识别为爬虫
 - REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
正常settings都有
 - DEFAULT_REQUEST_HEADERS={} 		# 所有的headers都可以写在里面  accept,accept-Language,referer等
- 使用redis必须要有的配置
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
SCHEDULER_PERSIST = True
REDIS_URL = "redis://127.0.0.1:6379"
ITEM_PIPELINES = {
	......
   'scrapy_redis.pipelines.RedisPipeline': 400,
}
```
# 设置过滤器 不设置的话就是scrapy本身的（Set）
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# 设置调度器  （scrapy_redis和redis数据库做交互）
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

# 下载管道
ITEM_PIPELINES = {
    'xxxxxx.pipelines.RedisPipeline': 300,        # redis管道
    # "xxxxxx.pipelines.TestScrapyRedis1Pipeline": 300,
}
REDIS_START_URLS_AS_SET = False     # 默认False
SCHEDULER_PERSIST = True
REDIS_HOST = 'localhost'        # 连接redis
REDIS_PORT = 6379
```
- 在middlewares中使用自己的cookie
COOKIES_ENABLED = True      # 用自己的cookie  放到middlewares中的process_request中   字典形式
```
class TestScrapyRedis1DownloaderMiddleware:
    def process_request(self, request, spider):
        request.cookies = {'bid': 'vIYuSYn4rw8', ....}
```
>将cookie转换为字典形式
cookie_str = 'xx'    # 从浏览器中取cookie
cookie_dict = {cookie.split('=')[0]: cookie.split('=')[1] for cookie in cookie_str.split('; ')}
### 在scrapy中使用redis

设置好settings
spiders中

```
import scrapy
from demo_58.items import Demo58Item_zufang,Demo58Item_ershou
from scrapy_redis.spiders import RedisSpider,RedisCrawlSpider

class SpiderSpider(RedisSpider):		# 继承RedisSpider
    name = "spider"
    allowed_domains = ["58.com"]
    # start_urls = ["http://58.com/"]
    redis_key = 'spider58:start_urls'		# 设置key
```

### scrapy中使用CrawlSpider

```
import scrapy
from scrapy.spiders import CrawlSpider, Rule

class LianjiaSpider(CrawlSpider):		# 继承CrawlSpider
    name = "lianjia_"
    allowed_domains = ["lianjia.com"]
    start_urls = ["https://hrb.lianjia.com/zufang/pg1"]

    rules = (
	    # 使用Rule规则
        # 翻页参数  https://hrb.lianjia.com/zufang/pg2/
        Rule(LinkExtractor(allow=r'/zufang/pg[0-2]/$'), callback="parse_url"),		# 回调函数处理得到的数据
        Rule(LinkExtractor(allow=r'/zufang/HRB\d+.html'), callback="parse_data"),
             )
```

##  在scrapy中使用RedisCrawlSpider

 设置好settings
 在spiders 中

 ```
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import RedisCrawlSpider

class CrawlFengkuangSpider(RedisCrawlSpider):
    name = "crawl_fengkuang"
    allowed_domains = ["ifeng.com"]
    # start_urls = ["http://app.finance.ifeng.com/list/stock.php"]
    redis_key = 'ifeng:start_url'

    rules = (
        # 解析列表页数据 - 详情页url      翻页
        Rule(LinkExtractor(allow=r"\?t=ha&f=amount&o=desc&p=\d+"), callback="parse_url", follow=True),
        # 解析详情页数据 - 具体数据
		Rule(LinkExtractor(allow=r"app/hq/stock/sh\d+/index.shtml"), callback="parse_data"),
             )
 ```

#### Selector对象的方法

 - .extrat()  		# 返回一个列表 包含Selector对象匹配到的所有元素的文本值，未找到则返回空列表
 - .extract_frist() 		# 返回一个字符串，为Selector对象匹配到的第一个元素的文本值，未找到则返回None
 - 

## 在scrapy中每次请求都得到随机headers

在middlewares中

```
from scrapy import signals
from fake_useragent import UserAgent

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

class RandomUserAgentMidddlware(object):
    def __init__(self, crawler):
        super(RandomUserAgentMidddlware, self).__init__()
        self.ua = UserAgent()
        self.ua_type = crawler.settings.get('RANDOM_UA_TYPE', 'random')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        def get_ua():
            return getattr(self.ua, self.ua_type)

        request.headers.setdefault('User-Agent', get_ua())

```
在settings文件中
RANDOM_UA_TYPE = "random"
DOWNLOADER_MIDDLEWARES = {
   'xxxxx.middlewares.RandomUserAgentMidddlware': 543,
'xxxxx.downloadermiddlewares.useragent.UserAgentMiddleware': None,
}

## 在scrapy中使用增量式爬虫

使用scrapy爬取大量数据时判断该次文件是否已经保存（增量式爬虫的关键）

新建py文件  ext_mod

```
#使用redis，hashlib，json
#将scrapy中得到的data保存到redis中
#去重  set
import redis
import hashlib
import json

redis_host = '127.0.0.1'

class Filter():
    '''将目标数据处理成哈希密文  用密文比较更快'''
    def get_md5(self,val):
        md5 = hashlib.md5()
        # updata()接受待加密对象
        md5.update(val.encode('utf-8'))
        return md5.hexdigest()  #取出密文值

    '''将密文值添加到队列'''
    def add_data(self,url):
        # python与redis建立连接
        red = redis.Redis(host=redis_host,port=6379,db=0)
        # 得到密文值后添加到redis服务中  key取为tc58:set_data
        result = red.sadd('tc58:set_data',self.get_md5(url))
        if result == 0:
            return False
        else:
            return True

    '''判断是否存在在集合中'''
    def ismember(self,url):
        # 建立连接
        red = redis.Redis(host=redis_host, port=6379, db=0)
        # 得到密文值后添加到redis服务中  key取为tc58:set_data
        # sismember()判断某内容存在
        res = red.sismember('tc58:set_data',self.get_md5(url))
        print("RES:",res)
        return res

    '''存储榨取的房屋信息(保存全量数据)'''
    def sava_house_info(self,item):
        red = redis.Redis(host=redis_host, port=6379, db=0)
        # 得到密文值后添加到redis服务中  key取为tc58:set_data
        result = red.sadd('tc58:set_data',json.dumps(item))
        return result
```
在管道文件里添加
```
from itemadapter import ItemAdapter
from lianjia.items import LianjiaItem
from lianjia.ext_mod import Filter
import logging
fu = Filter()		# 实例化

class LianjiaPipeline:
    def process_item(self, item, spider):
        data = dict(item)
        url = data['url'] # 取出详情页url
        print('链接:',url)
        # 如果url存在在服务中 就把重复的url保存到日志信息
        if fu.ismember(url):
            print('链接已保存.url:{}'.format(data['url']))
            logging.error(data['url'])
        # 不存在
        else:
            fu.add_data(url)
            fu.sava_house_info(data)

        return item
```
新建py文件  ext_items
```
import redis  # pip install redis
import json
# 建立链接  db = 11
r = redis.Redis(host='127.0.0.1',port="6379",)

class R_items():
    # 租房
    def save_zufang(self,val):
        r.sadd("demo58:zufang",json.dumps(val))


    # 二手房
    def save_ershou(self,val):
        r.sadd("demo58:ershou",json.dumps(val))
# 目的是可以将去重后的数据保存到redis中用以调用
# 管道文件中使用：
from demo_58.ext_items import R_items
r = R_items()
r.save_zufang(data)
```

## 线程池方法  多线程工作

```
from concurrent.futures import ThreadPoolExecutor
pool = ThreadPoolExecutor(5)
pool.submit(    )
#          方法名 不带括号,  形参1,2,...
```

## scrapy + selenium

spiders

```
导包item
from wangyinews.items import WangyinewsItem	
          第二层.item 				Item的类名
使用selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Optionsclass
xxxspider(scrapy.Spider):	
def __init__(self):        
     self.urls = []        
     chrome_options = Options()  # 启用一个配置文件
     chrome_options.add_argument("--headless")        
     chrome_options.add_argument("--disable-gpu")  
     # 将谷歌修改为无可视化界面        
     # 将selenium伪装为一个无头模式        
     chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])        
     # 驱动selenium        
>self.browse = webdriver.Chrome(options=chrome_options)
```
中间件
```
#middlewares.py
#4.2 开始篡改下载中间件的reposneclass WangyinewsDownloaderMiddleware:	
xxx	    
def process_response(self, request, response, spider):        
#4.3 该方法可以拦截引擎发送出去的响应对象（url + status + body）        
#下载器传递给Spider的响应对象        
#request：响应对象对应的请求对象        
#response： 当前方法拦截到的响应对象        
#spider： 像爬虫文件中对象的爬虫类提出要求        print('0000',request.url)        
#4.4 判断是否是四大新闻链接        
if request.url in spider.urls:            
#4.5 获取爬虫文件中的selenium对象            
browse = spider.browse            
#4.6 selenium像链接发请求            
browse.get(request.url)            
#下拉            browse.execute_script('window.scrollTo(0,document.body.scrollHeight)')            
time.sleep(1)            
#4.7 获取渲染后的源码            
page_text = browse.page_source            
#4.8 将selenium渲染等到的源码打包给引擎           
 '''            
 url: 响应体对应的            
 body:响应体（响应源码）            
 request:scrapy中的请求对象，数据都是跟着请求走的            
 '''            
new_reponse = HtmlResponse(url=request.url,body=page_text,encoding='utf-8',request=request)            
return new_reponse        
else:            return response      
#这里等同于返回未篡改前的response
```
item
```
#item.pyclass 
xxxItem(scrapy.Item):	
name = scrapy.Field()
#spider.pyitem = xxxItem()            
item['title'] = titles	
#在item里写入数据            
item['url'] = urls		
#[' ']里的必须在item.py里写入            
yield scrapy.Request(url=urls,callback=self.parse_content,meta={"ite":item})	
#请求url      #回调函数   		#meta携带的数据         #ite自己定
yield item            #spider.py 写到函数的最后
```

## 使用json格式保存数据

```
import json
from itemadapter import ItemAdapter

class WangyinewsPipeline:
    def __init__(self):
        self.file = open('新闻.json','a',encoding='utf-8')

    def process_item(self, item, spider):
        print('管道文件的item',item)
        print('item类型',type(item))
        data = dict(item)  # {}
        json_data = json.dumps(data,ensure_ascii=False)+',\n'  # JSON
        self.file.write(json_data)
        return item

    def __del__(self):
        self.file.close()
```


