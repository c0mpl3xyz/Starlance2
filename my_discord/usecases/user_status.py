import requests, os
from mappings.mappings import user_mappings
from dotenv import load_dotenv
load_dotenv()
URL = os.getenv('URL')

class GetUserStatus():
    def execute(self, user_id, bot):
        from views import UserView
        data = {
            'user_id': user_id
        }
        response = requests.get(URL + '/user/status', json=data)
        
        JSON = response.json()
        if JSON is None:
            return []
        user = user_mappings(JSON)
        return [UserView(user, bot)]
    
class UpdateUserPoints():
    def execute(self, user_id, points):
        data = {
            'user_id': user_id,
            'points': points
        }
        JSON = requests.put(URL + '/user/points', json=data).json()
        return JSON['success']