### 安装flask

```
#建议大家初学使用flask1.0版本,直接装高版本也可以
pip install flask==1.1.2
# 低版本报错太多了
pip install flask==2.0.2
```

### 创建项目

```python
from flask import Flask
app = Flask(__name__)  
if __name__ == '__main__':
    app.run(debug=True)
    # debug=True 自动重启 不需要再手动重启
```

运行后可以在浏览器访问
http://127.0.0.1:5000/ ---->  resoponse

### 创建路由

```python
@app.route('/')		# 路径
def index():	# 函数名
    return 'ok'  # flask 可直接返回字符串,会自动封装成httpresponse
```

### 使用静态文件

创建templates文件夹

里面创建html静态文件

创建static文件夹

里面放入图片

在index.html文件中导入图片

```python
from flask import Flask
from flask import render_template

app = Flask(__name__,static_folder='static',template_folder='templates')   
# 实例化一个flask项目  创建一个服务器  固定写法
# static_folder 和 template_folder 会配置静态文件位置  可以改名字  不写会默认


@app.route('/')
def index():
    return render_template('index.html')    # flask会直接找到templates文件夹中的文件


if __name__ == '__main__':
    app.run()   # 运行服务器
```

### 使用配置文件

创建config文件夹

创建base_settings文件

写入配置信息		1.加载文件方式加载配置, 配置必须大写生效

创建类完成配置	2.加载类的方式加载配置

```python
from flask import Flask,current_app

app = Flask(__name__)  # 实例化一个flask项目  创建一个服务器  固定写法
app1 = Flask(__name__)


# 方法1: 加载文件的方式加载配置, 配置必须大写生效
app1.config.from_pyfile('config/base_settings.py')


class BaseConfig:
    B = 'aa'


# 方法2: 加载类的方式加载配置
app1.config.from_object(BaseConfig)


@app1.route('/')
def index():
    print('a:', app1.config.get('A'))  # 获取配置信息
    print("B:",current_app.config.get("B")) #current_app实际上就是app的映射，把其看成app即可
    return 'ok'


if __name__ == '__main__':
    app1.run(debug=True)  # 运行服务器

```

### 路由配置



```python
from flask import Flask,request,render_template

app = Flask(__name__)   # 实例化一个flask项目  创建一个服务器  固定写法


# post请求
@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        print('get')
        return render_template('index.html')
    elif request.method == 'POST':
        print('post')
        return 'post'
    return 'ok'


if __name__ == '__main__':
    print(app.url_map)   # 查看当前app的所有路由
    app.run(debug=True)   # 运行服务器

```

```python
# 同一个url规则去装饰不同的视图函数 只会匹配第一个
# return 'login0'

@app.route('/login',methods=['GET','POST'])
def login():
    return 'login0'

@app.route('/login',methods=['GET','POST'])
def login1():
    return 'login1'
```

```python
# error 不能有相同的视图函数名

@app.route('/index',methods=['GET','POST'])
def index():
    return 'index'

@app.route('/index1',methods=['GET','POST'])
def index():
    return 'index'
```

```python
# 同一个试图函数装饰不同的路由规则  均生效

@app.route('/index')
@app.route('/index1')
def index1():
    return 'index'
```

### 反向解析

```python
from flask import Flask,url_for

app = Flask(__name__)

@app.route('/hello')
def hello():
    return f"解析index1的路由: {url_for('index1')}"     # 指的是视图函数index, url_for会解析出他的路由
# /index1

    return f'<a href="{url_for("index1")}">链接</a>'      # 跳转路由


if __name__ == '__main__':
    print(app.url_map)
    app.run(debug=True)

```

### 动态路由

```python
from flask import Flask

app = Flask(__name__)

# <int: que> que为int类型 若输入其他类型则错误     注意接收que
# <数据类型约束:变量名> 
@app.route('/qus/<int:que>/answer/<int:ans>')
def qus_ans(que,ans):
    return f'que: {que},ans: {ans}'


# 如果不给数据类型约束 则支持所有类型        最好有约束
@app.route('/qus/<int:que>/answer/<ans>')
def qus_ans(que,ans):
    return f'que: {que},ans: {ans}'

if __name__ == '__main__':
    app.run(debug=True)
```

### 正则转换器

```python
from flask import Flask
from werkzeug.routing import BaseConverter
app = Flask(__name__)


class RegexConverter(BaseConverter):
    # 重写父类init方法
    def __init__(self, url_map, *args):
        # 调用父类的方法,需要将url_map路由表传给父类
        super().__init__(url_map)
        # 获取到的参数  是路由规则的表达式
        self.regex = args[0]
    
    # to_python to_url 写不写均可  会默认
    # to_python : 从正则匹配到参数之后可以在这里处理操作返回字符串value,然后再返回给试图函数的参数
    def to_python(self, value: str):
        # new_value = int(value) + 1
        # return str(new_value)
        return value
    
    # 反向解析传参时会执行
    def to_url(self, value):
        return value
        
        
# 注册
app.url_map.converters['reg'] = RegexConverter

# 正则表达式写在 reg("")里面
@app.route('/reg/<reg("\d{6,12}@qq.com"):qqemail>')
def reg1(qqemail):
    return f'reg_name: {qqemail}'


if __name__ == '__main__':
    app.run(debug=True)

```

```python
# 正则加反向解析
@app.route('/reg/<reg("\d{3}"):name>')
def numb(name):
    return f'reg_num: {name}'


@app.route('/name_url_for')
def name_url_for():
    # url_for 反向解析
    return url_for('numb',name='123')
```

```python
# 最后的/ 有没有都会自动匹配   不要轻易在路由后加/
# 有时候需要匹配/  <path:>
@app.route('/qus/<path:f>')
def qus(f):
    return f'que: {f}'
```

### 请求参数

```python
@app.route('/',methods=['GET','POST'])
def index():
    print(request.method) #获取请求方式
    # print(request.headers) #获取请求头信息
    #获取get请求参数
    query = request.args #ImmutableMultiDict
    print("query---》",query)
    # print(query["wd"])#不推荐
    print(query.get("pwd")) #推荐 获取不到会返回None 当有多个的时候，只返回第一个
    print(query.get("name"))
    print(query.getlist("name")) #获取的一键多值，返回list
    print("我是分割符".center(50,"*"))


    #获取post请求参数
    form_data = request.form #ImmutableMultiDict
    print("form_data---》",form_data)
    print(form_data.get("id"))
    print(form_data.get("name")) #推荐 获取不到会返回None 当有多个的时候，只返回第一个
    print(form_data.getlist("name"))  # 获取的一键多值，返回list
    print("我是分割符".center(50, "*"))

    #同时获取get请求和post请求参数
    query_form_data = request.values #CombinedMultiDict
    print(f"query_form_data---》:{query_form_data}")
    print(query_form_data.get("pwd"))
    print(query_form_data.get("id"))
    print(query_form_data.get("name")) #推荐 获取不到会返回None 当有多个的时候，只返回第一个
    print(query_form_data.getlist("name"))  # 获取的一键多值，返回list

    return 'ok'
```

### 获取文件

```python
@app.route('/upload', methods=['post'])
def upload():
    save_path = './static'
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    # print(request.files) #ImmutableMultiDict([('pic', <FileStorage: '美女.png' ('image/png')>)])
    # txt = request.files.get("txt")
    # txt.save(os.path.join(save_path, txt.filename))  # 保存图片

    # 用文件原始名字保存，不推荐
    # pic = request.files.get("pic")
    # pic.save(os.path.join(save_path,pic.filename )) #保存图片


    #用secure_filename（对中文不友好，相同的文件名会被覆盖）
    # pic = request.files.get("pic")
    # pic.save(os.path.join(save_path, secure_filename(pic.filename)))  # 保存图片

    # #用hashlib （对中文友好，相同的文件名会被覆盖）
    # pic = request.files.get("pic")
    # ends = os.path.splitext(pic.filename)[-1]  # 获取文件名后缀
    # f_has = hashlib.md5()
    # f_has.update(pic.filename.encode('utf-8'))
    # save_name = f_has.hexdigest() + ends
    # print(f"save-name:{save_name}")
    # pic.save(os.path.join(save_path, save_name))  # 保存图片

    # 用uuid （不会覆盖,推荐）
    pic = request.files.get("pic")
    ends = os.path.splitext(pic.filename)[-1]  # 获取文件名后缀
    name = str(uuid.uuid4()).replace('-', '')  # 生成一个唯一标识
    save_name = name + ends
    print(f"save-name:{save_name}")
    pic.save(os.path.join(save_path, save_name))  # 保存图片
```





