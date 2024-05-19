import requests, os
from views import JobView
from mappings.mappings import job_mapping_with_type 
URL = os.getenv('URL')

class GetCompanyJobs:
    def execute(self, id):
        data = {
                'company_id': id,
            }

        response = requests.get(URL + '/job_register/user', json=data)
        JSON = response.json()
        jobs = [JobView(job_mapping_with_type(job)) for job in JSON]
        return jobs