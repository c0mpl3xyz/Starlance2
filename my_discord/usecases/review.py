import requests, os
# from mappings.mappings import review_mappings
URL = os.getenv('URL')
class Review():
    def update(self, review_id=None, job_register_id=None, job_id=None, user_id=None, link=None, review_type=None, descripton=None):
        data = {
            'id': review_id,
            'job_register_id': job_register_id,
            'job_id': job_id,
            'user_id': user_id,
            'link': link,
            'type': review_type,
            'description': descripton
        }

        response = requests.put(URL + '/review', json=data)
        if 'success' not in response.json():
            return False
        return response.json()