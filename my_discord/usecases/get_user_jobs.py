import requests, os
from views import JobView
from mappings.mappings import job_mapping_with_type 
URL = os.getenv('URL')
class GetUserJobs:
    def execute(self, user_id, bot):
        data = {
                'user_id': user_id,
            }

        response = requests.get(URL + '/job_register/user', json=data)
        JSON = response.json()
        jobs = [JobView(job_mapping_with_type(job), bot) for job in JSON]
        return jobs