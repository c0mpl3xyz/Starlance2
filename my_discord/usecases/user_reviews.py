import requests, os
from mappings.mappings import review_mappings

URL = os.getenv('URL')
class GetUserReview:
    def execute(self, user_id, bot):
        data = {
                'user_id': user_id,
            }

        response = requests.get(URL + '/review/user', json=data)
        reviews = [review_mappings(review) for review in response.json()]
        return reviews
    
class GetUserReviewView:
    def execute(self, user_id, bot):
        from views import ReviewView
        data = {
                'user_id': user_id,
            }

        response = requests.get(URL + '/review/user', json=data)
        reviews = [ReviewView(review_mappings(review), bot) for review in response.json()]
        return reviews
    
    
class GetCompanyReviewView:
    def execute(self, user_id, bot):
        from views import ReviewView
        data = {
                '': user_id,
            }

        response = requests.get(URL + '/review/company', json=data)
        reviews = [ReviewView(review_mappings(review), bot) for review in response.json()]
        return reviews

class CreateUserReview:
    def execute(self, job_register_id, job_id, user_id, link, description):
        data = {
                'job_reister_id': job_register_id,
                'job_id': job_id,
                'user_id': user_id,
                'link': link,
                'description': description,
                'type': 'Pending'
            }
        
        response = requests.get(URL + 'review/user', json=data)
        JSON = response.json()
        print(f'{JSON=}')
        return None