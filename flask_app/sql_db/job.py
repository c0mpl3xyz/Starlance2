import os
from sql_db.conn import ConnectSQL
from datetime import datetime, timedelta
class Job:
    def __init__(self, cursor=None):
        self.cursor = cursor
        self.date_format = '%Y/%m/%d'
        self.current = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def get_by_id(self, id):
        query = """
            SELECT * FROM Job WHERE id = %s
        """

        self.cursor.execute(query, (id,)) # type: ignore
        return self.cursor.fetchone() # type: ignore
    
    def get_all_by_company_id(self, discord_server_id):
        query = """
            SELECT * FROM Job WHERE discord_server_id = %s AND start_date > %s
        """

        self.cursor.execute(query, (discord_server_id, self.current))
        return self.cursor.fetchall()
    
    def get_by_discord_id(self, discord_id):
        query = """
            SELECT * FROM Job WHERE discord_server_id = %s
        """

        self.cursor.execute(query, (discord_id,)) # type: ignore
        return self.cursor.fetchone() # type: ignore
    
    def get_all_by_roles(self, user_id, roles: list):
        data = []
        for role in roles:
            query = """
                SELECT j.*
                FROM Job j
                WHERE j.start_date > %s
                AND (
                    LOWER(j.roles) LIKE %s 
                    OR LOWER(j.roles) LIKE %s 
                    OR LOWER(j.roles) LIKE %s 
                    OR LOWER(j.roles) = %s
                )
                AND NOT EXISTS (
                    SELECT 1
                    FROM JobRegister jr
                    WHERE jr.job_id = j.id
                    AND jr.user_id = %s
                );
            """
            # Execute the query with parameters
            self.cursor.execute(query, (self.current, f'%{role},%', f'%,{role},%', f'%,{role}', role, user_id))
            data = self.cursor.fetchall()
        return data

    def exist_by_id(self, id) -> bool:
        query = """
            SELECT 1 FROM Job WHERE discord_server_id = %s
        """

        self.cursor.execute(query, (id,)) # type: ignore
        return self.cursor.fetchone() is not None# type: ignore

    def create(self, company_id, name, roles, budget, start_date, end_date, duration: int, participation_date, description, upload_link, requirements) -> bool:
        # TODO: default values
        # TODO: fill fb id and, Ig id
        start_date = datetime.strptime(start_date, self.date_format)
        end_date = datetime.strptime(end_date, self.date_format)
        participation_date = datetime.strptime(participation_date, self.date_format)
        
        query = """
            INSERT INTO Job (discord_server_id, name, roles, budget, start_date, end_date, duration, participation_date, description, upload_link, requirements)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        self.cursor.execute(query, (company_id, name, roles, budget, start_date, end_date, duration, participation_date, description, upload_link, requirements)) # type: ignore

        return True
    
    def update(self, id, name, roles, budget, start_date, end_date, duration: int, participation_date, description, upload_link, requirements) -> bool:
        if not self.exist_by_id(id):
            return False
        
        start_date = datetime.strptime(start_date, self.date_format)
        end_date = datetime.strptime(end_date, self.date_format)
        participation_date = datetime.strptime(participation_date, self.date_format)

        update_query = "UPDATE Job SET "
        update_params = []

        if id is not None:
            update_query += "discord_server_id = %s, "
            update_params.append(id)

        if name is not None:
            update_query += "name = %s, "
            update_params.append(name)

        if roles is not None:
            update_query += "roles = %s, "
            update_params.append(','.join(roles))

        if budget is not None:
            update_query += "budget = %s, "
            update_params.append(budget)

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