import requests, os
from views import JobView
from mappings.mappings import job_mapping_with_type, job_mapping 
URL = os.getenv('URL')

class GetJobsByUserRoles:
    def execute(self, user_id, roles):
        data = {
                'user_id': user_id,
                'roles': roles
            }
        
        response = requests.get(URL + '/job_register/roles', json=data)
        print(f'{response.json()}')
        JSON = response.json()
        jobs = [JobView(job_mapping(job)) for job in JSON]
        return jobs