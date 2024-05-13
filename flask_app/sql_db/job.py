import os
from sql_db.conn import ConnectSQL

class Job:
    def __init__(self, cursor=None):
        self.cursor = cursor
        
    def get_by_id(self, id):
        query = """
            SELECT 1 FROM Job WHERE id = %s
        """

        self.cursor.execute(query, (id,)) # type: ignore
        return self.cursor.fetchone() # type: ignore

    def create(self, id, start_date, duration, end_date, modified_date, participation_date, job_delete_date, description, upload_file_links, requirements) -> bool:
        job = self.get_by_id(id)

        if job:
            return False

        # TODO: fill fb id and, Ig id
        query = """
            INSERT INTO User (id, start_date, duration, end_date, modified_date, participation_date, job_delete_date, description, upload_file_links, requirements)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(query, (id, start_date, duration, end_date, modified_date, participation_date, job_delete_date, description, upload_file_links, requirements)) # type: ignore

        return True
    
    def update(self, id, start_date, duration, end_date, modified_date, participation_date, job_delete_date, description, upload_file_links, requirements) -> bool:
        update_query = "UPDATE User SET "
        update_params = []

        if id is not None:
            update_query += "id = %s, "
            update_params.append(id)

        if start_date is not None:
            update_query += "start_date = %s, "
            update_params.append(start_date)
            
        if duration is not None:
            update_query += "duration = %s, "
            update_params.append(duration)

        if end_date is not None:
            update_query += "end_date = %s, "
            update_params.append(end_date)

        if modified_date is not None:
            update_query += "modified_date = %s, "
            update_params.append(modified_date)

        if participation_date is not None:
            update_query += "participation_date = %s, "
            update_params.append(participation_date)

        if job_delete_date is not None:
            update_query += "job_delete_date = %s, "
            update_params.append(job_delete_date)
        
        if description is not None:
            update_query += "description = %s, "
            update_params.append(description)
        
        if upload_file_links is not None:
            update_query += "upload_file_links = %s, "
            update_params.append(upload_file_links)
        
        if requirements is not None:
            update_query += "requirements = %s, "
            update_params.append(requirements)

        update_query = update_query.rstrip(", ") + " WHERE discord_id = %s"
        update_params.append(id)
        self.cursor.execute(update_query, tuple(update_params)) # type: ignore
        self.cursor.fetchall() # type: ignore
        
        return True
    
    def delete(self, discord_id):
        delete_query = "DELETE FROM User WHERE discord_id = %s"
        self.cursor.execute(delete_query, (discord_id,)) # type: ignore

        result = self.cursor.fetchall() # type: ignore
        return result