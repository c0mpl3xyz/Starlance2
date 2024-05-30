import requests, os
from mappings.mappings import review_mapping
URL = os.getenv('URL')
class Review():
    def update(self, review_id, job_register_id, job_id, user_id, link, review_type):
        data = {
            'review_id': review_id,
            'job_register_id': job_register_id,
            'job_id': job_id,
            'user_id': user_id,
            'link': link,
            'type': review_type,
        }

        response = requests.put(URL + '/review', json=data)
        if 'success' not in response.json():
            return False
        return response.json()