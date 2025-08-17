# selenium和webdriver

Selenium是一个web的自动化测试工具,最初是为网站自动化测试而开发的,selenium考科一直接调用浏览器,它支持所有主流的浏览器.我们可以使用selenium很容易完成爬虫.webdriver可以理解为浏览器的驱动.

selenium本质是通过驱动浏览器.完全模拟浏览器的操作.比如跳转,输入,点击,下拉等,来拿到网页渲染 之后的结果,可支持多种浏览器

**pip install selenium == 3.141.0**

下载浏览器驱动程序:

- https://registry.npmmirror.com/binary.html?path=chromedriver/&spm=a2c6h.24755359.0.0.1c384dccQ9PaJR
- https://msedgewebdriverstorage.z22.web.core.windows.net/
- edge的驱动需要换名字：`MicrosoftWebDriver.exe`

卸载: pip uninstall 模块名



# 浏览器对象

- get(url=url)    地址栏输入url地址并确认
- page_source    HTML结构源码
- maximize_window()    浏览器窗口最大化
- quit()    关闭浏览器



# selenium定位元素

from selenium.webdriver.common.by import By

- find_element(By.Id,'根据标签id属性进行定位')
- find_element(By.NAME,'根据标签name属性进行定位')
    - find_element(By.CLASS_NAME,'根据标签class属性进行定位')

- find_element(By.XPATH,'根据xpath语法进行定位')
- find_element(By.CSS_SELECTOR,'根据css语法进行定位')
- find_element(By.LINK_TEXT,'根据标签文本内容进行定位')
- get_attribute('要找的属性')  获取attr元素的属性

```python
import time

from selenium import webdriver
from selenium.webdriver.common.by import By


url = 'https://www.baidu.com/'

driver = webdriver.Chrome()
driver.get(url)

driver.maximize_window()

def get_data():
    dds = driver.find_elements(By.XPATH,'//*[@id="s-top-left"]/a')
    for dd in dds:
        print(dd.text.split("\n"))
        print('-' * 100)

get_data()

time.sleep(1)

driver.quit()
```



# 无界面模式

```
from selenium import webdriver

options = webdriver.ChromeOptions()
# 添加无界面参数
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
```



# 打开新窗口和切换页面

selenium中没有专门的打开新窗口的方法,是通过execute_script()来执行js脚本的形式来打开新窗口的.

```
window.execute_script("window.open('https://www.douban.com/')")
```

打开新窗口后driver当前的页面依然还是之前的,如果想要获取新的窗口的源代码,那么就必须要先切换过去.

```
window.switch_to.window(driver.window_handles[1])
```



# selenium-iframe

网页中嵌套了网页,先切换到iframe,然后再执行其他操作

- 切换到要吃力的Frame

  ```
  browser.switch_to.frame(frame节点对象)
  ```

  

- 再Frame中定位页面元素并进行操作

- 返回当前处理的Frame的上一级页面或主页面

  ```
  # 返回上一级
  browser.switch_to.parent_frame()
  # 返回主页面
  browser.switch_to.default_content()
  ```

  

# 操作cookie

- 获取cookie:   driver.get_cookies()
- 根据cookie的key获取value:   value = driver.get_cookie(key)
- 删除所以的cookie:   driver.delete_all_cookies()
- 删除某个cookie:   driver.delete_cookie(key)



# 隐式等待和显式等待

- 隐式等待 :  制定一个时间,在这个时间内一直会处于等待状态.隐式等待需要使用  

  driver.implicitly_wait

- 显式等待指定在某个时间内，如果某个条件满足了，那么就不会再等待。显式等待用的方法是 

  from selenium.webdriver.support.ui import WebDriverWait

