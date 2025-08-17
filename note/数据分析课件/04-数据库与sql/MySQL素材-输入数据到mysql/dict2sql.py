# -*- coding: utf-8 -*-


import pandas as pd
from sqlalchemy import create_engine


#个人
user = "root"  #用户名
password = "mysql" #密码
addr = "127.0.0.1:3306"  #ip:port
db_name = "python_db" #库名
chase = "utf8"  #编码方式
table_name = "student1"  #表名


df = pd.read_csv('mydata.csv')
print(df)

engine = create_engine("mysql+pymysql://{}:{}@{}/{}?charset={}".format(user, password, addr, db_name,chase))
con = engine.connect()#创建连接
res = df.to_sql(table_name, con, index=False, if_exists='append', chunksize=5000) #if_exists=‘replace’
# res = df.to_sql(table_name, con, index=False, if_exists='replace', chunksize=5000) #if_exists=‘replace’