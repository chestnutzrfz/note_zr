

# websocket

用于实现数据 '实时'更新的手段有轮询和 WebSocket这两种。
轮询指的是客户端按照一定时间间隔（如1 秒）访问服务端接口，从而达到 '实时' 的效果
websocket 真 实时

在WebSocket API中，浏览器和服务器只需要完成一次握手，
两者之间就直接可以创建持久性的连接，并进行双向数据传输。

WebSocket Secure (WSS)是基于SSL/TLS协议的WebSocket协议的加密版本
通过浏览器抓包ws

WebSocket 连接地址以ws 或wss 开头。连接成功的状态码不是200，而是101
Python库中用于连接 WebSocket 的有很多，易用、稳定的有  websocket-client(非异步)、websockets(异步)、aiowebsocket（异步）



```python
# websockets 异步的方法连接wss服务器
import asyncio
import websockets


async def connect_to_wss():
    async with websockets.connect('wss://example.com') as websocket:
        while True:
            # recv 方法接受服务器发送的数据
            data = await websocket.recv()
            # send 方法向服务器发送数据   发送订阅请求,以在无限循环中得到所需的数据
            await websocket.send('hi')
            print(data)

asyncio.run(connect_to_wss())
```



