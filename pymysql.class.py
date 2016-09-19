# encoding: utf-8

"""
author: ringzero@0x557.org
home:   http://github.com/ring04h/fpymysql
desc:   A Friendly pymysql Class

"""

import pymysql

class MYSQL:
    """A Friendly pymysql Class, Provide CRUD functionality"""

    def __init__(self, dbhost, dbuser, dbpwd, dbname, dbcharset):
        self.dbhost = dbhost
        self.dbuser = dbuser
        self.dbpwd = dbpwd
        self.dbname = dbname
        self.dbcharset = dbcharset
        self.connection = self.connect()

    def connect(self):
        """Connect to the database"""
        connection = pymysql.connect(
                host = self.dbhost,
                user = self.dbuser,
                password = self.dbpwd,
                db = self.dbname,
                charset = self.dbcharset,
                cursorclass=pymysql.cursors.DictCursor)
        return connection

    def insert(self, table, data):
        """mysql insert() function"""
        with self.connection.cursor() as cursor:
            params = self.join_field_value(data);
            sql = "INSERT INTO {table} SET {params}".format(table=table, params=params)

            result = cursor.execute(sql)
            self.connection.commit() # not autocommit

            return result

    def delete(self, table, condition=None, limit=0):
        """mysql delete() function"""
        with self.connection.cursor() as cursor:
            if not condition:
                where = '1';
            elif isinstance(condition, dict):
                where = self.join_field_value( condition, ' AND ' )
            else:
                where = condition

            limits = " LIMIT {limit}".format(limit=limit) if limit else ""
            sql = "DELETE FROM {table} WHERE {where}{limits}".format(
                table=table, where=where, limits=limits)

            result = cursor.execute(sql)
            self.connection.commit() # not autocommit

            return result

    def update(self, table, data, condition):
        """mysql update() function"""
        with self.connection.cursor() as cursor:
            params = self.join_field_value(data)
            if not condition:
                where = '1';
            elif isinstance(condition, dict):
                where = self.join_field_value( condition, ' AND ' )
            else:
                where = condition

            sql = "UPDATE {table} SET {params} WHERE {where}".format(
                table=table, params=params, where=where)

            result = cursor.execute(sql)
            self.connection.commit() # not autocommit

            return result

    def fetch_rows(self, table, condition, limit):
        """mysql select() function"""
        with self.connection.cursor() as cursor:
            sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
            cursor.execute(sql, ('webmaster@python.org',))
            result = cursor.fetchone()
            print(result)

    def close(self):
        if self.connection:
            return self.connection.close()

    def join_field_value(self, data, glue = ', '):
        sql = comma = ''
        for key, value in data.iteritems():
            sql +=  "{}`{}` = '{}'".format(comma, key, value)
            comma = glue
        return sql

    def __del__(self):
        """close mysql database connection"""
        self.close()

db = MYSQL('localhost', 'root', '', 'wyproxy', 'utf8')

data = {
    'host' : 'www.qq.com',
    'url' : 'http://www.qq.com',
}

print db.insert('capture', data)
print db.delete('capture', data)

# db.insert('capture', data)
