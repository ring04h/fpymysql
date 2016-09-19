# A Friendly pymysql Class
home: http://github.com/ring04h/fpymysql
base on Mysql.class.php

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