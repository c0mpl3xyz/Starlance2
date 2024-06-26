
import os, requests
# from pydantic import BaseModel, EmailStr, AnyUrl
from dotenv import load_dotenv

load_dotenv()
API_VERSION = os.getenv('API_VERSION')
APP_ID = os.getenv('APP_ID')
API_PREFIX = os.getenv('API_PREFIX')
PAGE_ID = os.getenv('PAGE_ID')

URL_PREFIX = f'{API_PREFIX}/{API_VERSION}'

class IGGraph():
    user_id: str
    username: str
    access_token: str
    base_url: str
    permissions: list = [
        'email,instagram_basic',
        # 'read_insights',
        # # 'pages_show_list',
        # 'instagram_basic',
        # 'instagram_manage_insights',
    ]
    def __init__(self, access_token):
        self.access_token = access_token
        self.base_url = URL_PREFIX
        self.url_suffix = f'access_token={self.access_token}'
        self.user_id = '17841465259887339'

    def get_user_id(self):
        return self.user_id
    
    def __permission_list(self):
        url = f'{self.base_url}/me/permissions?status=granted&access_token={self.access_token}'
        response = requests.get(url)
        print(url)
        # permissions = [data['permission'] for data in response.json()['data']]
        return response.json()
    
    def test(self):
        url = f'{self.base_url}/me/accounts?fields=name,id,instagram_business_account'
        response = requests.get(url)
        return response.json()

    def get_permissions(self):
        return self.__permission_list()
    
    def check_permissions(self):
        token_permissions = self.__permission_list()

        missing_permissions = [permission for permission in self.permissions if permission not in token_permissions]
        result = {
            'valid': len(missing_permissions) == 0,
            'missing_permissions': missing_permissions
        }

        return result

    def __find_user_id(self):
        url = f'{self.base_url}/me/accounts?fields=name,instagram_business_account&access_token={self.access_token}'
        response = requests.get(url)
        JSON = response.json()
        for data in JSON['data']:
            print(data['instagram_business_account']['id'])
            return data['instagram_business_account']['id']
            
        return None
        

    def get_media_list(self):
        url = f'{self.base_url}/{self.user_id}/media'
        print(url)
        data = {
            'fields': 'comments_count,shortcode,caption,like_count,media_product_type,media_type,owner,permalink,username,insights.metric(ig_reels_aggregated_all_plays_count)',
            'limit': 200,
            'access_token': self.access_token
            # 'client_id': APP_ID
        }

        params_str = '&'.join([f'{key}={value}' for key, value in data.items()])
        full_url = f'{url}?{params_str}'

        print(full_url)
        response = requests.get(url, data=data)
        return response.json()
    
    def find_media_by_shortcode(self, shortcode):
        JSON = self.get_media_list()
        while True:
            for item in JSON['data']:
                if item['shortcode'] is shortcode:
                    return item
            if 'next' not in JSON:
                break

            url = JSON['next']
            JSON = requests.get(url).json()

        return None
    
if __name__ == '__main__':
    ig_graph = IGGraph('')
    print(ig_graph.get_user_id())
    print(ig_graph.get_media_list())
    # print(ig_graph.get_media_list())