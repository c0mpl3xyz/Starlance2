import requests, os
from mappings.mappings import review_mappings, job_mapping, job_register_mapping
import discord
from utils.enums import Enums
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
    
class GetServerReviewView:
    def execute(self, bot):
        from views import ReviewView
        response = requests.get(URL + '/review/company_all')
        reviews = [ReviewView(review_mappings(review), bot, company=True) for review in response.json()]
        return reviews

class GetServerApprovementView:
    def execute(self, bot):
        from views import ApprovementJobView
        response = requests.get(URL + '/job/open_jobs')

        reviews = []
        for job in response.json():
            job_data = job_mapping(job)
            response = requests.get(URL + '/job_register/job', json={'job_id': job_data['job_id']})
            for job_register_raw in response.json():
                job_register = job_register_mapping(job_register_raw)
                guild_id = Enums.GUILD_ID.value
                guild = bot.get_guild(guild_id)
                user = discord.utils.get(guild.members, id=int(job_register['user_id']))

                embed_data = {
                    'user_id': job_register['user_id'],
                    'server_id': job_data['discord_server_id'],
                    'job_name': job_data['name'],
                    'job_id': job_data['job_id'],
                    'job_roles': job_data['roles'],
                    'user_roles': [role.name for role in user.roles],
                    'start_date': job_data['start_date'],
                    'description': job_data['description'],
                    'type': job_register['type'],
                    'job_type': job_data['job_type']
                }
                job_data['type'] = job_register['type']

                reviews.append(ApprovementJobView(embed_data, job_data, bot))
        return reviews    

class UpdateReview:
    def execute(self, review_data):        
        response = requests.put(URL + '/review', json=review_data)
        JSON = response.json()
        return JSON