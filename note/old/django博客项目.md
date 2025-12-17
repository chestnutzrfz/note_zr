##### 博客项目

# 版本

版本升级 --> 功能越多

可能很不稳定

开发中 强调 -->  最稳定的版本

django -> 第三方模块

pip install django==2.2 

pip install django==4.4  --->  会先把2.2版本的卸掉 重新安装4.4版本的    覆盖掉

之前用2.2写的项目不能用了 ...



### 虚拟环境

利用python第三方模块

##### 下载模块

```
pip install virtualenvwrapper-win		# windows 上使用
```



##### 创建虚拟环境

```
mkvirtualenv 要创建的虚拟环境的名字
# 默认是在用户目录下
# 可以修改 指定创建在哪里
# 环境变量 添加WORKON_HOME ,位置 D:\Env  重启电脑生效
```



##### 查看虚拟环境

```
lsvirtualenv     # 列出所有虚拟环境
workon			# 也可以列出所有
```



##### 进入虚拟环境

```
workon 要进入的虚拟环境的名字
```



##### 退出虚拟环境

```
deactivate
```



##### 删除虚拟环境

```
rmvirtualenv 要删除的虚拟环境的名字
# 本质上就是将虚拟环境对应的文件夹删掉
```



### venv  黄色文件夹

创建项目  配置解释器路径 选择 new    pycharm会创建虚拟环境

不要过度依赖pycharm    linux中没有pycharm  要习惯命令





# django项目

先进入虚拟环境   在虚拟环境中下载django2.2

找到想要创建项目的路径cmd, 进入虚拟环境,创建django项目

启动时  先进入虚拟环境和目录  再python manage.py runserver