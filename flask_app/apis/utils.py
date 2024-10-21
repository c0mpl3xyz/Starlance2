
from sql_db.conn import ConnectSQL
from sql_db.user import User
import os, requests
from dotenv import load_dotenv
from sql_db.content import Content

URL = os.getenv('URL')      
API_VERSION = os.getenv('API_VERSION')
API_PREFIX = os.getenv('API_PREFIX')
IG_URL_PREFIX = f'{API_PREFIX}/{API_VERSION}'


def get_shortcode(link):
    link = link.replace('https://www.instagram.com/reel/', '').replace('https://www.instagram.com/p/','')
    splits = link.split('/')
    if len(splits):
        return splits[0]
    return None

def get_fb_pages_ig_accounts(token):
    url = f'https://graph.facebook.com/v20.0/me?fields=accounts.limit(30){{connected_instagram_account,global_brand_page_name}}&access_token={token}'
    response = requests.get(url)
    ig_accounts = []
    fb_pages = []

    if response.status_code != 200:
        return ig_accounts, fb_pages    

    
    for account in response.json()["accounts"]["data"]:
        fb_pages.append(f'{account.get("global_brand_page_name")}-{account.get("id")}')
        if "connected_instagram_account" in account:
            ig_accounts.append(account["connected_instagram_account"]["id"])
    
    if len(ig_accounts):
        for idx, account in enumerate(ig_accounts):
            url = f'https://graph.facebook.com/v20.0/{account}?fields=username&access_token={token}'
            response = requests.get(url)
            ig_accounts[idx] = f'{response.json()["username"]}-{ig_accounts[idx]}'
    return fb_pages, ig_accounts
    

def get_ig_ids(token, link):
    shortcode = get_shortcode(link)
    url = f'https://graph.facebook.com/v20.0/me?fields=accounts.limit(30){{connected_instagram_account}}&access_token={token}'
    result = requests.get(url).json()
    ig_ids = [
        account["connected_instagram_account"]['id']
        for account in result.get("accounts", {}).get("data", [])
        if 'connected_instagram_account' in account
    ]

    for ig_id in ig_ids:
        url = None
        while True:
            if url is None:
                url = f'https://graph.facebook.com/{API_VERSION}/{ig_id}/media?fields=shortcode&limit=100&access_token={token}'
            response = requests.get(url)
            if response.status_code == 200:
                JSON = response.json()
                for data in JSON['data']:
                    if data['shortcode'] == shortcode:
                        media_id = data['id']            
                        return ig_id, media_id
                
                if 'paging' in JSON and 'next' in JSON['paging']:
                    url = JSON['paging']['next']
                else:
                    break
            else:
                break
    return None, None

if __name__ == '__main__':
    token = 'EAAOPS5RiFaMBO2bjFGWLd3wMTEpFiFdnAGdGvNq0UyFh2V8GM9QPrstINElYVu1GVVlcrztvszod37cEvPZA6H8ZCrqtBl5AhQb9LUPniKV45lG3RIH2QxolyabIZBX5vN5XcFXOc3DZBMTJtAi8C2UUTXyO2UUAyRB83gfCmMdbO5ghbHGCdWuNtm1Uwmx4rJ4ZB68hAIQLnxKQjBX0oHACu4EWlAhDHdAZDZD'
    print(get_fb_pages_ig_accounts(token))