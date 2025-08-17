# RPC

##### RPC原理

​    结合socket通讯
​    在js加密代码中执行js注入
​    把socket当成服务器
​    把信息传输给pycharm

##### 浏览器

​    访问抖音 弹幕有加密
​    通过js逆向 找到对应的解密方法
​    解密后的译文会由变量接收

    开始建立socket通信
    把浏览器当成服务器
    将解密后的译文通过socket通信传递给pycharm(客户端)

##### pycharm

​    socket当客户端

​    从服务器中获取数据
​    进行socket连接
​    不断的进行数据的获取

##### 序列化和反序列化

​    网络中数据的传递是以二进制传递的  字节
​    如何将二进制数据变成html  -> 反序列化
​    将数据变成二进制传递 -> 序列化
​    编码和解码

### WebSocket

```python
WebSocket()
WebSocket.send 向服务器发送请求
WebSocket.onmessage 指定收到服务器数据后的回调函数

需要js功底比较多
RPC最重要的是找到入口 一般WebSocket消息处理函数为onmessage或者addEventListener("message")


在部分有js加密的场景中
我们可以通过socket通信 以python为服务端 浏览器为客户端 将用户的输入传递仅js代码中,
然后在js代码中构架请求对象,发送请求,将响应内容通过socket通信返回给python客户端执行响应的解析
从而在有翻页等循环请求的场景中  解决js加密
```

### 浏览器爬取抖音弹幕

```python
浏览器抓包抖音直播
弹幕数据一般是WS(websocket) -> 消息 -> 接受 -> utf-8
对该包进行 js逆向
搜索new websocket
在搜索结果中继续搜索new websocket
找到其中一个包中有onmessage 方法
onmessage处理函数接收
e 为 websocket的响应

找到_receiveMessage(e, t)方法 返回数据
找到emit(e, ...t) 方法 解析数据

注入流程:
network中左上角点击替换 -> 创建文件夹 -> 浏览器上方授权 
    -> 在需要的js文件(new websocket所在文件)中点击替换内容   就可以发现在文件夹中有了该js文件的目录和文件
    -> 点击该js文件(与浏览器中原方法所在js文件同名) -> 浏览器替换中点开 
    -> 搜索emit找到创建的方法 11605行(2024年4月23日)  (直接搜22892 函数前数字)
    -> 1/44/20
    
    在pycharm中写RPC 代码(复用) 后启动py文件, 在浏览器中关闭检查 刷新

```

##### js代码注入

```javascript
# 本地打开js代码注入:

window.dataLx = i.toObject();
// !function为创建自执行方法
//!function(){
    // 创建局部变量，接收window.dataLx全局变量
    var res = window.dataLx;
    if (window.flagLX){
        window.wsLX.send(JSON.stringify(res));
    }
    else{
        var ws = new WebSocket("ws://127.0.0.1:9999");
        window.wsLX = ws;
        window.flagLX = true;
        ws.open = function(evt){};
        ws.onmessage = function(evt){
            ws.send(JSON.stringify(res));
        }
    }
//};
```

##### 代码

代码均可复用   只需添加得到数据后的方法

```python
import asyncio, websockets
# RPC 逆向js代码
# 代码都是相同的 可以复用

async def check_permit(websocket):
    send_text = 'lx'
    await websocket.send(send_text)
    return True


async def recv_msg(websocket):
    while True:
        recv_text = await websocket.recv()
        # 获取弹幕数据字典
        print(recv_text)


async def main_logic(websocket, path):
    await check_permit(websocket)
    await recv_msg(websocket)

start_server = websockets.serve(main_logic, '127.0.0.1', 9999)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
```

##### 实现流程

```python
实现流程整理：
    1.js文件定位：通过搜索new websocket定位js文件
    2.搜索结果有三个，通过观察js文件中结果位置：
        观察特性：websocket提供的原生方法
        WebSocket.send  用于向服务器发送请求
        WebSocket.onopen 用于指定连接成功后的回调函数
        WebSocket.onmessage 用于指定收到服务器数据后的回调函数
        WebSocket.onclose 用于指定连接关闭后的回调函数
        WebSocket.binaryType = "arraybuffer"; 用来表示通用的，固定长度的二进制数据缓冲区
        RPC最重要的是找到入口点，一般WebSocket消息处理函数为onmessage或者addEventListener("message")
        onMessage(e) {
                this.socket.addEventListener("message", e)
            }
        对onMessage(e)执行断点调试：该函数方法是用来处理消息的。用来处理弹幕的
    3.进入该断点：来到this.emit(r))：该函数方法是对响应的弹幕内容执行解析(序列化与反序列化)
    4.最终：通过调试，看到代码：
        runAllEvents(e, t) {
                var a;
                for (const [r,n] of this.eventsMap.entries()) {
                    const a = this.messageModules[r];
                    if (n && a && this.isCorrectEventName(r, e)) {
                        const o = t.getPayload_asU8()
                          , i = a.deserializeBinary(o);
                        return this.info(`emit Message Type: ${e} ${r}`),
                        this.info("emit Message Payload:", (()=>i.toObject())),
                        void n.forEach((e=>{
                            e(i, t, o)
                        }
                        ))
                    }
                }
    5.55行js代码位置，是弹幕的数据变量i：i值是用来接收弹幕数据的变量
    6.通过构建web socket通信将变量i值的内容，通过websocket传输给pycharm
    7.js的web socket通信代码
        window.dataLx = i.toObject();
        // !function为创建自执行方法
        //!function(){
            // 创建局部变量，接收window.dataLx全局变量
            var res = window.dataLx;
            if (window.flagLX){
                window.wsLX.send(JSON.stringify(res));
            }
            else{
                var ws = new WebSocket("ws://127.0.0.1:9999");
                window.wsLX = ws;
                window.flagLX = true;
                ws.open = function(evt){};
                ws.onmessage = function(evt){
                    ws.send(JSON.stringify(res));
                }
            }
        //};
    8.在pycharm中，构建客户端代码(见最下面)
    9.浏览器执行js注入，访问抖音平台执行本地加载js代码
    10.js注入流程
        1.在source区域，左上角，找到Overrides，点击+号(指定本地加载js的文件夹)
        2.对需要执行js注入的js文件：右击，save as Overrides(没有该选项，多调试几次)
        3.从本地打开该js，执行注入
            注入效果局部展示：
            for (const [r,n] of this.eventsMap.entries()) {
                    const a = this.messageModules[r];
                    if (n && a && this.isCorrectEventName(r, e)) {
                        const o = t.getPayload_asU8()
                          , i = a.deserializeBinary(o);
                         window.dataLx = i.toObject();
                        // !function为创建自执行方法
                        //!function(){
                            // 创建局部变量，接收window.dataLx全局变量
                            var res = window.dataLx;
                            if (window.flagLX){
                                window.wsLX.send(JSON.stringify(res));
                            }
                            else{
                                var ws = new WebSocket("ws://127.0.0.1:9999");
                                window.wsLX = ws;
                                window.flagLX = true;
                                ws.open = function(evt){};
                                ws.onmessage = function(evt){
                                    ws.send(JSON.stringify(res));
                                }
                            }
                        //};
                        return this.info(`emit Message Type: ${e} ${r}`),
                        this.info("emit Message Payload:", (()=>i.toObject())),
                        void n.forEach((e=>{
                            e(i, t, o)
                        }
                        ))
                    }
                }
        4. 对Enable Local Overrides打钩：访问该平台，执行本地js文件加载(是根据相同的文件名执行替换加载的)
        5.刷新浏览器，运行客户端代码，即可采集抖音平台任意直播间弹幕数据
            直播间的任意切换，不影响代码的运行
        6.直播间弹幕内容的获取：
            代码的获取效果：
                能够采集直播间的人气走动
                能够采集观看用户的送礼物信息
                能够采集用户的弹幕
```

