import requests, os
from views import JobView
from mappings.mappings import job_mapping_with_type
URL = os.getenv('URL')

class GetJobsByUserRoles:
    def execute(self, user_id, roles, bot):
        data = {
                'user_id': user_id,
                'roles': ['ADMIN', '@everyone', 'Influencer']
            }
        
        response = requests.get(URL + '/job_register/roles', json=data)
        print(response.text)
        
        JSON = response.json()
        jobs = [JobView(job_mapping_with_type(job), bot) for job in JSON]
        return jobs