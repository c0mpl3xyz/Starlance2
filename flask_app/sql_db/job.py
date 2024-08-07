import os
from sql_db.conn import ConnectSQL
from datetime import datetime, timedelta
import pytz

class Job:
    def __init__(self, cursor=None):
        self.cursor = cursor
        self.date_format = '%Y/%m/%d'
        self.timezone = pytz.timezone('Asia/Ulaanbaatar')
        date = datetime.now(self.timezone)
        self.current = f'{date.year, date.month, date.day}'

    def get_by_id(self, id):
        query = """
            SELECT * FROM Job WHERE id = %s
        """

        self.cursor.execute(query, (id,)) # type: ignore
        return self.cursor.fetchone() # type: ignore
    
    def get_all_by_server(self):
        query = """
            SELECT * FROM Job
        """

        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def get_all_by_user_id(self, user_id):
        query = """
            SELECT * FROM Job WHERE user_id = %s
        """

        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchall()

    def get_all_by_company_id(self, discord_server_id):
        query = """
            SELECT * FROM Job WHERE discord_server_id = %s AND start_date >= %s
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
        #j.start_date <= %s AND
        query = """
                SELECT j.*
                FROM Job j WHERE 
                (
                    LOWER(j.roles) LIKE LOWER(%s) 
                    OR LOWER(j.roles) LIKE LOWER(%s) 
                    OR LOWER(j.roles) LIKE LOWER(%s) 
                    OR LOWER(j.roles) = LOWER(%s)
                )
                AND j.type = 'Open'
                AND NOT EXISTS (
                    SELECT 1
                    FROM JobRegister jr
                    WHERE jr.job_id = j.id
                    AND jr.user_id = %s
                );
        """
        for role in roles:
            self.cursor.execute(query, (f'%{role},%', f'%,{role},%', f'%,{role}', role, user_id))
            # Fetch all rows from the result set
            rows = self.cursor.fetchall()
            data += rows  # Append fetched rows to data list

        return data

    def exist_by_id(self, id) -> bool:
        query = """
            SELECT 1 FROM Job WHERE id = %s
        """

        self.cursor.execute(query, (id,)) # type: ignore
        return self.cursor.fetchone() is not None# type: ignore

    def create(self, data: dict) -> bool:
        company_id = data['discord_id']
        name = data['name'] 
        server_name = data['server_name'] 
        roles = data['roles'] 
        budget = data['budget'] 
        start_date = data['start_date'] 
        end_date = data['end_date'] 
        duration = data['duration'] 
        participation_date = data['participation_date'] 
        description = data['description'] 
        upload_link = data['upload_link'] 
        requirements = data['requirements'] 
        job_type = data['job_type'] 
        user_count = data['user_count']
        point = data['point']
        
        start_date = datetime.strptime(start_date, self.date_format)
        end_date = datetime.strptime(end_date, self.date_format)
        participation_date = datetime.strptime(participation_date, self.date_format)
        
        query = """
            INSERT INTO Job (discord_server_id, server_name, name, roles, budget, start_date, end_date, duration, participation_date, description, upload_link, requirements, type, user_count, point)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        self.cursor.execute(query, (company_id, server_name, name, roles, budget, start_date, end_date, duration, participation_date, description, upload_link, requirements, job_type, user_count, point)) # type: ignore
        return True
    
    def update_status(self, job_id, job_type) -> bool:
        query = "UPDATE Job SET type = %s WHERE id = %s"
        self.cursor.execute(query, (job_type, job_id)) # type: ignore
        
        return True
    
    def update(self, job_id, data) -> bool:
        if not self.exist_by_id(id):
            return False
        start_date = None
        end_date = None
        participation_date = None

        if 'start_date' in data:
            start_date = datetime.strptime(data['start_date'], self.date_format)
            end_date = datetime.strptime(data['end_date'], self.date_format)
            participation_date = datetime.strptime(data['participation_date'], self.date_format)

        update_query = "UPDATE Job SET "
        update_params = []

        if 'company_id' in data:
            update_query += "discord_server_id = %s, "
            update_params.append(data['company_id'])

        if 'name' in data:
            update_query += "name = %s, "
            update_params.append(data['name'])

        if 'roles' in data:
            update_query += "roles = %s, "
            update_params.append(','.join(data['roles']))

        if 'budget' in data:
            update_query += "budget = %s, "
            update_params.append(data['budget'])
            
        if 'duration' in data:
            update_query += "duration = %s, "
            update_params.append(data['duration'])

        if start_date is not None:
            update_query += "start_date = %s, "
            update_params.append(start_date)

        if end_date is not None:
            update_query += "end_date = %s, "
            update_params.append(end_date)

        if participation_date is not None:
            update_query += "participation_date = %s, "
            update_params.append(participation_date)
        
        if 'description' in data:
            update_query += "description = %s, "
            update_params.append(data['description'])
        
        if 'upload_link' in data:
            update_query += "upload_link = %s, "
            update_params.append(data['upload_link'])
        
        if 'requirements' in data:
            update_query += "requirements = %s, "
            update_params.append(data['requirements'])
        
        if 'job_type' in data:
            update_query += "type = %s, "
            update_params.append(data['job_type'])

        if 'user_count' in data:
            update_query += "user_count = %s, "
            update_params.append(data['user_count'])
        
        if 'point' in data:
            update_query += "point = %s, "
            update_params.append(data['point'])

        update_query = update_query.rstrip(", ") + " WHERE id = %s"
        update_params.append(job_id)
        self.cursor.execute(update_query, tuple(update_params)) # type: ignore
        self.cursor.fetchall() # type: ignore
        
        return True
    
    def delete(self, job_id):
        try:
            # Identify all tables and columns referencing the Job table
            tables_referencing_job = [
                {"table": "Content", "column": "job_id"},
                {"table": "Review", "column": "job_id"},
                {"table": "JobRegister", "column": "job_id"}
            ]

            # Delete all references from the referencing tables
            for ref in tables_referencing_job:
                delete_reference_query = f"DELETE FROM {ref['table']} WHERE {ref['column']} = %s"
                self.cursor.execute(delete_reference_query, (job_id,))  # type: ignore

            # Delete the job itself
            delete_job_query = "DELETE FROM Job WHERE id = %s"
            self.cursor.execute(delete_job_query, (job_id,))  # type: ignore

            # Return success message or result as needed
            return True
        
        except Exception as e:
            print(str(e))
            return False
    
    def delete_by_user_id(self, user_id):
        delete_query = "DELETE FROM Job WHERE user_id = %s"
        self.cursor.execute(delete_query, (user_id,)) # type: ignore

        result = self.cursor.fetchall() # type: ignore
        return result
    
    def get_all_open_job(self):
        today = datetime.now(self.timezone)
        start_date = datetime(today.year, today.month, today.day)
        query = "SELECT * FROM Job WHERE type = 'OPEN' and start_date <= %s"
        self.cursor.execute(query, (start_date,)) # type: ignore
        result = self.cursor.fetchall() # type: ignore
        return result