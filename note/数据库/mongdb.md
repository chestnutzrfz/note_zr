Mongdb

### 安装

在虚拟机centos中安装

```python
1.在/etc/yum.repos.d 创建一个 mongodb-org.repo 文件
    sudo touch /etc/yum.repos.d/mongodb-org.repo
2.编辑 mongodb-org.repo 文件
    sudo vi /etc/yum.repos.d/mongodb-org.repo  按a进入inset模式
3.输入以下内容后 保存退出
// 把前面空格sahn'di'a
    [mongodb-org]
    name=MongoDB Repository
    baseurl=http://mirrors.aliyun.com/mongodb/yum/redhat/7Server/mongodb-org/3.2/x86_64/
    gpgcheck=0
    enabled=1
4.安装MongoDB
    sudo yum install -y mongodb-org
5.启动MongoDB
    sudo service mongod start
    // sudo service mongod restart 修改配置文件后重启
6.设置开机启动
    sudo chkconfig mongod on
7.打开MongoDB
// 先修改配置文件再打开
    sudo /bin/mongo
8.修改mongodb配置文件
	sudo vi /etc/mongod.conf
	将bindip 127.0.0.1 换成0.0.0.0
```

### 关系型数据库和非关系型数据库区别

```
关系型数据库  mysql
	主键: 数据上面的关联性
	不区分大小写

非关系型数据库  mongodb
	区分大小写

关系型数据库中的数据库，MongoDB中也叫数据库；
关系型数据库中的表，MongoDB中称为集合；
关系型数据库中的行或记录，MongoDB中叫做文档
数据之间无关联性

SQL中需要增加外部关联数据的话，规范化做法是在原表中增加一个外键，关联外部数据表

NoSQL则可以把外部数据直接放到数据集中，以提高查询效率，缺点也比较明显，对关联数据做更新时会比较麻烦

SQL中在一个表中的每条数据的字段是固定的，而NoSQL中的一个集合（表）中的每条文档（数据）的key（字段）可以是互不相同的

Mongodb作为非关系型数据库相较于关系型数据库的优势

易扩展：NoSQL数据库种类繁多，但是一个共同的特点都是去掉关系型数据库的关系型特性，数据之间无关系

大量数据，高性能：NoSQL数据库都具有高的读写性能，数据库的结构简单

灵活的数据模型：NoSQL无需事先为要存储的数据建立字段，可以自定义格式存储

mysql的引擎
支持事务的引擎: innodb(需要指定)
适合io操作的引擎: myisam(默认)

```

### mongodb介绍

```
优势:

易扩展： NoSQL数据库种类繁多， 但是⼀个共同的特点都是去掉关系数据库的关系型特性。 数据之间⽆关系， 这样就⾮常容易扩展⼤数据量，

⾼性能： NoSQL数据库都具有⾮常⾼的读写性能， 尤其在⼤数据量下， 同样表现优秀。 这得益于它的⽆关系性， 数据库的结构简单

灵活的数据模型： NoSQL⽆需事先为要存储的数据建⽴字段， 随时可以存储⾃定义的数据格式。 ⽽在关系数据库⾥， 增删字段是⼀件⾮常麻烦的事情。 如果是⾮常⼤数据量的表， 增加字段简直就是⼀个噩梦
```

### mongodb使用(对比mysql)

```
1.查看数据库
mysql: show databases;
mongodb: show dbs;

local数据库(默认虚拟数据库)

2.插入一个数据到数据库中所执行的步骤
mysql: 创建库  创建表  插入数据
mongodb: 
	切换库: use 数据库名称   // 自动创建虚拟数据库   插入数据时就创建了
	插入数据: db.test.insert({"name":"zr"})	 // test 虚拟的集合	相当于mysql的表

3.读取数据
mysql:	select * from....
mongodb:  db.集合名称.find() 	//查询条件  若无读取所有

_id 类似mysql主键(没有关系性)	自动创建 没有规律

4.修改数据
mongodb: 	db.test.update(原字典,修改后的字典)	//仅修改第一条

修改所有
db.test.updateMany({查询条件},{"$set":{新字典}})

5.删除数据
mongodb:	db.test.remove({查询条件})	//删除所有
```

### mongodb与python互联

```python
# 下载模块
# pip install pymongo==3.11.1
# 导包
from pymongo import MongoClient

# 1.创建连接mongodb数据库的对象
# mongo = MongoClient('ip',27017)
mongo = MongoClient('192.168.12.128', 27017)

# 2.创建数据库和集合
db = mongo['class']['data']

# 3.插入数据    insert 过时建议使用新的语句
# db.insert({"name":'zr',"age":"20"})
# db.insert_one({"name":"te","age":"16"})
# db.insert_many([
#     {"name":"jd","age":"10"},
#     {"name":"zds","age":"13"},
#     {"name":"jwq","age":"30"},
#     {"name":"jvcx","age":"17","sex":"woman"},
#     {"name":"dfsa","age":"14","sex":"man"},
# ])

# 4.修改数据    update 已过时 建议使用其他方法
# db.update({"name":"jd"},{"name":"jd","job":"study"})  # 覆盖之前的数据 更新键值对

# 纠正更新
# db.update_one({"age":"20"},{"$set":{"age":"13"}})

# update两个参数的使用
# 默认修改第一条
# db.update({"age":"13"}, {"$set":{"sex":"man"}})

# 修改所有
# db.update({"sex":"man"}, {"$set":{"sex":"girl"}}, multi=True)

# 没有的数据运行结果
# db.update({"age":"26"}, {"$set":{"sex":"girl"}}, upsert=True)
# 如果不存在的查询条件 则将查询条件和修改的内容合并为一条数据 插入到数据库中

# 查询数据
# _id不要动会报错
# for i in db.find():
#     print(i)

# print([i for i in db.find()])
# 忽略_id
# data = []
# for i in db.find():
#     dict1 = {}
#     for key,value in i.items():
#         if key == '_id':
#             continue
#         else:
#             dict1[key] = value
#     data.append(dict1)
# print(data)

# 列表推导式
# print([{key:value for key,value in i.items() if key != '_id'} for i in db.find()])

# 删除数据
# db.remove({条件})   # 删除所有条件的数据

# 删除所有数据
# db.remove()

# 删库跑路      在终端中执行
# db.dropDatabase()

```

