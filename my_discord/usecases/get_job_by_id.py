import requests, os

URL = os.getenv('URL')
class GetJobById():
    def __init__(self, job_id):
        self.data = {
                'job_id': job_id
            }
    
    def execute(self):
        response = requests.get(URL + '/job', json=self.data)
        print(f'{response.json()}')
        JSON = response.json()
        print(JSON)
        return None
    

if __name__ == '__init__':
    get_job = GetJobById('')