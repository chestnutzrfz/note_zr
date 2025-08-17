# windows编程



### 获取鼠标位置

```python
import pyautogui as pgui

while 1:
    print(pgui.position())
    # 输出鼠标的位置
```



### 模拟点击

```python
import time
import win32api as api
import pyautogui as pgui


# # 通过图标启动  通过pgui这个模块的识图功能, 找到图片并点击
# qq = pgui.locateAllOnScreen('qq.png')
# pgui.doubleClick(qq)   # 找到qq的图片  图标 并双击  wrong

# 1.通过指令启动  cmd
# api的工具箱可以直接启动
qq = r'E:\qq\Bin\QQScLauncher.exe'
api.ShellExecute(0,'open',qq,None,None,1)  # 固定None 0 1  文件路径,连带的影响..      打开qq程序

time.sleep(3)
# 2.选中输入框
user = pgui.locateOnScreen(r'zhanghao.png')
pgui.click(user)     # 点中图片   需要向右边偏移一点
pgui.moveRel(70,0)      # 向右移动
pgui.click()

# 3.输入数据
# 传入按键值给函数, 函数实现输入
def input_code(*args):
    for i in args:
        api.keybd_event(i,0)    # 模拟按键输入

# 传入的值是ascii//unicode码  不能直接传字符
input_code(55,48,53,50,48)  # 70521

# qq号输入完毕,鼠标往下一点  点  输入密码
pgui.moveRel(0,50)      # 向下移动50像素
pgui.click()

input_code(55,48,53,50,48)

# 点击登录
# login = pgui.locateOnScreen(r"login.png")
# pgui.click(login)
pgui.moveRel(0,100)
pgui.click()
```

