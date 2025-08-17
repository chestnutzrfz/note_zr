# 初识数据库

#### 数据库



##### 1.数据库

数据库系统阶段：专门的数据库来管理数据

​	特点：有数据库管理系统统一管理 ， 共享性比较好



数据库（database）：指可以长期保存在计算机内 ， 以及管理数据的仓库 ；数据按照一定的格式进行存储 ， 用户可以对数据库中的数据进行增删改查的操作。



数据库管理系统（DBMS）：用于建立，使用以及维护数据库。位于用户以及操作系统之间的位置。



常见的DBMS：MySQL ， Oracle、SQL sever、MongoDB……



##### 2.分类

数据库分为两类：关系型数据库 ， 非关系型数据库

1、关系型数据库

关系型数据库是一个结构化的数据库 ， 创建在关系模型上（二维表格）基础上 ，一般面向于记录数据。都是使用表结构并且格式一致。

相当于excel表格 ， 由行跟列组成的一个表格。

关系型数据库：MySQL ，  Oracle、SQL sever……

2、非关系型数据库

存储数据格式为key  ， value形式 ， 文档形式、 图片形式等等，使用灵活 ， 应用场景广泛。

非关系型数据库：MongoDB……

使用数据库：可以存储大量的数据 ， 方便用户查询 ， 以及访问；安全性以及共享性高。



##### 3.使用

启动MySQL ， net start mysql80

停止MySQL：net stop mysql80

进入mysql：mysql -uroot -p

再navicat中创建mysql连接 。 1、选择连接mysql ， 2、填入连接名以及密码，3、点击测试连接 ， 测试连接成功点击确定

右击连接名 ， 点击打开连接

#### SQL

##### 1.了解sql

结构化查询语言 ， 用于存取， 查询 ， 更新以及管理关系型数据库

SQL是关系型数据库的使用比较广泛的语言 ， 是各种数据库的交互基础

##### 2.sql指令

1、DDL：数据定义语言（用来完成对数据库中的创建 ， 删除 ， 修改表结构等的操作）create

2、DQL：数据查询语言（对数据库中的表数据进行查询）select

3、DML：数据操作语言（对表中的数据进行增删改）insert

4、TPL：事务控制语言：（用于管理数据库中的事务）

5、DCL：数据控制语言（定义数据库的访问权限 ， 安全级别）



##### 3.sql写法规则

1、每条sql语句要以分号结束;

2、使用空格隔开让代码的可读性高一些

3、sql不区分大小写的.(关键字使用大写 ， 其他的使用小写)

4、注释：使用两个减号假一个空格也可以是一个#



# mysql库操作

##### 1.数据库查询

```mysql
show databases;	
```

在MySQL安装好之后会有一些系统默认的数据库：

1、information_schema：这个是虚拟库 ， 不占用磁盘空间，存储时数据库启动之后的参数。
2、mysql：是一个授权库，主要存储系统用户的权限信息
3、performance_schema：这个是MySQL5.5后开始新增的数据库 ， 用于收集数据库服务器的性能参数等。
4、sakila：这个是MySQL提供的样例数据库 
5、sys：这个是数据主要是提一些视图 ， 让开发者可以查询性能问题。
6、world：是MySQL自动创建的。



##### 2.数据库创建

```
create database 数据库名称 character set 编码(一般是utf-8)；
```



##### 3.查询创建数据库的所以信息

```
show create database 数据库名称；
# 返回的是创建数据库名称，这个数据库使用的字符编码
```



##### 4.修改数据库的编码

```
alter database 数据库名称 character set 字符编码；
```



##### 5.查看当前所在数据库

```
select database();
# 查看当前所在数据库，需要想切换入数据库，否则会返回nill（空）
```



##### 6.切换数据库

```
use 数据库名称
```



##### 7.删除数据库

```
drop database 数据库名称;
```



# mysql表操作

### 1.数据类型

##### 1.1字符串类型

```
1.char(n);  # 最大能存储255个字符；n表示长度
2.varchar(n);  # 最大能存储65535个字符
3.enum:  # 在指定的数据中选择一个数据（单选）
4.set:  # 在指定的数据中可以选择多个（多选）
```



##### 1.2数值类型

```
1.int（n）;  # 存储整数范围在+-21亿以内的11位整数
2.float(m,d)；  # 单精度浮点型，留存小数点6-7位（m：表示的数据的总长度，d：小数位数）
3.double(m,d);  # 双精度浮点型，留存小数点后15位
# 浮点型会出现精度丢失问题
```



##### 1.3时间类型

```
1.date：年月日(年-月-日)
2.time: 时分秒(时:分:秒)
3.datetime: 年月日 时分秒 (年-月-日 时:分:秒)
4.year: 年
# 写入世界时是需要用引号包裹的
```

### 2.数据库的创建

```
create table 表名(
	字段名 数据类型，
	字段名 数据类型，
	字段名 数据类型
);
# 写到最后一个字段时，不需要加逗号

create table student(
	id int(5),
	name varchar(10),
	sex char(1),
	day date
);

```



### 3,对数据库增加数据

```
# 完整的按照数据表的顺序插入数据
insert into 表名 values(数值...);

# 同时插入多条数据
insert into 表名 values
(数值....),
(数值....),
...
(数值....);
```



### 4.数据库的查询

```
# 查看表中的所以内容
select * from 表名;
```



### 5.使用数据库

```
-- 使用数据库

use class1;

-- 编码 ， 名称 ， 价格 ， 分类
-- 创建表的代码不能重复运行
```



### 6.查看表结构

```
desc 表名;
```



### 7.表数据操作

##### 1.字段的增加

```
# 默认在表末尾增加
alter table 表名 add 字段名 字段类型;
# 添加在第一个字段
alter table 表名 add 字段名 字段类型 first;
# 添加到某一个字段以后
alter table 表名 add 字段名 字段类型 after 字段名(被指定);

```





##### 2.字段长度的修改

```
alter table 表名 modify column 字段名 数据类型（长度);
```

注意：修改长度不能小于原有的长度 ， 否则原有数据会被破会 ， 不可修复。



##### 3.字段数据类型的修改

```
alter table 表名 modify 字段名 数据类型(长度)；

```



##### 4.字段名修改

```
alter table 表名 change 旧的字段名 新的字段名 新的数据类型;
```



##### 5.字段的删除

```
alter table 表名 drop column 字段名;
```



##### 6.修改表名

```
alter table 表名 rename 新的表名；
```



##### 7.清空表数据

```
delete from 表名;
```



##### 8.删除表

```
drop table 表名;
```



##### 9.数据插入

```
# 完整的按照顺寻的插入字段
insert into 表名values(值...)
# 指定字段插入数据
insert into 表名(字段名, ...) values (值...);
```



##### 10.字段查询

```
# 获取整个表中的所有字段
select * from 表名;

# 获取查询指定字段
select 字段名， ... from 表名;
```



# 约束条件

### 1.not null;

非空约束， 表示该字段不能为空；插入数据值必须要给传值

```
  create table t1(
  id int not null
  );
```



### 2.默认值

在该字段中如果没有数据的传入，会默认的将默认值进行填充

```
create table t2(
sex enum('男','女') default ('男')
);
```



### 3.unique

字段值是唯一的，不能重复

```
create table t3(
id int unique
)；
```



### 4.primary key

主键约束，确保字段数据唯一却不能为空(相当于not null + unique)

```
create table t4(
id int primary key
);
```



### 5.auto_increment

自动增加(要把字段设置成一个主键), 会默认设置一个int类型的值从1开始， 每增加一个数据，会在上一条的基础上+1

```
create table t5(
id int primary key auto_increment
)；
```









# 数据查询

``` mysql
# 查询表中所以字段的所有数据
select * from 表名;
# 查看指定字段的数据
select 字段名，... from 表名;
```

### 1.where 子句

```mysql
=	等于
!=	不等于
>	大于
<	小于
>=	大于等于
<=	小于等于	


逻辑运算符
and  与
or	 或者
not  非


between	在两个值之间
not between 不在两个值之间
in 在指定集合内
not in 不在指定集合内
```



### 2.聚合函数

```mysql
avg(字段名)	-- 平均值
max(字段名)	-- 最大值
min(字段名)	-- 最小值
sum(字段名)	-- 求和
count(字段名)	-- 统计数据数据长度
```



### 3.as

as : 对字段重命名





# 数据更新

### 1.表数据修改

```python
update 表名 set 字段名 = 值…… where 条件;
-- 如果后面没有添加where子句的话 ， 会将整个字段的所有数据进行修改
```



### 2.表数据删除

```python
delete from 表名 where 条件
-- 如果后面没有添加where子句的话 ， 会将表中的记录全部清空
```



# 数据查询进阶

### 1.模糊查询

##### 1、like子句

在where子句中 ， 可以使用该子句以及关键字结合实现模糊**查找**

```python
select * from 表名 where 字段名 like '关键字';
```

##### 2.通配符

```python
%：表示匹配0个或者多个字符(NULL除外)
_: 表示匹配任意一个字符
可以在通配符前面或者后面指定文字
```



### 2.消除重复项

对查询的结果去重——distinct

```python
select distinct * from 表名;
select distinct 字段名 from 表名;
```



### 3.排序

在查询中添加排序 ， 按照自定的字段进行排序（升序 ， 降序）—— order by

```python
select * from 表名 where 条件 order by  字段名 desc;
select * from 表名 order by  字段名 desc;
```

根据order by指定的排序

asc ： 按照指定字段进行升序排序（默认的）

desc: 按照指定字段进行降序排序



### 4.分组

根据指定的字段进行分组

```python
select * from 表名 where 条件 group by 字段名(指定分组的字段)
select * from 表名 group by 字段名(指定分组的字段)
-- 没有where子句的话 ， 获得结果就是每类分组的第一个数据
```



5.限制查询条数（分页）

limit子句限制查询返回的数据条数

```
select * from 表名 limit 返回数量;
select * from 表名 where 条件 limit 返回数量;

select * from 表名 limit 起点 ， 返回数量;
```

```
-- select * from t2 limit 2;
select * from t2 limit 1 , 4;
select * from t2 limit 2 , 4;
```



# 数据查询

### 1、聚合筛选

having对分组之后的数据进行筛选 ，where只能操作表中的字段 ， having可以和聚合函数联合

注意：having必须和group by一起使用(avg  , max , min , sum  , count)

```
select * from 表名 where 条件 group by 字段名 having 条件;
```

```
-- select sex , count(id) from t1  where grade>0 group by sex;
select sex , count(id) from t1  group by sex having avg(grade)>85;
```



### 2、子查询

在一个select语句中 ， 嵌套进去另一个select语句 ， 那么被嵌套的select语句称之为子查询语句 ， 外部select语句称之为主查询。

```
select * from (select * from 表名 where 条件) as 表名 where 表名.条件;
select * from 表名 where 条件 (select * from 表名 where 条件);
```

```
-- select * from t1 where sex='女' and grade>95;
-- 情况一：在select中嵌套 ， 查询得到的结果作为一个表的内容 ， 交给外层查询 ， 此时得到的新表要用as对表进行取名 ， 方便后续操作
select * from (select * from t1 where sex='女') as s where s.grade>=90;

-- 情况二：在where子句中嵌套 ， 查询得到的结果必须是一个确切的数据 ， 不能是多行多列的表格，返回的结果就是交给外层进行条件筛选
select * from t1 where grade<(select grade from t1 where name='张三');
```



### 3、运算符

在查询得到的结果中做运算

```
select name , grade-5 as grade from t1;
select * from t1;
```



# 表与表的关系

### 1、多表之间的关系

```
1、一对一
	身份证号：一个人只能又一个身份证号 ， 一个身份证号只能对应一个人
	DNA  
	
2、一对多
3、多对一
	班级（一个）--学生（五六百号人）
	学生（一个人）—— 班级（多个（基本 ， 高级 ， 前端补充 ， 全栈 ， 高薪））
4、多对多
	城市 -- 个人 （一个人可以去多个城市 ， 一个城市可以有多个人）
```



### 2、外键约束

foreign key：建立表与表之间的某种约束关系 ， 这个关系的存在 ， 可以让表与表之间的数据关联性更强 ， 数据较完整。

主表：被外键连接的

从表：设置外键进行连接

注意：主表必须先创建 ， 才能创建从表进行外键约束；

```
foreign key (外键字段名) references 主表名(字段名)
```

```
create table t2(
id int(4) primary key auto_increment,
name varchar(5)
);

create table t3(
id int(4) primary key auto_increment,
age int(3),
class char(2),
-- 创建一个字段作为外键约束  让表之间成为一对一的关系
t3_id int unique,
foreign key (t3_id) references t2(id)
);

insert into t2(name) values
('傅耀武'),
('马晨旺'),
('朱晓际'),
('王鑫'),
('汪常正'),
('黄明辉');

insert into t3(age , class, t3_id) values (28 , '八班', 5);
insert into t3(age , class, t3_id) values (20 , '七班', 4);
insert into t3(age , class, t3_id) values (21 , '七班', 3);
insert into t3(age , class, t3_id) values (22 , '七班', 2);
insert into t3(age , class, t3_id) values (23 , '七班', 1);
insert into t3(age , class, t3_id) values (24 , '七班', 6);
```

在外键约束中

```
restrict(默认) 
on delete restrict
on update restrict
当主表要删除数据的时候 ， 从表有数据相关联的时 ， 则不允许主表数据删除（修改也一样）
```



# MySQL多表查询

