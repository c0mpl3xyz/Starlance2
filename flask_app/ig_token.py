
import os, requests
# from pydantic import BaseModel, EmailStr, AnyUrl
from dotenv import load_dotenv

load_dotenv()
API_VERSION = os.getenv('API_VERSION')
API_PREFIX = os.getenv('API_PREFIX')
PAGE_ID = os.getenv('PAGE_ID')

URL_PREFIX = f'{API_PREFIX}/{API_VERSION}'

class IGGraph():
    user_id: str
    username: str
    access_token: str
    base_url: str

    def __init__(self, user_id, username, access_token):
        self.access_token = access_token
        self.username = username
        self.base_url = URL_PREFIX
        self.url_suffix = f'access_token={self.access_token}'
        self.user_id = self.__find_user_id()

    def __permission_list(self):
        url = f'{self.base_url}/me/permissions?status=granted&access_token={self.access_token}'
        response = requests.get(url)
        permissions = [data['permission'] for data in response.json()['data']]
        return permissions
    
    def test(self):
        url = f'{self.base_url}/me/accounts?fields=name,id,instagram_business_account'
        response = requests.get(url)
        return response.json()

    def check_permissions(self, permissions):
        token_permissions = self.__permission_list()
        missing_permissions = [permission for permission in permissions if permission not in token_permissions]

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
            if data['id'] == PAGE_ID:
                return data['instagram_business_account']['id']
            
        return None
        

    def get_media_list(self):
        url = f'{self.base_url}/{self.user_id}/media'
        data = {
            'fields': 'comments_count,shortcode,caption,like_count,media_product_type,media_type,owner,permalink,username,insights.metric(ig_reels_aggregated_all_plays_count)',
            'limit': 200,
            'access_token': self.access_token
        }

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
    access_token = 'EAAVXXqU1qYUBOxZCMBOzqEBr7dhkQOhpZCpPGLdVgeN80T7oBq8jEqrUQW6ZAtW7rOJWU9bAtpZAKUpQjcZBk2R14yOLZAmDvdMHp2QBjRUF9ObeFO8vECNpeojs0QmcbVIlRR7BDlrvQRcs6ZBtvaFFrYl1akiZA4xFZCrOrBZAUYqFF62Ewh1ImR6PiicF9MCCXPiFNQQcoeUOENofxcjZCuf9D5AI5J3I3F72sCkONbmaBWWFrS0tcXjCC9U40Ryj5zmVgZDZD'
    ig_graph = IGGraph('17841407620688258', 'altn_bgn', access_token)

    print(ig_graph.find_media_by_shortcode(''))