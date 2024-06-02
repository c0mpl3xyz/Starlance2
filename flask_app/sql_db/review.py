class Review:
    def __init__(self, cursor=None):
        self.cursor = cursor
        self.date_format = '%Y/%m/%d'
    
    def get_by_id(self, id):
        query = """
            SELECT * FROM Review WHERE id = %s
        """

        self.cursor.execute(query, (id,)) # type: ignore
        return self.cursor.fetchall() # type: ignore
    
    def get_by_job_id(self, job_id):
        query = """
            SELECT * FROM Review WHERE job_id = %s
        """

        self.cursor.execute(query, (job_id,)) # type: ignore
        return self.cursor.fetchall() # type: ignore
    
    def get_by_user_id(self, user_id):
        query = """
            SELECT * FROM Review WHERE user_id = %s
        """

        self.cursor.execute(query, (user_id,)) # type: ignore
        return self.cursor.fetchall() # type: ignore
    
    def get_by_job_register_id(self, job_register_id):
        query = """
            SELECT * FROM Review WHERE job_register_id = %s
        """

        self.cursor.execute(query, (job_register_id)) # type: ignore
        return self.cursor.fetchall() # type: ignore
    
    def get_by_job_register_id(self, job_register_id, user_id):
        query = """
            SELECT * FROM Review WHERE job_register_id = %s and user_id = %s
        """

        self.cursor.execute(query, (job_register_id, user_id)) # type: ignore
        return self.cursor.fetchall() # type: ignore
    
    def get_by_server_id(self, server_id):
        query = """
            SELECT * FROM Review WHERE server_id %s
        """

        self.cursor.execute(query, (server_id)) # type: ignore
        return self.cursor.fetchall() # type: ignore

    def create(self, job_register_id, job_id, job_name, job_description, user_id,  server_id, server_name, link, review_type, description) -> bool:
        query = """
            INSERT INTO Review (job_register_id, job_id, job_name, job_description, user_id, server_id, server_name, link, type, description)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        self.cursor.execute(query, (job_register_id, job_id, job_name, job_description, user_id, server_id, server_name, link, review_type, description)) # type: ignore
        return True
    
    def update(self, id, job_register_id, job_id, job_name, job_description, user_id, link, review_type, description) -> bool:
        update_query = "UPDATE Review SET "
        update_params = []

        if job_register_id is not None:
            update_query += "job_register_id = %s, "
            update_params.append(job_register_id)
        
        if job_id is not None:
            update_query += "job_id = %s, "
            update_params.append(job_id)

        if job_name is not None:
            update_query += "job_name = %s, "
            update_params.append(job_name)

        if job_description is not None:
            update_query += "job_description = %s, "
            update_params.append(job_description)
        
        if user_id is not None:
            update_query += "user_id = %s, "
            update_params.append(user_id)

        if link is not None:
            update_query += "link = %s, "
            update_params.append(','.join(link))
        
        if review_type is not None:
            update_query += "type = %s, "
            update_params.append(review_type)
        
        if description is not None:
            update_query += "description = %s, "
            update_params.append(description)

        update_query = update_query.rstrip(", ") + " WHERE id = %s"
        update_params.append(id)
        self.cursor.execute(update_query, tuple(update_params)) # type: ignore
        self.cursor.fetchall() # type: ignore

        return True

    def delete_by_job_register_id(self, job_register_id):
        delete_query = "DELETE FROM Review WHERE job_register_id = %s"
        self.cursor.execute(delete_query, (job_register_id)) # type: ignore