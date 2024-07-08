import requests, os
from mappings.mappings import content_mapping, review_mapping, job_mapping
from views import ContentView, JobView

URL = os.getenv('URL')
class GetUserContentView:
    def execute(self, user_id, bot):
        data = {
                'user_id': user_id,
        }

        response = requests.get(URL + '/content/user', json=data)

        JSON = response.json()
        if not len(JSON):
            return []
        
        contents = []
        for i, content_json in enumerate(JSON):
            content = content_mapping(content_json)
            contents.append(ContentView(None, content, bot))
        return contents

class GetUserContentReport:
    def execute(self, user_id, bot, server=False):
        data = {
                'user_id': user_id,
        }

        response = requests.get(URL + '/job/user', json=data)
        JOB_JSON = response.json()
        if not len(JOB_JSON):
            return []
        
        jobs = []
        for i, job_json in enumerate(JOB_JSON):
            job = job_mapping(job_json)
            contents = []
            content_data = requests.get(URL + '/content/user_and_job', json={'user_id': user_id, 'job_id': job['job_id']}).json()
            if len(content_data):
                for content in content_data:
                    contents.append(content_mapping(content))
            
            job = JobView(job, bot, company=False, has_review=False, contents=contents, server=server)
            yield job

class GetServerContentView:
    def execute(self, bot):
        response = requests.get(URL + '/content/server')

        contents = []
        JSON = response.json()
        for content_json in JSON:
            content = content_mapping(content_json)
            review_json = requests.get(URL + '/review', json={'review_id': content['review_id']}).json()

            for review in review_json:
                if len(review):
                    contents.append(ContentView(review_mapping(review), content, bot, main=True))
        return contents
    
class GetServerUserContentViews:
    def execute(self, bot, user_id):
        # response = requests.get(URL + '/content/server')
        pass