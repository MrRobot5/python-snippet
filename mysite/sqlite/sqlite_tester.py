# -*- coding:utf-8 -*-

# 可视化工具
# https://sqlitestudio.pl/index.rvt?act=download

# 导入sqlite3模块
import sqlite3

# 创建链接对象
# 打开一个到 SQLite 数据库文件 db.sqlite3 的链接
# 如果该数据库不存在则会自动创建，可以指定带有文件路径的文件名
conn = sqlite3.connect('db.sqlite3')

# 获取游标对象用来操作数据库
cursor = conn.cursor()

# 插入user表
# id int型　主键自增
# name varchar型　最大长度２０　不能为空
# cursor.execute('''create table user(id integer primary key autoincrement,name varchar(20) not null)''')

cursor.execute('''insert into user(id,name) values(null,'xiaoqiang')''')
conn.commit()

cursor.execute('SELECT * FROM user')
print cursor.fetchall()

# 修改id=1记录中的name为xiaoming
cursor.execute('''update user set name='xiaoming' where id=1''')
conn.commit()

cursor.close()
conn.close()
