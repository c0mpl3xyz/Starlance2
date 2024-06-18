from datetime import datetime, timedelta
import uuid

class AccessToken:
    def __init__(self, cursor):
        self.cursor = cursor

    def add(self, access_token, server_id, duration_sec, token_type) -> bool:
        expires_in_timedelta = timedelta(seconds=duration_sec)
        expiration_date = datetime.now() + expires_in_timedelta

        insert_query = """
            INSERT INTO AccessToken (server_id, token, token_type, expiration_date, active)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        update_query = """
            UPDATE AccessToken
            SET token = %s, token_type = %s, expiration_date = %s, active = %s
            WHERE user_id = %s
        """

        select_query = "SELECT * FROM AccessToken WHERE server_id = %s"
        self.cursor.execute(select_query, (server_id,))
        existing_record = self.cursor.fetchone()

        try:
            if existing_record:
                update_values = (access_token, token_type, expiration_date, True, server_id)
                self.cursor.execute(update_query, update_values)
            else:
                self.cursor.execute(insert_query, (server_id, access_token, token_type, expiration_date, True))
            return True
        except Exception:
            return False