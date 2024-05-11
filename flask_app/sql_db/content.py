class Content:
    def __init__(self, content_id, content_link, code, user_discord_id, start_date, deadline, end_date=None, collected_point=0, last_collected_date=None):
        self.content_id = content_id
        self.content_link = content_link
        self.code = code
        self.user_discord_id = user_discord_id
        self.start_date = start_date
        self.deadline = deadline
        self.end_date = end_date
        self.collected_point = collected_point
        self.last_collected_date = last_collected_date
    
    @classmethod
    def create(cls, cursor, content_id, content_link, code, user_discord_id, start_date, deadline):
        insert_query = """
            INSERT INTO Content (content_id, content_link, code, user_discord_id, start_date, deadline)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (content_id, content_link, code, user_discord_id, start_date, deadline))
    
    @classmethod
    def delete(cls, cursor, content_id):
        delete_query = "DELETE FROM Content WHERE content_id = %s"
        cursor.execute(delete_query, (content_id,))
    
    @classmethod
    def get(cls, cursor, content_id):
        select_query = "SELECT * FROM Content WHERE content_id = %s"
        cursor.execute(select_query, (content_id,))
        result = cursor.fetchone()
        if result:
            return cls(*result)
        else:
            return None