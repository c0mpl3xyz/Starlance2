from datetime import datetime, timedelta
import uuid

class AccessToken:
    def __init__(self, cursor):
        self.cursor = cursor

    def add(self, access_token, user_id, duration_sec, token_type) -> bool:
        expires_in_timedelta = timedelta(seconds=duration_sec)
        expiration_date = datetime.now() + expires_in_timedelta

        insert_query = """
            INSERT INTO AccessToken (user_id, token, token_type, expiration_date, active)
            VALUES (%s, %s, %s, %s, %s)
        """

        update_query = """
            UPDATE AccessToken
            SET token = %s, token_type = %s, expiration_date = %s, active = %s
            WHERE user_id = %s
        """

        select_query = "SELECT * FROM AccessToken WHERE user_id = %s"
        self.cursor.execute(select_query, (user_id,))
        existing_record = self.cursor.fetchone()

        try:
            if existing_record:
                update_values = (access_token, token_type, expiration_date, True, user_id)
                self.cursor.execute(update_query, update_values)
            else:
                self.cursor.execute(insert_query, (user_id, access_token, token_type, expiration_date, True))
            return True
        except Exception:
            raise
    
    def create(self, user_id) -> bool:
        update_query = """
            INSERT INTO users (user_id) VALUES (%s);
        """

        try:
            self.cursor.execute(update_query, (user_id,))
            return True
        except Exception:
            raise