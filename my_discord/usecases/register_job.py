import requests, os

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