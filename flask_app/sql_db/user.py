import os
from sql_db.conn import ConnectSQL

class User:
    def __init__(self, cursor=None):
        self.cursor = cursor
        
    def get_by_id(self, id):
        query = """
            SELECT * FROM User WHERE id = %s
        """ 

        self.cursor.execute(query, (id,)) # type: ignore
        return self.cursor.fetchone() # type: ignore
    
    def exists(self, id):
        query = """
            SELECT 1 FROM User WHERE id = %s
        """ 

        self.cursor.execute(query, (id,)) # type: ignore
        return self.cursor.fetchone() # type: ignore

    def create(self, id, total_points=None, points=None, bank_name=None, bank_number=None, register=None) -> bool:
        user = self.get_by_id(id)

        if user:
            return False

        if total_points is None:
            total_points = 1000
        if points is None:
            points = 1000
        # TODO: fill fb id and, Ig id
        query = """
            INSERT INTO User (id, total_points, points, bank_name, bank_number, register)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(query, (id, total_points, points, bank_name, bank_number, register)) # type: ignore

        return True
    
    def update_points(self, id, points):
        update_query = "UPDATE User SET "
        update_params = []

        if points is not None:
            update_query += "points = %s, "
            update_params.append(points)

        update_query = update_query.rstrip(", ") + " WHERE id = %s"
        update_params.append(id)
        self.cursor.execute(update_query, tuple(update_params,)) # type: ignore
        self.cursor.fetchall() # type: ignore
        
        return True
    def update(self, id, total_points=None, points=None, bank_name=None, bank_number=None, register=None):
        update_query = "UPDATE User SET "
        update_params = []

        if total_points is not None:
            update_query += "total_points = %s, "
            update_params.append(total_points)

        if points is not None:
            update_query += "points = %s, "
            update_params.append(points)

        if bank_name is not None:
            update_query += "bank_name = %s, "
            update_params.append(bank_name)

        if bank_number is not None:
            update_query += "bank_number = %s, "
            update_params.append(bank_number)

        if register is not None:
            update_query += "register = %s, "
            update_params.append(register)

        update_query = update_query.rstrip(", ") + " WHERE id = %s"
        update_params.append(id)
        self.cursor.execute(update_query, tuple(update_params)) # type: ignore
        self.cursor.fetchall() # type: ignore
        
        return True
    
    def delete(self, id):
        delete_query = "DELETE FROM User WHERE id = %s"
        self.cursor.execute(delete_query, (id,)) # type: ignore

        result = self.cursor.fetchall() # type: ignore
        return result