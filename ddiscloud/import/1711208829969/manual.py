import os
from dotenv import load_dotenv
from urllib.parse import urlencode

load_dotenv()

APP_ID = os.getenv('APP_ID')
REDIRECT_URL = os.getenv('REDIRECT_URL')
APP_TOKEN = os.getenv('ADMIN_TOKEN')
ADMIN_TOKEN = os.getenv('APP_TOKEN')

def get_manual_link(username):
    scope = 'instagram_basic,pages_show_list'
    url = f'https://www.facebook.com/dialog/oauth'
    data = {
        'client_id': APP_ID,
        'redirect_uri': REDIRECT_URL,
        'scope': scope,
        'state': {
            'username': username
        },
        'response_type': 'code'
    }

    query = urlencode(data)
    link = f'{url}?{query}'

    # Open the authorization URL in the user's browser
    # webbrowser.open(url)
    return link

# def debug_token(app_token, admin_token, token):
#     f'graph.facebook.com/debug_token?input_token={token}&access_token={app-token-or-admin-token}'

if __name__ == '__main__':
    link = get_manual_link()
    print(link)