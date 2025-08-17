# Tkinter

Tkinter是python的标准GUI库

GUI(图形用户界面)：

GUI并不是将整个窗口 ， 将一整个整体进行庖丁解牛 ，相当于搭积木一样 。

GUI有很多的不同功能的组件 ， 每个组件就相当于一个单独的积木块

```python
创建组件
添加组件
配置组件
```



# 布局管理

要考虑每个组件放置的位置 ， 每个组件的大小。布局管理器会自动的调整窗口中各个组件的位置以及大小

Pack布局管理器

组件：Label ， 编写窗口中的内容

title：设置窗口的标题

```python
pack（）里面的方法参数
anchor:N S E W CENTER
padx: 水平上x轴上与其他的组件的间距
pady: 水平上y轴上与其他的组件的间距
side: 设置组件的位置 TOP ， LEFT ， RIGHT ， BOTTOM
fill：设置组件是水平或者垂直方向进行添加
expand：指定组件是否可以进行拉伸
```



### Label窗口内容

```python
# 导入tkinter模块
import tkinter

# 创建主窗口对象用来容纳整个GUI程序
root = tkinter.Tk()

# 设置窗口大小
root.geometry('600x400+100+100')

# 设置主窗口对象的标题
root.title('标题')

# 窗口内容组件Label
# font 设置字体大小
lab = tkinter.Label(root,text='这是第一行内容',font=30)
lab.pack() # 对组件布局
lab = tkinter.Label(root,text='这是第二行内容',font=30)
lab.pack()

# 启动窗口
root.mainloop()
```





### Button摁键

```python
# 导入tkinter
import tkinter

# 创建窗口对象
root = tkinter.Tk()

# 设置窗口大小
root.geometry('600x400+100+100')

# 创建一个页面（创建一个容器）
frame_1 = tkinter.Frame(root)
frame_1.pack()

# 摁键1
one_button = tkinter.Button(frame_1,text='摁键1')
one_button.pack(side=tkinter.LEFT,fill=tkinter.X,padx=30)

# 摁键2
two_button = tkinter.Button(frame_1,text='摁键2',)
two_button.pack(side=tkinter.LEFT,fill=tkinter.X)

# 启动窗口
root.mainloop()
```



### Image图片&嵌套

```python
from PIL import Image , ImageTk
from tkinter import messagebox
import tkinter

# 创建窗口对象
root = tkinter.Tk()

# 设置窗口大小
root.geometry('600x400+200+200')
root.title('标题')

# 第一个页面内容
frame_1 = tkinter.Frame(root)
frame_1.pack()

# 页面内容
# font 设置字体大小
tkinter.Label(frame_1 , text='内容' , font=30 , padx=30 , pady=30).pack(side=tkinter.LEFT , anchor=tkinter.N)

# 打开图片
photo = Image.open('图片名称(本目录下)')
img = ImageTk.PhotoImage(photo)
label_img = tkinter.Label(frame_1 , image=img , padx=30 , pady=30)
label_img.pack(side=tkinter.LEFT , anchor=tkinter.N)

# 把图片帖到摁键上       bd = 0
# place 百分比布局
photo = Image.open('图片1名称')
img = ImageTk.PhotoImage(photo)

btn = tkinter.Button(frame_1 , image=img)
btn.place(relx=0.3 , rely=0.8 , anchor=tkinter.CENTER)

# 第二个页面内容
frame_2 = tkinter.Frame(root)
frame_2.pack()


tkinter.Label(frame_2 ,
              text='内容',
              font=('黑体' , 18) , # 字体&字号
              justify=tkinter.LEFT , # 左右对齐
              height= 300 , # 字体高度
              fg='red' , # 字体颜色
              padx=50
              ).pack()



```


