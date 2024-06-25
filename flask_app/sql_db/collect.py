class Collect():
    def __init__(self, cursor=None):
        self.cursor = cursor

    def get_by_id(self, collect_id):
        query = """
            SELECT * FROM CollectRequest WHERE id = %s
        """

        self.cursor.execute(query, (collect_id,)) # type: ignore
        return self.cursor.fetchall() # type: ignore

    def get_by_user_id(self, user_id):
        query = """
            SELECT * FROM CollectRequest WHERE user_id = %s and type = 'Pending'
        """

        self.cursor.execute(query, (user_id,)) # type: ignore
        return self.cursor.fetchall() # type: ignore

    def delete(self, user_id):
        query = """
            DELETE from CollectRequest WHERE id = %s
        """

        self.cursor.execute(query, (user_id,)) # type: ignore
        return self.cursor.fetchall() # type: ignore

    def get_all_pending(self):
        query = """
            SELECT * FROM CollectRequest WHERE type = 'Pending'
        """

        self.cursor.execute(query) # type: ignore
        return self.cursor.fetchall() # type: ignore

    def create(self, user_id, points) -> bool:
        collect_type = 'Pending'
        if len(self.get_by_user_id(user_id)):
            return False
        
        query = """
            INSERT INTO CollectRequest (user_id, points, type)
            VALUES (%s, %s, %s)
        """
        self.cursor.execute(query, (user_id, points, collect_type)) # type: ignore
        return True

    def update(self, collect_id, user_id=None, points=None, collect_type=None):
        update_query = "UPDATE CollectRequest SET "
        update_params = []
        
        if user_id is not None:
            update_query += "user_id = %s, "
            update_params.append(user_id)

        if points is not None:
            update_query += "points = %s, "
            update_params.append(points)

        if collect_type is not None:
            update_query += "type = %s, "
            update_params.append(collect_type)

        update_query = update_query.rstrip(", ") + " WHERE id = %s"
        update_params.append(collect_id)
        self.cursor.execute(update_query, tuple(update_params)) # type: ignore
        self.cursor.fetchall() # type: ignore
        
        return True
    