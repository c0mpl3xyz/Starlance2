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