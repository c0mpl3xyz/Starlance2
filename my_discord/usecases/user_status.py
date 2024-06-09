import requests, os
from mappings.mappings import user_mappings
from dotenv import load_dotenv
load_dotenv()
URL = os.getenv('URL')

class GetUserStatus():
    def execute(self, user_id):
        from views import UserView
        data = {
            'user_id': user_id
        }
        response = requests.get(URL + '/user/status', json=data)
        print(response.text)
        print(response.json())

        users = []
        JSON = response.json()
        for user_json in JSON:
            user = user_mappings(user_json)
            users.append(UserView(user))
        return users