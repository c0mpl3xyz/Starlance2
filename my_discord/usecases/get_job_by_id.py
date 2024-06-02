import requests, os
from mappings.mappings import job_mapping
URL = os.getenv('URL')
class GetJobById():
    def __init__(self, job_id):
        self.data = {
                'job_id': job_id
            }
    
    def execute(self):
        response = requests.get(URL + '/job', json=self.data)
        return job_mapping(response.json())