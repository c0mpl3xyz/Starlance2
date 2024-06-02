import requests, os
from mappings.mappings import job_register_mapping
URL = os.getenv('URL')
class RegisterJob():
    def register(self, user_id, job_id, job_type):
        data = {
            'user_id': user_id,
            'job_id': job_id,
            'type': job_type
        }

        response = requests.post(URL + '/job_register', json=data)
        if 'success' not in response.json():
            return False
        return response.json()
    
    def update(self, user_id, job_id, job_type):
        data = {
            'user_id': user_id,
            'job_id': job_id,
            'type': job_type
        }

        response = requests.put(URL + '/job_register', json=data)
        if 'success' not in response.json():
            return False
        return response.json()
    
    def get_by_user_job(self, user_id, job_id):
        data = {
            'user_id': user_id,
            'job_id': job_id
        }

        response = requests.get(URL + '/job_register/user_job', json=data)
        # if 'success' not in response.json():
        #     return False
        return job_register_mapping(response.json())
    
    def update_link(self, user_id, job_id, instagram_link, facebook_link, youtube_link, tiktok_link):
        data = {
            'user_id': user_id,
            'job_id': job_id,
            'instagram_link': instagram_link,
            'facebook_link': facebook_link,
            'youtube_link': youtube_link,
            'tiktok_link': tiktok_link,
        }

        response = requests.put(URL + '/job_register/link', json=data)
        if 'success' not in response.json():
            return False
        return response.json()