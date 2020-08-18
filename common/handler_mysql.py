# author:CC
# email:yangdeyi1201@foxmail.com

import pymysql
from pymysql.cursors import DictCursor


class MysqlHandler(object):
    def __init__(self):
        self.conn = pymysql.connect(host='120.78.128.25', port=3306, database='futureloan', user='future', password='123456', charset='utf8', cursorclass=DictCursor)
        self.cursor = self.conn.cursor()

    def query(self, sql, one=True):
        self.cursor.execute(query=sql)
        self.conn.commit()

        if one:
            return self.cursor.fetchone()
        else:
            return self.cursor.fetchall()


if __name__ == '__main__':
    pass
