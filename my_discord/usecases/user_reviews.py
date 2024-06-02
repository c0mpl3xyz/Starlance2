import requests, os
from mappings.mappings import review_mappings

URL = os.getenv('URL')
class GetUserReview:
    def execute(self, user_id):
        data = {
                'user_id': user_id,
            }

        response = requests.get(URL + '/review/user', json=data)
        reviews = [review_mappings(review) for review in response.json()]
        return reviews

class GetUserReviewById:
    def execute(self, review_id, bot):
        data = {
                'review_id': review_id,
            }

        response = requests.get(URL + '/review', json=data)
        reviews = [review_mappings(review) for review in response.json()]
        if len(reviews):
            reviews = reviews[0]
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
    def execute(self, server_id, bot):
        from views import ReviewView
        data = {
                'server_id': server_id,
        }

        response = requests.get(URL + '/review/company', json=data)
        print(response.text)
        reviews = [ReviewView(review_mappings(review), bot, company=True) for review in response.json()]
        return reviews
    
class UpdateReview:
    def execute(self, review_data):        
        response = requests.put(URL + '/review', json=review_data)
        JSON = response.json()
        return JSON