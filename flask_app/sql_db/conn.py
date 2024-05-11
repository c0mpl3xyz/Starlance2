import mysql.connector

class ConnectSQL():
    def __init__(self, host, user, password, database):
        self.__conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
        )

    def get_connection(self):
        return self.__conn
    
    def get_cursor(self):
        return self.__conn.cursor()