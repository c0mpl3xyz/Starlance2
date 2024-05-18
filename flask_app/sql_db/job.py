import os
from sql_db.conn import ConnectSQL
from datetime import datetime, timedelta
class Job:
    def __init__(self, cursor=None):
        self.cursor = cursor
        self.date_format = '%Y/%m/%d'
        
    def get_by_id(self, id):
        query = """
            SELECT 1 FROM Job WHERE id = %s
        """

        self.cursor.execute(query, (id,)) # type: ignore
        return self.cursor.fetchone() # type: ignore

    def exist_by_id(self, id) -> bool:
        query = """
            SELECT 1 FROM Job WHERE id = %s
        """

        self.cursor.execute(query, (id,)) # type: ignore
        return self.cursor.fetchone() is not None# type: ignore

    def create(self, name, roles, start_date, duration: int, participation_date, description, upload_link, requirements) -> bool:
        # TODO: default values
        # TODO: fill fb id and, Ig id
        start_date = datetime.strptime(start_date, self.date_format)
        end_date = (start_date + timedelta(days=duration)).strftime(self.date_format)
        participation_date = datetime.strptime(participation_date, self.date_format)
        query = """
            INSERT INTO Job (name, roles, start_date, duration, end_date, participation_date, description, upload_link, requirements)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        self.cursor.execute(query, (name, ','.join(roles), start_date, duration, end_date, participation_date, description, upload_link, requirements)) # type: ignore

        return True
    
    def update(self, id, name, roles, start_date, duration: int, participation_date, description, upload_link, requirements) -> bool:
        if not self.exist_by_id(id):
            return False
        
        start_date = datetime.strptime(start_date, self.date_format)
        end_date = (start_date + timedelta(days=duration)).strftime(self.date_format)
        participation_date = datetime.strptime(participation_date, self.date_format)

        update_query = "UPDATE Job SET "
        update_params = []

        if id is not None:
            update_query += "id = %s, "
            update_params.append(id)

        if name is not None:
            update_query += "name = %s, "
            update_params.append(name)

        if roles is not None:
            update_query += "roles = %s, "
            update_params.append(','.join(roles))

        if start_date is not None:
            update_query += "start_date = %s, "
            update_params.append(start_date)
            
        if duration is not None:
            update_query += "duration = %s, "
            update_params.append(duration)

        if end_date is not None:
            update_query += "end_date = %s, "
            update_params.append(end_date)

        if participation_date is not None:
            update_query += "participation_date = %s, "
            update_params.append(participation_date)
        
        if description is not None:
            update_query += "description = %s, "
            update_params.append(description)
        
        if upload_link is not None:
            update_query += "upload_link = %s, "
            update_params.append(upload_link)
        
        if requirements is not None:
            update_query += "requirements = %s, "
            update_params.append(requirements)

        update_query = update_query.rstrip(", ") + " WHERE id = %s"
        update_params.append(id)
        self.cursor.execute(update_query, tuple(update_params)) # type: ignore
        self.cursor.fetchall() # type: ignore
        
        return True
    
    def delete(self, id):
        delete_query = "DELETE FROM Job WHERE id = %s"
        self.cursor.execute(delete_query, (id,)) # type: ignore

        result = self.cursor.fetchall() # type: ignore
        return result