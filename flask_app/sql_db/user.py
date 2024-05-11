import os
from sql_db.conn import ConnectSQL

class User:
    def __init__(self, cursor):
        self.cursor = cursor
        
    def get_user_by_id(self, discord_id):
        query = """
            SELECT * FROM User WHERE discord_id = %s LIMIT 1
        """

        self.cursor.execute(query, (discord_id,))
        return self.cursor.fetchone()

    def create(self, discord_id, fb_id=None, ig_id=None, tiktok_id=None, youtube_id=None) -> bool:
        user = self.get_user_by_id(discord_id)

        if user:
            return False

        query = """
            INSERT INTO User (discord_id, fb_id, ig_id, tiktok_id, youtube_id)
            VALUES (%s, %s, %s, %s, %s)
        """
        self.cursor.execute(query, (discord_id, fb_id, ig_id, tiktok_id, youtube_id))

        return True
    
    def edit(self, discord_id, username, fb_id=None, ig_id=None, tiktok_id=None, youtube_id=None):
        update_query = "UPDATE User SET "
        update_params = []

        if fb_id is not None:
            update_query += "username = %s, "
            update_params.append(username)
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

        update_query = update_query.rstrip(", ") + " WHERE discord_id = %s"
        update_params.append(discord_id)
        self.cursor.execute(update_query, tuple(update_params))
        result = self.cursor.fetchall()
        return result
    
    def delete(self, discord_id):
        delete_query = "DELETE FROM User WHERE discord_id = %s"
        self.cursor.execute(delete_query, (discord_id,))

        result = self.cursor.fetchall()
        return result

    def get(self, discord_id):
        select_query = "SELECT * FROM User WHERE discord_id = %s"
        self.cursor.execute(select_query, (discord_id,))
        result = self.cursor.fetchone()
        if result:
            return self(*result)
        else:
            return None
        
if __name__ == '__main__':
    SQL_HOST = 'localhost'
    SQL_USER= 'c0mpl3x'
    SQL_PASSWORD= 'ThePassword123'
    SQL_DATABASE= 'c0mpl3x$discord'

    cursor = ConnectSQL(SQL_HOST, SQL_USER, SQL_PASSWORD, SQL_DATABASE).get_cursor()

    try:
        cursor.execute("SELECT 1")
        print("Cursor is connected.")
    except Exception as e:
        print("Cursor is not connected:", e)
        # raise e

    user = User(cursor)
    temp = user.create('1')