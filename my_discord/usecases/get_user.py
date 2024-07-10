import requests, os, aiohttp
from mappings.mappings import user_mappings
from dotenv import load_dotenv
load_dotenv()
URL = os.getenv('URL')

class GetUserStatus():
    async def execute(self, user_id, bot):
        from views import UserView
        data = {
            'user_id': user_id
        }
        response = requests.get(URL + '/user/status', json=data)
        
        JSON = response.json()
        if JSON is None:
            return []
        user = user_mappings(JSON)
        return [await UserView(user, bot).setup()]
    
class UpdateUserPoints():
    def execute(self, user_id, points):
        data = {
            'user_id': user_id,
            'points': points
        }
        response = requests.put(URL + '/user/points', json=data)
        JSON = response.json()
        return JSON['success']
    
class GetUsersReport():
    async def execute(self):
        content = None
        async with aiohttp.ClientSession() as session:
            async with session.get(URL + '/user/users/report') as response:
                if response.status == 200:
                    content = await response.read()
        return content