### 使用scrapy数据抓取django将数据整理essearch实现站内搜索

##### 根目录中创建两个文件夹

1－essearch_58_spider 	  	scrapy文件夹
2－essearch_58  		django文件夹

### 1.1－在scrapy根目录中创建estool.py文件

创建能够让scrapy与es连接让爬取的数据可以直接存储在es中

```
'''与es连接 存储数据'''
from elasticsearch import Elasticsearch
#忽略警告
import warnings
warnings.filterwarnings("ignore")

class Estools():
    def __init__(self):
        # 连接
        self.es = Elasticsearch('http://127.0.0.1:9200')
        
    # 创建一个索引
    def create_index(self,body):
        r = self.es.indices.create(index='tcdata',body = body)
        return r

    # 插入数据
    def insert_data(self,body):
        result = self.es.index(index='tcdata',body=body)
        return result

if __name__ == '__main__':
    body = {
        "mappings":{
            "properties":{
                "fang_title":{
                    "type":"text",
                    "analyzer":"ik_max_word"

                },
                "fang_price": {
                    "type": "text",

                },
                "fang_href": {
                    "type": "text",

                },
                "fang_address": {
                    "type": "text",
                    "analyzer": "ik_max_word"

                },
            }
        }
    }
    es = Estools()
    es.create_index(body)
```

### 1.2 - 创建scrapy文件项目

##### 1.2.1 - 在scrapy中使用redis将爬取得到的数据去重

ext_mod.py

```
# -*- coding: utf-8 -*-
import redis  # pip install redis
import hashlib

REDIS_HOST = '127.0.0.1'

class Filter(object):
    '''将目标数据进行打包成哈希 用哈希去重比对更快'''

    def get_md5(self, val):
        md5 = hashlib.md5()
        md5.update(val.encode('utf-8'))
        return md5.hexdigest()

    '''将目标数据加入到Redis过滤器（指纹队列）'''

    def add_url(self, url):
        # python连接redis数据库
        red = redis.Redis(host=REDIS_HOST, port=6379, db=1)
        # 将元素加入到集合中，已经存在于集合中的元素将被忽略
        res = red.sadd('demo58:url_set', self.get_md5(url))
        if res == 0:
            return False
        else:
            return True

    '''检查目标数据是否存在在集合队列中'''
    def ismember(self, url):
        red = redis.Redis(host=REDIS_HOST, port=6379, db=1)
        # 判断某元素是否在集合
        result = red.sismember('demo58:url_set', self.get_md5(url))
        return result
```

##### 1.2.2 - 修改items.py文件

```
import scrapy

class Essearch58SpiderItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    url = scrapy.Field()
    address = scrapy.Field()
# 四种所要爬取的数据
```

##### 1.2.3 - 修改middlewares.py 文件

```
import random
from scrapy import signals

from itemadapter import is_item, ItemAdapter
from fake_useragent import UserAgent

class RandomProxyMiddleware(object):

    def process_request(self, request, spider):
        proxy_list = []
        proxy = random.choice(proxy_list)
        request.meta['proxy'] = proxy
# 使用代理ip

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
# 让每次发送的请求所带的useragent都不相同
```

##### 1.2.4 - 修改settings.py文件

```
BOT_NAME = "essearch_58_spider"

SPIDER_MODULES = ["essearch_58_spider.spiders"]
NEWSPIDER_MODULE = "essearch_58_spider.spiders"

ROBOTSTXT_OBEY = True

DEFAULT_REQUEST_HEADERS = {
   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
   "Accept-Language": "en",
    'referer': 'https://58.com/chuzu'
}

DOWNLOADER_MIDDLEWARES = {
   # "essearch_58_spider.middlewares.Essearch58SpiderDownloaderMiddleware": 543,
    'essearch_58_spider.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'essearch_58_spider.middlewares.RandomUserAgentMidddlware': 543,
}

PROXY_POOL_ENABLED = True
PROXY_POOL_URL = 'http://your-proxy-pool-url'

RANDOM_UA_TYPE = "random"

ITEM_PIPELINES = {
   "essearch_58_spider.pipelines.Essearch58SpiderPipeline": 300,
    # 'essearch_58_spider.pipelines.Esfangdata': 299,
}

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
```

##### 1.2.5 - 修改pipelines.py文件

```
# 让数据下载直接通过es下载
from essearch_58_spider.items import Essearch58SpiderItem
from estools.estool import Estools
import json

class Essearch58SpiderPipeline:

    def __init__(self):
        self.file = open('zufang58.json','a',encoding='utf-8')

    def process_item(self, item, spider):
        data = dict(item)  # {}
        json_data = json.dumps(data,ensure_ascii=False)+',\n'  # JSON
        self.file.write(json_data)
        return item

    def __del__(self):
        self.file.close()

class Esfangdata:
    def __init__(self):
        self.es = Estools()

    def process_item(self, item, spider):
        if isinstance(item, Essearch58SpiderItem):
            data = dict(item)
            self.es.insert_data(data)
        return item
```

### 1.3 - 完成spider.py爬虫主体部分

```
import re
import scrapy
from essearch_58_spider.items import Essearch58SpiderItem

class SpiderSpider(scrapy.Spider):
    name = "spider"
    allowed_domains = ["58.com"]
    start_urls = ["https://hrb.58.com/zufang/"]
    '''解析租房信息'''
    def parse(self, response):
        # 标题
        titles = response.xpath('//div[@class="des"]/h2/a/text()').extract()
        # 价格
        price_list = response.xpath('//div[@class="money"]')
        # 详情页链接
        hrefs = response.xpath('//div[@class="des"]/h2/a/@href').extract()
        # 地址信息
        address_list = response.xpath('//p[@class="infor"]')
        for title, price, href, address in zip(titles, price_list, hrefs, address_list):
            a = address.xpath('string(.)').extract_first()
            # 地址会出现一些特殊符号 所以对其进行替换处理
            zufang_addre = re.sub(r'\xa0|\n', '-', a, re.S).replace('  ', '').strip()
            # print(zufang_addre)
            zf_item = Essearch58SpiderItem()
            zf_item['title'] = title.strip()
            zf_item['price'] = price.xpath('string(.)').extract_first().strip()
            zf_item['url'] = href
            zf_item['address'] = zufang_addre
            print("租房数据：", zf_item)
            yield zf_item
        # 构造翻页
        # https://cs.58.com/chuzu/pn3/   一共70页 pn1..pn70
        for i in range(2, 71):
            zufang_next_url = 'https://hrb.58.com/chuzu/pn{}/'.format(i)
            # print('当前正在租房的翻页：{}'.format(zufang_next_url))
            yield scrapy.Request(url=zufang_next_url, callback=self.parse)

if __name__ == '__main__':
    from scrapy import cmdline
    cmdline.execute(['scrapy', 'crawl', 'spider'])
```

### 2.1 － 通过django框架将数据整理便于es搜索
