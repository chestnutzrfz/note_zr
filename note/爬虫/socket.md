

# 网络基础

##### 网络

计算机网络就是把分布在不同的地理区域的计算机与专门的外部设备用通信线路互联在一起 ， 成为一个规模大 ， 功能强的网络系统。使得众多计算机可以方便的互通信息 ， 共享硬件、软件、数据资料等。

计算机网络可以提供一些主要的功能

- 资源共享

- 信息传输以及可以集中处理

- 综合信息服务

  ​

##### 计算机网络的种类

计算机网络有多类 ， 按照不同的分类原则 ， 可以分为不同的类型的计算机网络。

通常情况下计算机网络是按照规模大小以及延申范围进行分类，常见的类型有：

局域网(LAN)、城域网(MAN)、广域网(WAN);

internet 可以被视为世界上最大的广域网。



##### 网络安全

互联网具有双面性 ， 可以方便一些不法分子进行的一些侵害；方便了我们的日常使用。

我们只能防御 ， 如果你要反攻的话 ， 就需要精通计算机和互联网

建立安全的互联网连接



##### 互联网协议

协议的前提必须要有至少两方进行。

网络协议就是在网络中对信息管理 ， 传递的一些规范，在相互通信之间共同遵守的规则。

网络协议分为三个部分组成：

​	一个是语义部分：用于决定双方对话的类型

​	一个是语法部分：用于决定双方的对话格式

​	一个是变换规则：用于决定通信双方的应答关系



国际标准化组织（ISO）提出了 开放系统互连参考模型 ， 就是OSI 参考模型（理想模型）。OSI

力求将网络简化 ， 并以模块化的方式来设计网络

OSI参考模型把计算机网络分成7层 ， 是计算机网络结构的参考标准

OSI（从下到上分别为）：物理层、数据链路层、网络层、传输层、会话层、表示层、应用层

```
应用层: 为程序提供一个服务的接口
表示层：将上一层数据进行转换 ， 保证程序能够明白
会话层：负责建立、管理、终止会话
传输层：相当于网关，负责将上面的数据进行分段
网络层：负责对子网间的数据包进行路由选择
数据链路层：将数据进行打包 ， 或者进行解析数据后 ， 传递到网络层
物理层：将解释的数据传递给数据链路层 ， 将打包好的数据传递给硬件设备传输。
```

通信协议是网络通信的基础 ， IP协议是一个非常重要的通信协议，IP又称网际协议，是支持网间互联的数据报协议。IP协议提供了网间连接比较完善的功能 ， 包括IP数据报规定的互联网络范围内的地址格式。

TCP是传输控制协议，规定了一种可靠数据信息传递服务。与IP协议的功能不尽相同 ， 也可以分开单独使用，在功能上是互补的，在实际使用中将两个协议统称为TCP/IP协议。TCP/IP协议也是Internet中最常用的基础协议

（TCP/IP协议族）

TCP/IP协议将网络分为四层：网络接口层，网络层，传输层、应用层。

```
应用层：HTTP、DNS、FTP……
传输层：TCP、UDP
网络层：IP、ICMP、IDMP、ARP……
网络接口层：LAN、WAN、MAN
```

HTTP协议

超文本传输协议，常用与web浏览器和服务器之间的传递信息

HTTPS :超文本传输安全协议，通过使用SSL/TSL加密技术和HTTP协议结合进行网络数据安全传输

```
http和https的区别
1、http协议默认是TCP协议端口是80 ， https协议则是TCP协议443端口
2、http协议传输是明文传输 ， https协议传输之前需要SLL对数据进行加密
3、http协议页面响应要比https快 ， http协议需要3个TCP包 ， https传输数据需要12个TCP包
```



# sockert编程

### 网络请求方式

URL：对象代表资源的定位器；就是资源的地点（地址）

网络请求方式分为GET请求以及POST请求

GET：最常见的请求方式,传输的数据显示在URL中，对数据传输的大小有限制

POST：URL不显示传输数据 ， 以表单的形式进行传参，可以进行查询和修改信息

这两种请求方式都是使用TCP协议

状态码

```
100：继续。客户端可以继续传输请求
200: 请求成功
4** ：客户端的错误
404：服务器无法根据客户端的请求找到对应的资源
500：服务器内部错误 ， 无法完成请求
505：不支持HTTP版本
```

### 域名

在访问一台服务器的时候，需要记住服务器的IP地址 , 由于IP地址不便于记忆，就推出了域名技术，域名就是有一串字母著称的Internet上的某一台或者是计算机组的名称 ， 用于在数据传输的时候表示计算机的位置

域名可以用来表示一个单位 ， 机构以及个人在互联网上确定的名称或者位置，域名是唯一的

DNS

域名跟IP都是表示计算机的位置，但是IP唯一标识计算机的位置，DNS是将域名以及IP之间对应的关系进行存储 ， 当我们向DNS发起请求 ， DNS就会返回出域名所对应的IP地址

### IP地址

IP地址就是IP协议提供和的一种统一的地址格式，为互联网上每一个主机和每一个网络分配的逻辑地址

每个IP地址包括两个识别码（ID）就是网络id以及主机id

A类

```
0000000.000000.000000.000000
由一个字节的网络地址跟3个字节的主机地址组成 ， 网络地址的最高位必须是0
网络地址就是126 ， 主机的数量256**3-2
地址范围：1.0.0.0 - 126.255.255.254
```

B类

```
1000000.000000.000000.000000
由2个字节的网络地址跟2个字节的主机地址组成 ， 网络地址的最高位必须是10
网络地址就是16382 ， 主机的数量256**2-2
地址范围：128.0.0.0 - 191.255.255.254
```

C类

```
1100000.000000.000000.000000
由3个字节的网络地址跟1个字节的主机地址组成 ， 网络地址的最高位必须是110
网络地址就是， 主机的数量254
地址范围：192.0.0.0 - 223.255.255.254
```

D类：该地址用于多点广播地址（多播）

D类IP地址第一个字节以‘1110’开始 ，范围：224.0.0.0 - 239.255.255.254

E类 ， 用于测试开发用的 ，范围：240.0.0.0 - 255.255.255.254

 255.255.255.255属于广播地址

私有IP，在多网络IP中，有一部分IP地址是用于我们的局域网使用，也就属于私网IP ， 不在公网上使用

```
私网范围：
10.0.0.0~10.255.255.255
172.16.0.0~172.31.255.255
192.168.0.0~192.168.255.255
```

注意

IP地址是127.0.0.1~127.255.255.255用于回路测试

如果：127.0.0.1可以代表本机IP地址 ， 用http://127.0.0.1就可以测试中配置的web服务器的。

### 网络通信开发框架

我们涉及使用到的软件程序之间的网络通信应用大致分为两种：

1、web类：csdn ， 博客园 ， 力扣……可以直接使用浏览器打开的。

2、应用类：微信 ， QQ ， 抖音……需要进行安装

这两类的软件通信对应了不同的开发架构

1、C/S架构

C/S（Clinet和Server）就是客户端与服务端架构 ， 这种机构是从用户层面进行划分的 ， 该模式对用户的电脑操作系统的环境依赖比较大。

2、B/S架构

B/S（Brower和Server）就是浏览器和客户端架构 ，该模式只需要通过浏览器发送http协议请求服务商对应的资源 。 

### 端口

端口是传输数据的通道 ， 相当于门

端口号就是每一个端口的编号 ， 相当于门牌号

端口号的分类：知名端口 ， 动态端口

知名端口一般固定分配给一些服务 ， 范围0~1023.比如http协议服务端口号就是80.

动态端口操作系统在动态端口号范围内随机分配的，程序结束是 ， 端口号就会被释放 。范围1024~65535.

### socket编程

socket被翻译成‘套接字’ , 是实现网络编写进行数据传输的一种技术手段 ， 网络上各种各样的网络服务大多数都是基于socket来完成通信的。

```
我要给你发消息
1、有手机
2、有微信号
3、打开微信
4、等待关联（加好友）
5、接收 ， 发送消息
6、退出微信
7、手机息屏（关机）
```

### socket_TCP网络通信

TCP：传输控制协议。是一种面向连接的 ， 可靠的、基于字节流的传输层的通信协议

```
通信步骤：
建立连接
传输数据
关闭连接

特点：
1、面向连接 
2、可靠性（应答机制 ,超时冲传 , 错误校验 , 流量控制）

服务端的创建流程
1、创建服务端对象scoket
2、绑定IP ， 端口号
3、设置监听模式，设置最大的连接数
4、等待客户端连接
5、接收客户端数据
6、给客户端发送数据
7、关闭
socket  --> bind --> listen --> accpet  -- > recv(收)send(发) --> close
```

代码

```
# 服务端

import socket

# 1、创建服务端对象scoket(买手机)
'''
socket_family 网络地址类型 AF_INET 标识ipv4
socket_type 套接字类型 ， SOCK_STREAM 表示tcp套接字（流式套接字）
'''
phone = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# 2、绑定IP ， 端口号(注册微信号)
'''
bind的参数必须是一个元组
这个元组的参数（ip ， port） （'127.0.0.1' , 10086）
'''
phone.bind(('127.0.0.1' , 10086))

# 3、设置监听模式，设置最大的连接数
phone.listen(5)

# 4、等待客户端连接
'''
accept返回值一个是客户端连接的套接字对象 ， 一个是连接客户端的地址
'''
conn , clinent = phone.accept()

# 5、接收客户端数据
# 参数是每次最多接收最大字节 ， 格式bytes
data = conn.recv(1024)

print(data.decode('utf-8'))
# 6、给客户端发送数据
conn.send(data)

# 7、关闭
conn.close()
phone.close()
```

```
# 客户端
import socket

phone = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# 连接服务器
# ip与端口号必须与服务端的一致
phone.connect(('127.0.0.1' , 10086))

# 发送数据
phone.send('阿宸真帅'.encode('utf-8'))
# 接收消息
data = phone.recv(1024)
print(data.decode('utf-8'))

phone.close()
```

```
# 接收客户端的数据
while True:
    try:
        data = conn.recv(1024)
        print(data.decode('utf-8'))
        # 发送数据
        conn.send(data)
    except ConnectionResetError:
        break
        
        
# 发送数据
while True:
    msg = input('请输入消息>>>')
    if msg =='q':
        break
    # 判断msg是否有输入内容
    if not msg:
        continue
    phone.send(msg.encode('utf-8'))

    data = phone.recv(1024)
    print(data.decode('utf-8'))
```

### socket_UDP网络通信

udp是无连接的 ， 先启动哪一端都不会报错

UDP是属于数据报协议，发空的时候会自带报头 ， 在客户端可以输入为空 ， 服务端也可以接收到

```
import socket

phone = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)

phone.bind(('127.0.0.1' , 8864))

# 接收数据
while True:
    # 返回一个元组
    # 一个值是数据
    # 对方的IP地址以及端口号
    msg , clinet = phone.recvfrom(1024)
    print(msg.decode('utf-8'))
    phone.sendto(msg , clinet)

phone.close()
```

```
import  socket

phone = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
# 服务端的以及端口号
ip_port=('127.0.0.1' , 8864)

# 发送消息
while True:
    msg = input('>>>')
    if msg=='q':
        break
    phone.sendto(msg.encode('utf-8'), ip_port)
    get_msg , sever = phone.recvfrom(1024)
    print(get_msg.decode('utf-8'))

phone.close()
```



# 阻塞与非阻塞

socket都是会阻塞的

在等待连接以及等待接收数据的时候进入一个阻塞状态

```
import socket

phone = socket.socket(socket.AF_INET , socket.SOCK_STREAM)

# 绑定IP地址以及端口号
phone.bind(('127.0.0.1' , 10086))
# 设置非阻塞
phone.setblocking(False)

# 设置监听模式
phone.listen(5)

# 存放客户端的连接对象
r_list=[]
while True:
    try:
        # 等待客户端的连接
        conn , clinent = phone.accept()
        r_list.append(conn)
    except BlockingIOError:
        del_list=[]
        # 循环列表中是否有连接对象
        for i in r_list:
            # 等待客户端发送消息也会发送阻塞
            try:
                # 接收客户端的数据
                data = conn.recv(1024)
                print(data.decode('utf-8'))
                conn.send(data)
            except BlockingIOError:
                continue
            except Exception:
                conn.close()
                del_list.append(conn)
        # 删除断开连接的客户端对象
        for conn in del_list:
            r_list.remove(conn)
```

```
import socket

phone = socket.socket(socket.AF_INET , socket.SOCK_STREAM)

# 连接服务器
phone.connect(('127.0.0.1' , 10086))

# 发送数据
while True:
    msg = input('请输入消息>>>')
    if msg =='q':
        break
    # 判断msg是否有输入内容
    if not msg:
        continue
    phone.send(msg.encode('utf-8'))

    data = phone.recv(1024)
    print(data.decode('utf-8'))

phone.close()
```



# IO多路复用

IO是指input ， output

IO多路复用主要是用于提升效率 ， 一个服务端可以同时连接多个客户端

在socket实现需要使用到select模块

```
select.select([r],[w],[err])
r:当调用到accept的时候 ， 如果有新连接 ， 就会将连接添加到当中
```

```
import socket
import select

sock = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
# 这个默认是为True即为阻塞状态
sock.setblocking(False)
sock.bind(('127.0.0.1' , 8081))
sock.listen(5)

read_list = [sock]
'''
如果i等于自己创建的对象 ， 那就判断是否有新的连接进来
有 ， 将连接添加到列表中[sock , 第一个客户链接 ,]

如果i是连接对象 ， 那么就获取对象发送的消息并给链接客户发送消息
'''
while True:
    r , w , e = select.select(read_list ,[],[])
    for i in r:
        if i is sock:
            # 在此获取新的客户连接
            conn,addr=i.accept()
            read_list.append(conn)
        else:
            try:
                data = i.recv(1024)
                print(data.decode('utf-8'))
            except Exception:
                i.close()
                read_list.remove(i)
                continue
            i.send(data.upper())
```

```
import socket

sock = socket.socket(socket.AF_INET , socket.SOCK_STREAM)

sock.connect(('127.0.0.1' , 8081))
while True:
    msg = input('>>>')
    if not msg:
        continue
    if msg=='q':
        break
    sock.send(msg.encode('utf-8'))
    data = sock.recv(1024)
    print(data.decode('utf-8'))
```

# 粘包

原因：TCP，数据流会杂糅在一起

通过send的数据长度来判断接收的次数

使用struct获取数据报头

```

```

