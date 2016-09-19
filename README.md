# A Friendly pymysql CURD Class
Based on Mysql.class.php   

[wyproxy](https://github.com/ring04h/wyproxy) 的web控制台, flask + pymysql    
   
不想使用sqlalchemy, 又没有好用的轮子类, 就自己造一个了   
   
## EXMPLE
数据库表结构   
   
```sql
CREATE TABLE `users` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `email` varchar(255) COLLATE utf8_bin NOT NULL,
    `password` varchar(255) COLLATE utf8_bin NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
```

### 初始化数据库连接
```python
# msyql dababase connection info
dbconn = MYSQL(
        dbhost = 'localhost', 
        dbuser = 'root', 
        dbpwd = '', 
        dbname = 'wyproxy', 
        dbcharset = 'utf8')
```

### 插入数据
```python
user = {'email': 'ringzero@0x557.org', 'password': '123123'}
dbconn.insert(table='users', data=user)

# change user dict, 修改用户信息提交
user['email'] = 'ringzero@wooyun.org'
user['password'] = '123456'
dbconn.insert(table='users', data=user)
```

### update 更新信息 
```python
user = {'email': 'newringzero@0x557.org', 'password': '888888'}
cond = {'email': 'ringzero@0x557.org'}
rows = dbconn.update(table='users', data=user, condition=cond)
print('update {} records success..'.format(rows))
```

### delete data, 删除数据, limit参数为删除少条
```python
cond = {'email': 'ringzero@0x557.org'}
rows = dbconn.delete(table='users', condition=cond, limit='1')
print('deleted {} records success..'.format(rows))
```

### select 查询信息
```python
fields = ('id', 'email')
cond = {'email': 'ringzero@wooyun.org'}
rows = dbconn.fetch_rows(
                    table='users', 
                    fields=fields, 
                    condition=cond, 
                    order='id asc', 
                    limit='0,5')

for row in rows:
    print(row)

# 不指定 fields 字段, 将返回所有*字段, 
# 不指定 order, 将不进行排序
# 不指定 limit, 将返回所有记录

rows = dbconn.fetch_rows(
                    table='users', 
                    condition=cond,
                    limit='0,5')
for row in rows:
    print(row)
```

### query 执行自定义SQL语句
```python
sql = 'select * from users limit 0, 5'
rows = dbconn.query(sql)
for row in rows:
    print(row)
```