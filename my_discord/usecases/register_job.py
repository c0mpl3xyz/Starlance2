import requests, os

URL = os.getenv('URL')
class RegisterJob():
    def register(self, user_id, job_id):
        data = {
            'user_id': user_id,
            'job_id': job_id
        }

        response = requests.post(URL + '/job_register', json=data)
        return 'success' in response.json()
