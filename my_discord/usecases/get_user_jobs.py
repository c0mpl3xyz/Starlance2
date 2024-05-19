import requests, os
from views import JobView
from mappings.mappings import job_mapping 
URL = os.getenv('URL')
class GetUserJobs:
    def execute(self, user_id):
        data = {
                'user_id': user_id,
            }

        response = requests.get(URL + '/job_register/user', json=data)
        JSON = response.json()
        print(f'{JSON}')

        jobs = [JobView(job_mapping(job)) for job in JSON]

        print(f'{JSON=}')
        return jobs