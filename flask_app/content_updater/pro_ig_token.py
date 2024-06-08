
import os, requests
# from pydantic import BaseModel, EmailStr, AnyUrl
from dotenv import load_dotenv

load_dotenv()
API_VERSION = os.getenv('API_VERSION')
APP_ID = os.getenv('APP_ID')
API_PREFIX = os.getenv('API_PREFIX')
PAGE_ID = os.getenv('PAGE_ID')

URL_PREFIX = f'{API_PREFIX}/{API_VERSION}'
IG_TOKEN = os.getenv('IG_TOKEN')
IG_ID = os.getenv('IG_ID')
PERMISSIONS = ['instagram_manage_insights', 'instagram_basic', 'pages_show_list']

class ProIGToken():
    def __init__(self):
        self.access_token = IG_TOKEN
        self.base_url = URL_PREFIX
        self.url_suffix = f'access_token={self.access_token}'
        self.user_id = IG_ID
        self.permissions = PERMISSIONS
    
    def __permission_list(self):
        url = f'{self.base_url}/me/permissions?status=granted&access_token={self.access_token}'
        response = requests.get(url)
        print(url)
        # permissions = [data['permission'] for data in response.json()['data']]
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

    def get_media_list(self, url=None):
        if url is None:
            url = f'https://graph.facebook.com/v20.0/{IG_ID}?fields=media.limit(10){{shortcode,comments_count,media_product_type,like_count,insights.metric(plays,likes,comments,reach,total_interactions,saved,shares)}}&access_token={IG_TOKEN}'

        response = requests.get(url)
        return response.json()
    
    def sanity_shortcodes(self, shortcodes):
        return [shortcode for shortcode in shortcodes if len(shortcode) == 11]
        
    def filter_by_shortcodes(self, shortcode_dict: dict):
        shortcodes = self.sanity_shortcodes(list(shortcode_dict.keys()))
        if not len(shortcodes):
            return {}
        
        foundcodes = []
        finished = False
        my_result = {}
        first = True
        next_url = None
        while not finished:
            if first:
                media_dict, next_url = self.get_media_dict()
                print('first')
                first = False
            elif next_url is not None:
                media_dict, next_url = self.get_media_dict(next_url)
            
            for shortcode in shortcodes:
                if shortcode in media_dict.keys():
                    foundcodes.append(shortcode)
                    my_result[shortcode_dict[shortcode]] = media_dict[shortcode]
            
            if set(shortcodes).intersection(set(foundcodes)) == set(shortcodes):
                finished = True

            if next_url is None:
                break

        return my_result

    def get_media_dict(self, url=None) -> dict:
        media = self.get_media_list(url)
        if url is None:
            media = media['media']
        my_data = {}
        for data in media['data']:
            if data['media_product_type'] == 'REELS':
                insights_data = data['insights']['data']
                new_data = {}
                for insight in insights_data:
                    if insight['name'] == 'plays':
                        new_data['initial_plays'] = insight['values'][0]['value']

                    if insight['name'] == 'likes':
                        new_data['likes'] = insight['values'][0]['value']

                    if insight['name'] == 'comments':
                        new_data['comments'] = insight['values'][0]['value']

                    if insight['name'] == 'saved':
                        new_data['saves'] = insight['values'][0]['value']

                    if insight['name'] == 'shares':
                        new_data['shares'] = insight['values'][0]['value']

                    if insight['name'] == 'reach':
                        new_data['account_reach'] = insight['values'][0]['value']
                    
                    if insight['name'] == 'total_interactions':
                        new_data['total_interactions'] = insight['values'][0]['value']

                new_data['replays'] = new_data['initial_plays'] - new_data['account_reach']
                new_data['total_plays'] = new_data['initial_plays'] + new_data['replays']
                new_data['points'] = 0 # calculate points
                new_data['engagement'] = 0 # calculate engagement
                my_data[data['shortcode']] = new_data
        next_url = None
        if 'next' in media['paging']:
            next_url = media['paging']['next']
        return my_data, next_url
    
if __name__ == '__main__':
    ig_graph = ProIGToken()
    shortcodes = ['C7Lt8_hLEfS', 'C7D3fqBLoAP', 'C7EHGmxL9pU']
    my_data = ig_graph.filter_by_shortcodes(shortcodes)
    print(my_data)