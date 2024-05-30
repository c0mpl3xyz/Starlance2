from sql_db.conn import ConnectSQL
from sql_db.content import Content

class GetContentByJob:
    def execute(self, job_id):
        connection = ConnectSQL().get_connection()
        cursor = connection.cursor()

        contents = []
        content = Content(cursor)
        content.get_by_job_id(job_id)
        return contents
    
class GetContentByUser:
    def execute(self, user_id):
        connection = ConnectSQL().get_connection()
        cursor = connection.cursor()

        contents = []
        content = Content(cursor)
        content.get_by_user_id(user_id)
        return contents
    
class GetContentByJobRegister:
    def execute(self, job_register_id):
        connection = ConnectSQL().get_connection()
        cursor = connection.cursor()

        contents = []
        content = Content(cursor)
        content.get_by_job_register_id(job_register_id)
        return contents
    
class GetContentByJobRegisterAndUser:
    def execute(self, job_register_id, user_id):
        connection = ConnectSQL().get_connection()
        cursor = connection.cursor()

        contents = []
        content = Content(cursor)
        content.get_by_job_register_id_and_user_id(job_register_id, user_id)
        return contents