import requests, os
from views import JobView
from mappings.mappings import job_mapping
URL = os.getenv('URL')

class GetCompanyJobs:
    def execute(self, id):
        data = {
                'company_id': id,
            }

        response = requests.get(URL + '/job/company', json=data)
        JSON = response.json()
        jobs = [JobView(job_mapping(job), company=True) for job in JSON]
        return jobs