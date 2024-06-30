import requests, os
from mappings.mappings import job_mapping
import aiohttp, uuid, aiofiles

URL = os.getenv('URL')

class GetJobById():
    def __init__(self, job_id):
        self.data = {
                'job_id': job_id
            }
    
    def execute(self):
        response = requests.get(URL + '/job', json=self.data)
        return job_mapping(response.json())
    
class GetJobReportById():
    async def execute(self, job_id):
        data = {'job_id': job_id}
        content = None

        async with aiohttp.ClientSession() as session:
            async with session.get(URL + '/job/report', json=data) as response:
                if response.status == 200:
                    content = await response.read()
        return content