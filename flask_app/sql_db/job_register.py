import os
from sql_db.conn import ConnectSQL
from datetime import datetime, timedelta
class JobRegister:
    def __init__(self, cursor=None):
        self.cursor = cursor
        self.date_format = '%Y/%m/%d'
        
    def get_by_user_id(self, user_id):
        query = """
            SELECT * FROM JobRegister WHERE user_id = %s
        """

        self.cursor.execute(query, (user_id,)) # type: ignore
        return self.cursor.fetchall() # type: ignore

    def get_by_job_id(self, job_id):
        query = """
            SELECT * FROM JobRegister WHERE job_id = %s
        """

        self.cursor.execute(query, (job_id,)) # type: ignore
        return self.cursor.fetchall() # type: ignore

    def exist_by_id(self, user_id, job_id) -> bool:
        query = """
            SELECT 1 FROM JobRegister WHERE user_id = %s AND job_id = %s
        """

        self.cursor.execute(query, (user_id, job_id)) # type: ignore
        return self.cursor.fetchone() is not None# type: ignore

    def create(self, user_id, job_id, job_type=None) -> bool:
        if self.exist_by_id(user_id, job_id):
            return False
        
        query = """
            INSERT INTO JobRegister (user_id, job_id, type)
            VALUES (%s, %s, %s)
        """

        self.cursor.execute(query, (user_id, job_id, job_type)) # type: ignore
        return True
    
    def update(self, user_id, job_id, job_type=None) -> bool:
        if not self.exist_by_id(user_id, job_id):
            return False
        
        start_date = datetime.strptime(start_date, self.date_format)
        end_date = datetime.strptime(end_date, self.date_format)
        participation_date = datetime.strptime(participation_date, self.date_format)

        update_query = "UPDATE JobRegister SET "
        update_params = []

        if user_id is not None:
            update_query += "user_id = %s, "
            update_params.append(user_id)

        if job_id is not None:
            update_query += "job_id = %s, "
            update_params.append(job_id)

        if job_type is not None:
            update_query += "job_type = %s, "
            update_params.append(','.join(job_type))

        update_query = update_query.rstrip(", ") + " WHERE id = %s"
        update_params.append(id)
        self.cursor.execute(update_query, tuple(update_params)) # type: ignore
        self.cursor.fetchall() # type: ignore
        
        return True
    
    def delete(self, user_id, job_id):
        delete_query = "DELETE FROM JobRegister WHERE user_id = %s AND job_id = %s"
        self.cursor.execute(delete_query, (user_id, job_id)) # type: ignore