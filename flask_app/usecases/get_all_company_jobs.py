from sql_db.conn import ConnectSQL
from sql_db.job import Job

class GetCompanyJobs():
    def execute(self, company_id):
        connection = ConnectSQL().get_connection()
        cursor = connection.cursor()
        job = Job(cursor)
        try:
            jobs = job.get_all_by_company_id(company_id)
        finally:
            connection.close()
        return jobs
    
class GetServerJobs():
    def execute(self):
        connection = ConnectSQL().get_connection()
        cursor = connection.cursor()
        job = Job(cursor)
        try:
            jobs = job.get_all_by_server()
        finally:
            connection.close()
        return jobs