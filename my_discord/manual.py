import os
from dotenv import load_dotenv
from urllib.parse import urlencode

load_dotenv()

APP_ID = os.getenv('APP_ID')
URL = os.getenv('URL')
APP_TOKEN = os.getenv('ADMIN_TOKEN')
ADMIN_TOKEN = os.getenv('APP_TOKEN')
CONFIG_ID = os.getenv('CONFIG_ID')
REDIRECT_URL = URL + 'exchange_token/'
CLIENT_SECRET = os.getenv('APP_SECRET')
API_VERSION = os.getenv('API_VERSION')

def get_manual_link(user_id, username):
    # scope = ''
    url = f'https://www.facebook.com/{API_VERSION}/dialog/oauth'
    print(f'{REDIRECT_URL=}')
    data = {
        'client_id': APP_ID,
        # 'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URL,
        # "auth_type": "reauthenticate",
        'scope': 'instagram_basic,instagram_manage_insights',
        'state': {
            'user_id': user_id,
            'username': username
        },
        'response_type': 'code'
        # 'config_id': 985148693320820
    }

    query = urlencode(data)
    link = f'{url}?{query}'

    # Open the authorization URL in the user's browser
    # webbrowser.open(url)
    print(link)
    return link

def get_manual_link_ig(user_id, username):
    # scope = ''

    REDIRECT_URL = 'https://c0mpl3x.pythonanywhere.com/token_api/oauth_ig'
    url = f'https://www.facebook.com//dialog/oauth'
    data = {
        'client_id': APP_ID,
        'display': 'page',
        'extras': {"setup": {"channel": "IG_API_ONBOARDING"}},

        # 'client_secret': CLIENT_SECRET,
        'redirect_uri': f'{REDIRECT_URL}',
        # "auth_type": "reauthenticate",
        'scope': 'instagram_basic,instagram_manage_insights',
        # 'state': {
        #     'user_id': user_id,
        #     'username': username
        # },
        'response_type': 'token'
        # 'config_id': 985148693320820
    }

    query = urlencode(data)
    link = f'{url}?{query}'

    # Open the authorization URL in the user's browser
    # webbrowser.open(url)
    print(link)
    return link

# def debug_token(app_token, admin_token, token):
#     f'graph.facebook.com/debug_token?input_token={token}&access_token={app-token-or-admin-token}'

if __name__ == '__main__':
    link = get_manual_link_ig(user_id='1', username='test')