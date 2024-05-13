import mysql.connector
from dotenv import load_dotenv
import os
load_dotenv()

SQL_DICT = {
    'host': os.getenv('SQL_HOST'),
    'user': os.getenv('SQL_USER'),
    'password': os.getenv('SQL_PASSWORD'),
    'database': os.getenv('SQL_DATABASE')
}

class ConnectSQL():
    def __init__(self, sql_dict=None):
        if sql_dict is None:
            sql_dict = SQL_DICT
        self.__conn = self.connect(sql_dict)

    def connect(self, sql_dict):
        return mysql.connector.connect(
            host=sql_dict['host'],
            user=sql_dict['user'],
            password=sql_dict['password'],
            database=sql_dict['database'],
        )
    
    def get_connection(self):
        return self.__conn
    
    def get_cursor(self):
        return self.__conn.cursor()