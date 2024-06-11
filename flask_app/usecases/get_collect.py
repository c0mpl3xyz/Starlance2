from sql_db.conn import ConnectSQL
from sql_db.collect import Collect

class GetCollectByUser:
    def execute(self, user_id):
        connection = ConnectSQL().get_connection()
        cursor = connection.cursor()
        collect = Collect(cursor)

        data = collect.get_by_user_id(user_id)
        return data
    
class GetCollectById:
    def execute(self, collect_id):
        connection = ConnectSQL().get_connection()
        cursor = connection.cursor()
        collect = Collect(cursor)

        data = collect.get_by_id(collect_id)
        return data
    
class GetAllCollectPending:
    def execute(self):
        connection = ConnectSQL().get_connection()
        cursor = connection.cursor()
        collect = Collect(cursor)

        data = collect.get_all_pending()
        return data