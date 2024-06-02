from sql_db.conn import ConnectSQL
from sql_db.review import Review

class GetReviewByJob:
    def execute(self, job_id):
        connection = ConnectSQL().get_connection()
        cursor = connection.cursor()

        review = Review(cursor)
        reviews = review.get_by_job_id(job_id)
        return reviews
    
class GetReviewByUser:
    def execute(self, user_id):
        connection = ConnectSQL().get_connection()
        cursor = connection.cursor()

        review = Review(cursor)
        reviews = review.get_by_user_id(user_id)
        return reviews
    
class GetReviewByJobRegister:
    def execute(self, job_register_id):
        connection = ConnectSQL().get_connection()
        cursor = connection.cursor()

        review = Review(cursor)
        reviews = review.get_by_job_register_id(job_register_id)
        return reviews
    
class GetReviewByJobRegisterAndUser:
    def execute(self, job_register_id, user_id):
        connection = ConnectSQL().get_connection()
        cursor = connection.cursor()

        review = Review(cursor)
        reviews = review.get_by_job_register_id_and_user_id(job_register_id, user_id)
        return reviews
    
class GetReviewByCompany:
    def execute(self, server_id):
        connection = ConnectSQL().get_connection()
        cursor = connection.cursor()

        review = Review(cursor)
        reviews = review.get_by_server_id(server_id)
        return reviews