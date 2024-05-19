from sql_db.conn import ConnectSQL
from sql_db.job_register import JobRegister
from sql_db.job import Job
from sql_db.user import User

class GetAllJobsByUser:
    def execute(self, user_id):
        connection = ConnectSQL().get_connection()
        cursor = connection.cursor()
        job_register = JobRegister(cursor)
        registered_jobs = [(j[1], j[2]) for j in job_register.get_by_user_id(user_id)]

        jobs = []
        for job_id, type in registered_jobs:
            job = Job(cursor).get_by_id(job_id)
            job.append(type)
            if job is not None:
                jobs.append(job)
        return jobs