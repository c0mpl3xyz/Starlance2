import os
from sql_db.conn import ConnectSQL

class User:
    def __init__(self, cursor=None):
        self.cursor = cursor
        
    def get_user_by_id(self, discord_id):
        query = """
            SELECT 1 FROM User WHERE discord_id = %s
        """

        self.cursor.execute(query, (discord_id,))
        return self.cursor.fetchone()

    def create(self, discord_id, fb_id=None, ig_id=None, tiktok_id=None, youtube_id=None, bank_name=None, bank_number=None, register=None) -> bool:
        user = self.get_user_by_id(discord_id)

        if user:
            return False

        # TODO: fill fb id and, Ig id
        query = """
            INSERT INTO User (discord_id, fb_id, ig_id, tiktok_id, youtube_id, bank_name, bank_number, register)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(query, (discord_id, fb_id, ig_id, tiktok_id, youtube_id, bank_name, bank_number, register))

        return True
    
    def update(self, discord_id, fb_id=None, ig_id=None, tiktok_id=None, youtube_id=None, bank_name=None, bank_number=None, register=None):
        update_query = "UPDATE User SET "
        update_params = []

        if fb_id is not None:
            update_query += "fb_id = %s, "
            update_params.append(fb_id)

        if ig_id is not None:
            update_query += "ig_id = %s, "
            update_params.append(ig_id)
            
        if tiktok_id is not None:
            update_query += "tiktok_id = %s, "
            update_params.append(tiktok_id)

        if youtube_id is not None:
            update_query += "youtube_id = %s, "
            update_params.append(youtube_id)

        if bank_name is not None:
            update_query += "bank_name = %s, "
            update_params.append(bank_name)

        if bank_number is not None:
            update_query += "bank_number = %s, "
            update_params.append(bank_number)

        if register is not None:
            update_query += "register = %s, "
            update_params.append(register)

        update_query = update_query.rstrip(", ") + " WHERE discord_id = %s"
        update_params.append(discord_id)
        self.cursor.execute(update_query, tuple(update_params))
        result = self.cursor.fetchall()
        
        return True
    
    def delete(self, discord_id):
        delete_query = "DELETE FROM User WHERE discord_id = %s"
        self.cursor.execute(delete_query, (discord_id,))

        result = self.cursor.fetchall()
        return result

    def get(self, discord_id):
        select_query = "SELECT 1 FROM User WHERE discord_id = %s"
        self.cursor.execute(select_query, (discord_id,))
        result = self.cursor.fetchone()
        if result:
            return self(*result)
        else:
            return None