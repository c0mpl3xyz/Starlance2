import requests, os
from views import JobView
from mappings.mappings import job_mapping, content_mappings
URL = os.getenv('URL')

class GetCompanyJobs:
    def execute(self, id, bot, our_company):
        data = {
                'company_id': id,
            }

        response = requests.get(URL + '/job/company', json=data)
        JSON = response.json()
        
        job_views = []
        for job in JSON:
            response = requests.get(URL + '/content/job', json={'job_id': str(job[0])})
            contents = [content_mappings(content) for content in response.json()]
            view = JobView(job_mapping(job), bot,  company=True, has_review=False, contents=contents, our_company=our_company)
            job_views.append(view)
        return job_views