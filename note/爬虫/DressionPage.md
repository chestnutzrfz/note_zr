# DressionPage

DrissionPage 是一个基于 python 的网页自动化工具
它既能控制浏览器，也能收发数据包，还能把两者合而为一
无 webdriver 特征
无需为不同版本的浏览器下载不同的驱动
运行速度更快
可以跨 iframe 查找元素，无需切入切出

iframe 看作普通元素，获取后可直接在其中查找元素，逻辑更清晰
可以同时操作浏览器中的多个标签页，即使标签页为非激活状态，无需切换
可以直接读取浏览器缓存来保存图片，无需用 GUI 点击另存
可以对整个网页截图，包括视口外的部分（90以上版本浏览器支持）
可处理非open状态的 shadow-root

```python
co = ChromiumOptions()
# 阻止“自动保存密码”的提示气泡
co.set_pref('credentials_enable_service', False)
# 阻止“要恢复页面吗？Chrome未正确关闭”的提示气泡
co.set_argument('--hide-crash-restore-bubble')
page = ChromiumPage(co)
```

### 简单使用dp

```python
# 启动chrome 浏览器  访问网址   ChromiiumPage单纯用于操作浏览器的页面对象
from DrissionPage import ChromiumPage
# 创建chrome对象
page = ChromiumPage()
# 访问网址
page.get('https://gitee.com/login')
# 定位到账号文本框，获取文本框元素
# ele查找元素  # 按id查找   ele内置等待 若元素未加载等待  超时10s
ele = page.ele('#user_login')
# 输入对文本框输入账号  input 对元素输入文本
ele.input('zhanghao')
# 定位到密码文本框并输入密码
page.ele('#user_password').input('mima')
# 点击登录按钮   @ 按属性值查找     click 点击
page.ele('@value=登 录').click()
```



```python
# 导入
from DrissionPage import ChromiumPage
# 创建对象
page = ChromiumPage()
# 等待页面跳转
page.wait.load_start()
# 设置窗口最大化       mini 最小化
page.set.window.max()
# 隐藏浏览器窗口
page.set.window.hide()
# 关闭浏览器
page.quit()
# 关闭当前标签页
page.close()
# 如果要点击的元素就是没有位置的，可以强制使用 js 点击，用法是
.click('js')
# 页面滚动的功能藏在scroll属性中   bottom 底部    top顶部  ......
page.scroll.to_bottom()
# 此方法用于保存src()方法获取到的资源到文件
img = page('tag:img')
img.save('D:\\img.png')
```



### 启动的配置

```python
from DrissionPage import ChromiumOptions, ChromiumPage

co = ChromiumOptions()
co.incognito()  # 匿名模式
co.headless()  # 无头模式
co.set_argument('--no-sandbox')  # 无沙盒模式
page = ChromiumPage(co)
```

```python
from DrissionPage import WebPage, ChromiumOptions

# 创建配置对象（默认从 ini 文件中读取配置）
co = ChromiumOptions()
# 设置不加载图片、静音
co.no_imgs(True).mute(True)

# 以该配置创建页面对象
page = WebPage(chromium_options=co)
```

### 模拟鼠标

```python
# 对ele元素进行模拟点击，如判断被遮挡也会点击
ele.click()

# 用js方式点击ele元素，无视遮罩层
ele.click(by_js=True)
ele.click(js)

# 如元素不被遮挡，用模拟点击，否则用js点击
ele.click(by_js=None)


# 此方法用于带偏移量点击元素
# 点击元素右上方 50*50 的位置
ele.click.at(50, -50)

# 点击元素上中部，x相对左上角向右偏移50，y保持在元素中点
ele.click.at(offset_x=50)

# 和click()一致，但没有重试功能
ele.click.at()


# 拖动当前元素到距离50*50的位置，用时1秒
ele.drag(50, 50, 1)


# 把 ele1 拖拽到 ele2 上
ele1 = page.ele('#div1')
ele2 = page.ele('#div2')
ele1.drag_to(ele2)

# 把 ele1 拖拽到网页 50, 50 的位置
ele1.drag_to((50, 50))


# 对整页截图并保存
page.get_screenshot(path='tmp', name='pic.jpg', full_page=True)

# 对元素截图
img = page('tag:img')
img.get_screenshot()
bytes_str = img.get_screenshot(as_bytes='png')  # 返回截图二进制文本
```



### 定位符

```python
定位符:
    page('abc')     定位页面内的 文本包含'abc'的元素
    page('.abc')    定位页面内的 class为'abc'的元素
    ele = page.ele('#abc')    定位id为'abc'的元素
    ele.next('tag:a')   定位ele元素后面的第一个a元素
    ele.eles('tag:p')   定位ele元素内所有的p元素
    ele1.ele('@name')   查找有name属性的元素    单元素@
    le1.ele('@')    没有任何属性的元素
    
    # 多属性查找@@  查找name属性为row1且class属性包含cls文本的元素
    ele2 = ele1.ele('@@name=row1@@class:cls')
    
    # 多属性或查找@|  查找id属性为one或id属性为two的元素
    ele2 = ele1.ele('@|id=one@|id=two')
    
    # 属性否定查找@!  匹配arg1不等于abc
    page.ele('@!arg1=abc')

    # 类型匹配符tag  定位div元素
    ele2 = ele1.ele('tag:div')

    # css selector 匹配符css  查找 div 元素
    ele2 = ele1.ele('css:.div')

    # xpath匹配符 xpath  查找后代中第一个 div 元素
    ele2 = ele1.ele('xpath:.//div')
```

### 匹配模式

```python
匹配模式:
    = 精准匹配
    # 获取name属性为'row1'的元素
    ele = page.ele('@name=row1')
    
    : 模糊匹配
    # 获取name属性包含'row1'的元素
    ele = page.ele('@name:row1')
    
    ^ 匹配开头
    # 获取name属性以'row1'开头的元素
    ele = page.ele('@name^ro')
    
    $ 匹配结尾
    # 获取name属性以'w1'结尾的元素
    ele = page.ele('@name$w1')
```

### 特点

```python
<iframe>和<frame>也可以查找到
建议用 Page 对象的get_frame()方法获取
使用方法与ele()一致，可以用定位符查找。

还增加了用序号、id、name 属性定位元素的功能
与 selenium 不同，本库可以直接查找同域<iframe>里面的元素。
而且无视层级，可以直接获取到多层<iframe>里的元素。
无需切入切出，大大简化了程序逻辑，使用更便捷。

# 设置查找元素超时时间为 5 秒
page.set.timeouts(5)
# 为这次查找页面独立设置等待时间（1 秒）
ele1 = page.ele('search text', timeout=1)
```



