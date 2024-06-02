import requests, os
from views import JobView
from mappings.mappings import job_mapping_with_type 
URL = os.getenv('URL')

class GetUserJobViews:
    def execute(self, user_id, bot):
        data = {
                'user_id': user_id,
            }

        response = requests.get(URL + '/job_register/user', json=data)
        JSON = response.json()

        if not len(JSON):
            return []
        
        job_ids = [jobs[0] for jobs in JSON]
        print(f'{job_ids=}')

        data['job_ids'] = job_ids
        response = requests.get(URL + '/review/not_approved_count', json=data)

        review_counts: dict = response.json()

        print(f'{review_counts=}')
        jobs = [JobView(job_mapping_with_type(job), bot, has_review=str(job[0]) in review_counts.keys()) for job in JSON]
        return jobs