import requests, os
from views import JobView
from mappings.mappings import job_mapping, content_mappings
URL = os.getenv('URL')

class GetCompanyJobs:
    def execute(self, id, bot):
        data = {
                'company_id': id,
            }

        response = requests.get(URL + '/job/company', json=data)
        JSON = response.json()
        
        job_views = []
        for job in JSON:
            response = requests.get(URL + '/content/job', json={'job_id': str(job[0])})
            contents = [content_mappings(content) for content in response.json()]
            view = JobView(job_mapping(job), bot,  company=True, has_review=False, contents=contents)
            job_views.append(view)
        return job_views
    
class GetServerJobs:
    def execute(self, bot):
        response = requests.get(URL + '/job/server')
        JSON = response.json()
        
        job_views = []
        for job in JSON:
            response = requests.get(URL + '/content/job', json={'job_id': str(job[0])})
            contents = [content_mappings(content) for content in response.json()]
            view = JobView(job_mapping(job), bot,  company=True, has_review=False, contents=contents, server=True)
            job_views.append(view)
        return job_views