## MitmProxy中间人代理攻击



### 介绍

```stylus
mitm的全称是Man-in-the-middle attack(中间人攻击)，它是一种"间接"的入侵攻击，这种攻击模式是通过各种技术手段将受入侵者控制的计算机虚拟放置在网络连接中的两台通信计算机之间，这台计算机就成为中间人，有一点类似我们之前使用的fiddler以及IP代理
```

<img src="../img/mitmproxy原理.png"></img>

```stylus
mitmproxy是一个免费和开源的交互式HTTPS代理，基于中间人的方式用于调试，测试，抓包和渗透测试，它可以用于拦截，检查，修改和重构web通信，例如：HTTP/1,HTTP/2,Websocket或任何其他受SSL/TLS保护的协议

可以解码从HTML到Protobuf的各种消息类型，即时拦截特定的消息，在它们到达目的地之前，对其进行修改，稍后将其重构到客户端或服务器
```

### 优势

```stylus
mitmproxy-mitmdump可编写强大的插件和脚本，脚本APi提供对MitmProxy的完全控制，并可以自动修改消息，重定向流量，可视化消息或实现自定义命令，最重要的原因式可配合Python脚本对数据包进行拦截修改，使用简单，所以MitmProxy是爬虫工程师必须掌握的利器之一
```

### 官网的Python代码示例

```python
"""
mitmProxy 介绍：https://blog.csdn.net/h416756139/article/details/51940757
github地址：https://github.com/mitmproxy/mitmprox
mitmproxy 官网：https://mitmproxy.org
mitmproxy 官网文档：https://docs.mitmproxy.org/stable
"""
def request(flow: http.HTTPFlow):
    # 重定向到不同的主机
    if flow.request.pretty_host == "example.com":
        flow.request.host = "mitmproxy.org"
    # 来自代理的回答
    elif flow.request.path.endswith("/brew"):
        flow.response = http.Response.make(
            418, b"I'm a teapot",
        )
```

### 安装配置

```stylus
客户端安装：https://mitmproxy.org/downloads/
python库安装：pip install mitmproxy

(1) 在安装完成之后，在cmd命令行中输入Mitmdump启动服务，默认端口是8080

(2) 启动成功后，下载Mitm证书：访问：http://mitm.it/ 下载

(3) 点击windows下载安装，如果网页显示If you can see this, traffic is not passing through Mitmproxy,则按照第二步设置Windows本地代理后，再次安装

(4) 修改Windows本地代理，选择"设置"中的"网络代理"中的"手动设置代理"，打开"使用代理"，并将IP地址修改为127.0.0.1，端口修改为默认8080端口或修改后的端口

安装结束可以通过命令查看是否安装成功
mitmdump --version
输出
Mitmproxy: 4.0.1
Python:    3.6.5
OpenSSL:   OpenSSL 1.1.0h  27 Mar 2018
Platform:  Windows-10-10.0.16299-SP0
```

### 常规命令

```stylus
要启动 mitmproxy 用 mitmproxy、mitmdump、mitmweb 这三个命令中的任意一个即可，这三个命令功能一致，且都可以加载自定义脚本，唯一的区别是交互界面的不同。

linux操作系统下(windos不支持mitmproxy)
mitmproxy 命令启动后，会提供一个命令行界面，用户可以实时看到发生的请求，并通过命令过滤请求，查看请求数据。形如：
```

<img src="../img/mitmproxy命令界面.png"></img>

```stylus
mitmweb 命令启动后，会提供一个 web 界面，用户可以实时看到发生的请求，并通过 GUI 交互来过滤请求，查看请求数据。形如：
```

<img src="../img/mitmweb可视化界面.png"></img>

```stylus
mitmdump 命令启动后——你应该猜到了，没有界面，程序默默运行，所以 mitmdump 无法提供过滤请求、查看数据的功能，只能结合自定义脚本，默默工作。

由于 mitmproxy 命令的交互操作稍显繁杂且不支持 windows 系统，而我们主要的使用方式又是载入自定义脚本，并不需要交互，所以原则上说只需要 mitmdump 即可，但考虑到有交互界面可以更方便排查错误，所以这里以 mitmweb 命令为例。实际使用中可以根据情况选择任何一个命令。
```

### 脚本锻炼

```stylus
完成了上述工作，我们已经具备了操作 mitmproxy 的基本能力 了。接下来开始开发自定义脚本，这才是 mitmproxy 真正强大的地方。

脚本的编写需要遵循 mitmproxy 规定的套路，这样的套路有两个。

第一个是，编写一个 py 文件供 mitmproxy 加载，文件中定义了若干函数，这些函数实现了某些 mitmproxy 提供的事件，mitmproxy 会在某个事件发生时调用对应的函数，形如：
```

```python
import mitmproxy.http
from mitmproxy import ctx
 
num = 0
 
 
def request(flow: mitmproxy.http.HTTPFlow):
    global num
    num = num + 1
    ctx.log.info("We've seen %d flows" % num)
```

```stylus
第二个是，编写一个 py 文件供 mitmproxy 加载，文件定义了变量 addons，addons 是个数组，每个元素是一个类实例，这些类有若干方法，这些方法实现了某些 mitmproxy 提供的事件，mitmproxy 会在某个事件发生时调用对应的方法。这些类，称为一个个 addon，比如一个叫 Counter 的 addon：
```

```python
import mitmproxy.http
from mitmproxy import ctx
 
 
class Counter:
    def __init__(self):
        self.num = 0
 
    def request(self, flow: mitmproxy.http.HTTPFlow):
        self.num = self.num + 1
        ctx.log.info("We've seen %d flows" % self.num)
 
 
addons = [
    Counter()
]

"""
控制台处于当前文件目录，执行：
mitmweb -s py文件名
或者
mitmdump -s py文件名
"""
```

这里强烈建议使用第二种套路，直觉上就会感觉第二种套路更为先进，使用会更方便也更容易管理和拓展。况且这也是[官方内置的一些 addon](https://github.com/mitmproxy/mitmproxy/tree/master/mitmproxy/addons) 的实现方式。

```stylus
我们将上面第二种套路的示例代码存为 addons.py，再重新启动 mitmproxy：
mitmweb -s addons.py

当浏览器使用代理进行访问时，就应该能看到控制台里有类似这样的日志：
Web server listening at http://127.0.0.1:8081/
Loading script addons.py
Proxy server listening at http://*:8080
We've seen 1 flows
……
……
We've seen 2 flows
……
We've seen 3 flows
……
We've seen 4 flows
……
……
We've seen 5 flows
……

这就说明自定义脚本生效了
```



## HTTP的生命周期事件

###针对 HTTP 生命周期

```stylus
def http_connect(self, flow: mitmproxy.http.HTTPFlow):

(Called when) 收到了来自客户端的 HTTP CONNECT 请求。在 flow 上设置非 2xx 响应将返回该响应并断开连接。CONNECT 不是常用的 HTTP 请求方法，目的是与服务器建立代理连接，仅是 client 与 proxy 的之间的交流，所以 CONNECT 请求不会触发 request、response 等其他常规的 HTTP 事件

def requestheaders(self, flow: mitmproxy.http.HTTPFlow):
(Called when) 来自客户端的 HTTP 请求的头部被成功读取。此时 flow 中的 request 的 body 是空的

def request(self, flow: mitmproxy.http.HTTPFlow):
(Called when) 来自客户端的 HTTP 请求被成功完整读取

def responseheaders(self, flow: mitmproxy.http.HTTPFlow):
(Called when) 来自服务端的 HTTP 响应的头部被成功读取。此时 flow 中的 response 的 body 是空的

def response(self, flow: mitmproxy.http.HTTPFlow):
(Called when) 来自服务端端的 HTTP 响应被成功完整读取

def error(self, flow: mitmproxy.http.HTTPFlow):
(Called when) 发生了一个 HTTP 错误。比如无效的服务端响应、连接断开等。注意与“有效的 HTTP 错误返回”不是一回事，后者是一个正确的服务端响应，只是 HTTP code 表示错误而已
```

###针对 TCP 生命周期

```stylus
def tcp_start(self, flow: mitmproxy.tcp.TCPFlow):
(Called when) 建立了一个 TCP 连接

def tcp_message(self, flow: mitmproxy.tcp.TCPFlow):
(Called when) TCP 连接收到了一条消息，最近一条消息存于 flow.messages[-1]。消息是可修改的

def tcp_error(self, flow: mitmproxy.tcp.TCPFlow):
(Called when) 发生了 TCP 错误

def tcp_end(self, flow: mitmproxy.tcp.TCPFlow):
(Called when) TCP 连接关闭
```

###针对 Websocket 生命周期

```stylus
def websocket_handshake(self, flow: mitmproxy.http.HTTPFlow):
(Called when) 客户端试图建立一个 websocket 连接。可以通过控制 HTTP 头部中针对 websocket 的条目来改变握手行为。flow 的 request 属性保证是非空的的

def websocket_start(self, flow: mitmproxy.websocket.WebSocketFlow):
(Called when) 建立了一个 websocket 连接

def websocket_message(self, flow: mitmproxy.websocket.WebSocketFlow):
(Called when) 收到一条来自客户端或服务端的 websocket 消息。最近一条消息存于 flow.messages[-1]。消息是可修改的。目前有两种消息类型，对应 BINARY 类型的 frame 或 TEXT 类型的 frame

def websocket_error(self, flow: mitmproxy.websocket.WebSocketFlow):
(Called when) 发生了 websocket 错误

def websocket_end(self, flow: mitmproxy.websocket.WebSocketFlow):
(Called when) websocket 连接关闭
```

###针对网络连接生命周期

```stylus
def clientconnect(self, layer: mitmproxy.proxy.protocol.Layer):
(Called when) 客户端连接到了 mitmproxy。注意一条连接可能对应多个 HTTP 请求

def clientdisconnect(self, layer: mitmproxy.proxy.protocol.Layer):
(Called when) 客户端断开了和 mitmproxy 的连接

def serverconnect(self, conn: mitmproxy.connections.ServerConnection):
(Called when) mitmproxy 连接到了服务端。注意一条连接可能对应多个 HTTP 请求

def serverdisconnect(self, conn: mitmproxy.connections.ServerConnection):
(Called when) mitmproxy 断开了和服务端的连接

def next_layer(self, layer: mitmproxy.proxy.protocol.Layer):
(Called when) 网络 layer 发生切换。你可以通过返回一个新的 layer 对象来改变将被使用的 layer。详见 layer 的定义
https://github.com/mitmproxy/mitmproxy/blob/fc80aa562e5fdd239c82aab1ac73502adb4f67dd/mitmproxy/proxy/protocol/__init__.py#L2
```

###通用生命周期

```stylus
def configure(self, updated: typing.Set[str]):
(Called when) 配置发生变化。updated 参数是一个类似集合的对象，包含了所有变化了的选项。在 mitmproxy 启动时，该事件也会触发，且 updated 包含所有选项

def done(self):
(Called when) addon 关闭或被移除，又或者 mitmproxy 本身关闭。由于会先等事件循环终止后再触发该事件，所以这是一个 addon 可以看见的最后一个事件。由于此时 log 也已经关闭，所以此时调用 log 函数没有任何输出

def load(self, entry: mitmproxy.addonmanager.Loader):
(Called when) addon 第一次加载时。entry 参数是一个 Loader 对象，包含有添加选项、命令的方法。这里是 addon 配置它自己的地方

def log(self, entry: mitmproxy.log.LogEntry):
(Called when) 通过 mitmproxy.ctx.log 产生了一条新日志。小心不要在这个事件内打日志，否则会造成死循环

def running(self):
(Called when) mitmproxy 完全启动并开始运行。此时，mitmproxy 已经绑定了端口，所有的 addon 都被加载了

def update(self, flows: typing.Sequence[mitmproxy.flow.Flow]):
(Called when) 一个或多个 flow 对象被修改了，通常是来自一个不同的 addon
```

### 示例

```stylus
估计看了那么多的事件你已经晕了，正常，鬼才会记得那么多事件。事实上考虑到 mitmproxy 的实际使用场景，大多数情况下我们只会用到针对 HTTP 生命周期的几个事件。再精简一点，甚至只需要用到 http_connect、request、response 三个事件就能完成大多数需求了
```





##拓展实战参考作业

### 替换浏览器的JS

```stylus
通过中间人替换js文件内容通常用来规避检测，比如下面的代码，如果拦截到了来自https://baidu.com的响应内容，则把响应内容中的所有debugger替换为空
```

```python
from mitmproxy import flow

def response(flow:flow):
    target_url = 'https://www.baidu.com'
    if target_url in flow.request.url:
        jscode = flow.response.get_text()
        jscode = jscode.reqplace("debugger", "")
        flow.response.set_text(jscode)
```

### 微信公众号为例

```stylus
因为获取微信公众号有很多参数，比如x-wechat-key, __biz, Appmsg_token, pass_ticket等，如果去逆向，难度过高并且消耗大量时间，此时可以通过自动触发请求，然后用mitmproxy拦截请求，获取其中的加密参数来进行数据的采集

本案例采用Python自动化操作windos客户端的微信，用Redis存储Mitm拦截到的key，然后通过调度分配采集任务，完成请求后将数据保存入库
```

```python
# Python-Mitm拦截代码如下：
from mitmproxy import http


class WeiXinProxy(object):

    def request(self, flow:http.HTTPFlow):
        if flow.request.host == 'mp.weixin.com':
            url_path = flow.request.path
            if url_path.startswith("/s?__biz"):
                if "uin=" in url_path and "key=" in url_path and "pass_ticket=" in url_path:
                    link = url_path.partition('?')[2].split('&')
                    biz = link[0].partition('=')[2]
                    mid = link[1].partition('=')[2]
                    idx = link[2].partition('=')[2]
                    sn = link[3].partition('=')[2]
                    print("抓到了：", biz, mid, idx, sn)
# 通过host判断是否来自微信的请求，然后通过url来判断是否包含加密参数的连接
```

### 移动端拦截案例

```stylus
移动端不论是APP还是小程序，都可以采用上一小节的方法，通过自动化工具或者脚本触发请求，然后用Mitmproxy拦截请求，或者响应，另外Mitmproxy有一个优势就是可以部署在Linux服务器上

本案例以appium + Android设备 + Mitmproxy采集微信指数为例，微信指数并没有复杂的加密算法，但是有一个具有时效性的search_key参数，所以需要做的就是通过Mitm将search_key取出保存到数据库中，供外部程序使用，如果过期则重新获取

配置好相关环境和证书后，编写拦截代码
```

```python
import json

def response(flow):
    url = "https://search.weixin.qq.com/cgi-bin/searchweb/weApplogin"
    if flow.request.url.startswith(url):
        text = flow.response.text
        data = json.loads(text)
        search_key = data.get('data').get('search_key')
        print(search_key)

# 也就是说，只要是mitmproxy抓到包的请求，都可以通过这种方式进行拦截并做相应的数据采集
```

