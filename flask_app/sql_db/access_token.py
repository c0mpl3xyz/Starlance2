from datetime import datetime, timedelta
import uuid

class AccessToken:
    def __init__(self, cursor):
        self.cursor = cursor

    def add(self, access_token, user_id, duration_sec, token_type, fb_pages: list, ig_accounts: list) -> bool:
        expires_in_timedelta = timedelta(seconds=duration_sec)
        expiration_date = datetime.now() + expires_in_timedelta
        
        fb_pages = ','.join([fb_page for fb_page in fb_pages])
        ig_accounts = ','.join([ig_account for ig_account in ig_accounts])
        
        insert_query = """
            INSERT INTO AccessToken (user_id, token, token_type, expiration_date, active, fb_pages, ig_accounts)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        update_query = """
            UPDATE AccessToken
            SET token = %s, token_type = %s, expiration_date = %s, active = %s, fb_pages = %s, ig_accounts = %s
            WHERE user_id = %s
        """

        select_query = "SELECT * FROM AccessToken WHERE user_id = %s"
        self.cursor.execute(select_query, (user_id,))
        existing_record = self.cursor.fetchone()

        try:
            if existing_record:
                update_values = (access_token, token_type, expiration_date, True, fb_pages, ig_accounts, user_id)
                self.cursor.execute(update_query, update_values)
            else:
                self.cursor.execute(insert_query, (user_id, access_token, token_type, expiration_date, True, fb_pages, ig_accounts))
            return True
        except Exception:
            raise