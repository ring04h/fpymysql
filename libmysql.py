# encoding: utf-8

"""
author: ringzero@0x557.org
home:   http://github.com/ring04h/fpymysql
desc:   A Friendly pymysql CURD Class

https://dev.mysql.com/doc/connector-python/en/connector-python-reference.html

SQL Injection Warning: pymysql.escape_string(value)

"""

from pymysql import (connect, cursors, err, escape_sequence)


def connect_db(mysqldb_conn):
    # msyql dababase connection info
    dbconn = MYSQL(
        dbhost=mysqldb_conn.get('host'),
        dbport=mysqldb_conn.get('port'),
        dbuser=mysqldb_conn.get('user'),
        dbpwd=mysqldb_conn.get('password'),
        dbname=mysqldb_conn.get('db'),
        dbcharset=mysqldb_conn.get('charset'))
    return dbconn


class MYSQL:
    """A Friendly pymysql Class, Provide CRUD functionality"""

    def __init__(self, dbhost, dbuser, dbpwd, dbname, dbcharset='utf-8', dbport=3306):
        self.dbhost = dbhost
        self.dbport = int(dbport)
        self.dbuser = dbuser
        self.dbpwd = dbpwd
        self.dbname = dbname
        self.dbcharset = dbcharset
        self.connection = self.session()

    def session(self):
        """Connect to the database return dbsession"""
        connection = connect(
            host=self.dbhost,
            port=self.dbport,
            user=self.dbuser,
            password=self.dbpwd,
            db=self.dbname,
            charset=self.dbcharset,
            cursorclass=cursors.DictCursor)
        return connection

    def insert(self, table, data):
        """mysql insert() function"""

        with self.connection.cursor() as cursor:

            params = self.join_field_value(data)

            sql = "INSERT IGNORE INTO {table} SET {params}".format(
                table=table, params=params)

            cursor.execute(sql, tuple(data.values()))
            last_id = self.connection.insert_id()

            self.connection.commit()
            return last_id

    def bulk_insert(self, table, data):

        assert isinstance(data, list) and data != [], "data format is error"

        with self.connection.cursor() as cursor:

            params = []
            for param in data:
                params.append(escape_sequence(param.values(), 'utf-8'))

            values = ', '.join(params)
            fields = ', '.join('`{}`'.format(x) for x in param.keys())

            sql = u"INSERT IGNORE INTO {table} ({fields}) VALUES {values}".format(
                fields=fields, table=table, values=values)

            cursor.execute(sql)
            last_id = self.connection.insert_id()

            self.connection.commit()
            return last_id

    def delete(self, table, condition=None, limit=None):
        """
        mysql delete() function
        sql.PreparedStatement method
        """
        with self.connection.cursor() as cursor:

            prepared = []

            if not condition:
                where = '1'
            elif isinstance(condition, dict):
                where = self.join_field_value(condition, ' AND ')
                prepared.extend(condition.values())
            else:
                where = condition

            limits = "LIMIT {limit}".format(limit=limit) if limit else ""

            sql = "DELETE FROM {table} WHERE {where} {limits}".format(
                table=table, where=where, limits=limits)

            if not prepared:
                result = cursor.execute(sql)
            else:
                result = cursor.execute(sql, tuple(prepared))

            self.connection.commit()
            return result

    def update(self, table, data, condition=None):
        """
        mysql update() function
        Use sql.PreparedStatement method
        """
        with self.connection.cursor() as cursor:

            prepared = []
            params = self.join_field_value(data)
            prepared.extend(data.values())

            if not condition:
                where = '1'
            elif isinstance(condition, dict):
                where = self.join_field_value(condition, ' AND ')
                prepared.extend(condition.values())
            else:
                where = condition

            sql = "UPDATE IGNORE {table} SET {params} WHERE {where}".format(
                table=table, params=params, where=where)

            # check PreparedStatement
            if not prepared:
                result = cursor.execute(sql)
            else:
                result = cursor.execute(sql, tuple(prepared))

            self.connection.commit()
            return result

    def count(self, table, condition=None):
        """
        count database record
        Use sql.PreparedStatement method
        """
        with self.connection.cursor() as cursor:

            prepared = []

            if not condition:
                where = '1'
            elif isinstance(condition, dict):
                where = self.join_field_value(condition, ' AND ')
                prepared.extend(condition.values())
            else:
                where = condition

            sql = "SELECT COUNT(*) as cnt FROM {table} WHERE {where}".format(
                table=table, where=where)

            if not prepared:
                cursor.execute(sql)
            else:
                cursor.execute(sql, tuple(prepared))

            self.connection.commit()
            return cursor.fetchone().get('cnt')

    def fetch_rows(self, table, fields=None, condition=None, order=None, limit=None, fetchone=False):
        """
        mysql select() function
        Use sql.PreparedStatement method
        """
        with self.connection.cursor() as cursor:

            prepared = []

            if not fields:
                fields = '*'
            elif isinstance(fields, tuple) or isinstance(fields, list):
                fields = '`{0}`'.format('`, `'.join(fields))
            else:
                fields = fields

            if not condition:
                where = '1'
            elif isinstance(condition, dict):
                where = self.join_field_value(condition, ' AND ')
                prepared.extend(condition.values())
            else:
                where = condition

            if not order:
                orderby = ''
            else:
                orderby = 'ORDER BY {order}'.format(order=order)

            limits = "LIMIT {limit}".format(limit=limit) if limit else ""

            sql = "SELECT {fields} FROM {table} WHERE {where} {orderby} {limits}".format(
                fields=fields, table=table, where=where, orderby=orderby, limits=limits)

            if not prepared:
                cursor.execute(sql)
            else:
                cursor.execute(sql, tuple(prepared))

            self.connection.commit()
            return cursor.fetchone() if fetchone else cursor.fetchall()

    def query(self, sql, fetchone=False, execute=False):
        """execute custom sql query"""
        with self.connection.cursor() as cursor:

            cursor.execute(sql)
            self.connection.commit()

            if execute:
                return

            return cursor.fetchone() if fetchone else cursor.fetchall()

    def join_field_value(self, data, glue=', '):
        sql = comma = ''
        for key in data.keys():
            sql += "{}`{}` = %s".format(comma, key)
            comma = glue
        return sql

    def close(self):
        if getattr(self, 'connection', 0):
            return self.connection.close()

    def __del__(self):
        """close mysql database connection"""
        self.close()
