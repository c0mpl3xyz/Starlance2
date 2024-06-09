import requests, os
from views import JobView
from mappings.mappings import job_mapping_with_type, content_mappings
URL = os.getenv('URL')

class GetUserJobViews:
    def execute(self, user_id, bot):
        data = {
                'user_id': user_id,
            }

        response = requests.get(URL + '/job_register/user', json=data)
        JSON = response.json()
        
        job_ids = [job[0] for job in JSON]
        data['job_ids'] = job_ids
        response = requests.get(URL + '/review/not_approved_count', json=data)
        review_counts = {}
        if response:
            review_counts = response.json()

        job_views = []
        for job in JSON:
            response = requests.get(URL + '/content/user_and_job', json={'user_id': user_id, 'job_id': str(job[0])})
            contents = [content_mappings(content) for content in response.json()]
            job_view = JobView(job_mapping_with_type(job), bot, has_review=str(job[0]) in review_counts.keys(), contents=contents)
            job_views.append(job_view)
        return job_views