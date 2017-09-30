# encoding: utf-8

"""
author: ringzero@0x557.org
home:   http://github.com/ring04h/fpymysql
desc:   A Friendly pymysql CURD Class

https://dev.mysql.com/doc/connector-python/en/connector-python-reference.html

SQL Injection Warning: pymysql.escape_string(value)

"""

from pymysql import (connect, cursors, escape_string, err)


class MYSQL:
    """A Friendly pymysql Class, Provide CRUD functionality"""

    def __init__(self, dbhost, dbuser, dbpwd, dbname, dbcharset, dbport=3306):
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

            sql = "INSERT IGNORE INTO {table} SET {params}".\
                format(table=table, params=params)

            cursor.execute(sql, tuple(data.values()))
            last_id = self.connection.insert_id()

            self.connection.commit()
            return last_id

    def bulk_insert(self, table, data):
        """mysql bulk_insert() function"""

        assert isinstance(data, list)
        with self.connection.cursor() as cursor:

            params = [str(tuple(escape_string(str(x))
                                for x in param.values())) for param in data]

            values = ', '.join(params)
            fields = ', '.join('`{}`'.format(x) for x in param.keys())

            sql = "INSERT IGNORE INTO {table} ({fields}) VALUES {values}".format(
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

            # check PreparedStatement
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

            # WHERE CONDITION
            if not condition:
                where = '1'
            elif isinstance(condition, dict):
                where = self.join_field_value(condition, ' AND ')
                prepared.extend(condition.values())
            else:
                where = condition

            # SELECT COUNT(*) as cnt
            sql = "SELECT COUNT(*) as cnt FROM {table} WHERE {where}".format(
                table=table, where=where)

            # check PreparedStatement, EXECUTE SELECT COUNT sql
            if not prepared:
                cursor.execute(sql)
            else:
                cursor.execute(sql, tuple(prepared))

            # RETURN cnt RESULT
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

            # WHERE CONDITION
            if not condition:
                where = '1'
            elif isinstance(condition, dict):
                where = self.join_field_value(condition, ' AND ')
                prepared.extend(condition.values())
            else:
                where = condition

            # ORDER BY OPTIONS
            if not order:
                orderby = ''
            else:
                orderby = 'ORDER BY {order}'.format(order=order)

            # LIMIT NUMS
            limits = "LIMIT {limit}".format(limit=limit) if limit else ""

            sql = "SELECT {fields} FROM {table} WHERE {where} {orderby} {limits}".format(
                fields=fields, table=table, where=where, orderby=orderby, limits=limits)

            # check PreparedStatement
            if not prepared:
                cursor.execute(sql)
            else:
                cursor.execute(sql, tuple(prepared))

            return cursor.fetchone() if fetchone else cursor.fetchall()

    def query(self, sql, fetchone=False, execute=False):
        """execute custom sql query"""
        with self.connection.cursor() as cursor:

            cursor.execute(sql)
            self.connection.commit()  # not auto commit

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
        if self.connection:
            return self.connection.close()

    def __del__(self):
        """close mysql database connection"""
        self.close()
