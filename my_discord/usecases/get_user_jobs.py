import requests, os
from views import JobView
URL = os.getenv('URL')
class GetUserJobs:
    def execute(self, user_id):
        data = {
                'user_id': user_id,
            }

        response = requests.get(URL + '/job_register/user', json=data).json()
        print(f'{response=}')
        job_register_ids = [user[0] for user in response]

        for job_reg_id in job_register_ids:
            pass
        return response