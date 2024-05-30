class Review:
    def __init__(self, cursor=None):
        self.cursor = cursor
        self.date_format = '%Y/%m/%d'
    
    def get_by_id(self, id):
        query = """
            SELECT * FROM Content WHERE id = %s
        """

        self.cursor.execute(query, (id,)) # type: ignore
        return self.cursor.fetchall() # type: ignore
    
    def get_by_job_id(self, job_id):
        query = """
            SELECT * FROM Content WHERE job_id = %s
        """

        self.cursor.execute(query, (job_id,)) # type: ignore
        return self.cursor.fetchall() # type: ignore
    
    def get_by_user_id(self, user_id):
        query = """
            SELECT * FROM Content WHERE user_id = %s
        """

        self.cursor.execute(query, (user_id,)) # type: ignore
        return self.cursor.fetchall() # type: ignore
    
    def get_by_job_register_id(self, job_register_id):
        query = """
            SELECT * FROM Content WHERE job_register_id = %s
        """

        self.cursor.execute(query, (job_register_id)) # type: ignore
        return self.cursor.fetchall() # type: ignore

    def create(self, job_register_id, job_id, user_id, link, review_type) -> bool:
        query = """
            INSERT INTO Content (job_register_id, job_id, user_id, link, type)
            VALUES (%s, %s, %s, %s, %s)
        """

        self.cursor.execute(query, (job_register_id, job_id, user_id, link, review_type)) # type: ignore
        return True
    
    def update(self, id, job_register_id, job_id, user_id, link, review_type) -> bool:
        update_query = "UPDATE Content SET "
        update_params = []

        if job_register_id is not None:
            update_query += "job_register_id = %s, "
            update_params.append(job_register_id)
        
        if job_id is not None:
            update_query += "job_id = %s, "
            update_params.append(job_id)
        
        if user_id is not None:
            update_query += "user_id = %s, "
            update_params.append(user_id)

        if link is not None:
            update_query += "link = %s, "
            update_params.append(','.join(link))
        
        if review_type is not None:
            update_query += "review_type = %s, "
            update_params.append(review_type)

        update_query = update_query.rstrip(", ") + " WHERE id = %s"
        update_params.append(id)
        self.cursor.execute(update_query, tuple(update_params)) # type: ignore
        self.cursor.fetchall() # type: ignore

        return True

    def delete_by_job_register_id(self, job_register_id):
        delete_query = "DELETE FROM Content WHERE job_register_id = %s"
        self.cursor.execute(delete_query, (job_register_id)) # type: ignore