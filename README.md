# A Friendly pymysql CURD Class
Based on Mysql.class.php   

[wyproxy](https://github.com/ring04h/wyproxy) 的web控制台, flask+pymysql    
   
不想使用sqlalchemy, 又没有好用的轮子类, 就自己造一个了   
   
## EXMPLE
```python
db = MYSQL('localhost', 'root', '', 'wyproxy', 'utf8')

data = {
    'host' : 'www.qq.com',
    'url' : 'http://www.qq.com',
}

print db.insert('capture', data)
print db.delete('capture', data)
```