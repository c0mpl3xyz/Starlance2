from flask import Blueprint, request, redirect
from sql_db.conn import ConnectSQL
from typing import Dict, List, Tuple, Union
import os, ast
import requests
from urllib.parse import urlencode
from flask import Flask, request, jsonify, make_response, render_template, url_for
from dotenv import load_dotenv
from sql_db.user  import User
from sql_db.access_token import AccessToken
from apis.utils import get_fb_pages_ig_accounts
import datetime

load_dotenv()
APP_ID = os.getenv('APP_ID')
APP_SECRET = os.getenv('APP_SECRET')
URL = os.getenv('URL')
REDIRECT_URL = URL + 'exchange_token/'
API_VERSION = os.getenv('API_VERSION')
API_PREFIX = os.getenv('API_PREFIX')
URL_PREFIX = f'{API_PREFIX}/{API_VERSION}'
HOME = os.getenv('HOME')

SQL_DICT = {
    'host': os.getenv('SQL_HOST'),
    'user': os.getenv('SQL_USER'),
    'password': os.getenv('SQL_PASSWORD'),
    'database': os.getenv('SQL_DATABASE')
}

token_bp = Blueprint('token_api', __name__)

def exchange_code_for_token(cursor, client_id, client_secret, redirect_uri, code, state):
    url = f'{URL_PREFIX}/oauth/access_token'
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'code': code
    }

    response = requests.post(url, data=data)
    JSON = response.json()
    # token_bp.logger.info(JSON)
    # token = JSON['access_token']

    check_token = 'access_token' in JSON
    token_creation: bool = False
    user_exist: bool = False
    created: bool = False
    debug = 'token not genearated'
    if check_token:
        access_token = JSON['access_token']
        duration = 90
        token_type = JSON['token_type']
        user_id = state['user_id']
        message: Dict = {}
        debug = ''
        user_exist = User(cursor).get_by_id(user_id)
        debug = 'user exists'
        if not user_exist:
            created = True
            debug = 'user not exists'   
            user_exist = User(cursor).create(user_id)

        if user_exist:
            fb_pages, ig_accounts = get_fb_pages_ig_accounts(access_token)
            token_creation = AccessToken(cursor).add(access_token, user_id, duration, token_type, fb_pages, ig_accounts)

    message = {
            'success': user_exist and token_creation,
            'token_created': token_creation,
            'access_token': check_token,
            'server_created': created,
            'debug': debug,
            'data': data,
            'json': JSON
        }
        
    return message

@token_bp.route('/success')
def success_page():
    return render_template('registered.html')

@token_bp.route('/exchange_token/', methods=['GET'])
def exchange_token_test():
    code = request.args.get('code')
    state = ast.literal_eval(request.args.get('state'))

    connection = ConnectSQL(SQL_DICT).get_connection()
    try:
        result = exchange_code_for_token(connection.cursor(), APP_ID, APP_SECRET, REDIRECT_URL, code, state)
        if result['success']:
            connection.commit()
            # Build the URL with query parameters and redirect
            discord_name = state["username"]
            return redirect(url_for('token_api.success_page', discord_name=discord_name))
        else:
            # return jsonify(result)
            return render_template('unregistered.html')
    except Exception as e:
        # return render_template('unregistered.html')
        data = {'error': str(e)}
        raise e
        return jsonify(data)
    finally:
        connection.close()
    return redirect(url_for('home_page'))

@token_bp.route('/oauth_ig', methods=['GET'])
def oauth_ig():
    return jsonify(request.args.to_dict())
    # url = f'{URL_PREFIX}/oauth/access_token'
    # data = {
    #     'client_id': client_id,
    #     'client_secret': client_secret,
    #     'redirect_uri': redirect_uri,
    #     'code': code
    # }

#     # response = requests.post(url, data=data)
#     # JSON = response.json()
#     # # token_bp.logger.info(JSON)
#     # # token = JSON['access_token']

#     # check_token = 'access_token' in JSON
#     # token_creation: bool = False
#     # user_exist: bool = False
#     # created: bool = False
#     # debug = 'token not genearated'
#     # if check_token:
#     #     access_token = JSON['access_token']
#     #     duration = JSON['expires_in']
#     #     token_type = JSON['token_type']
#     #     user_id = state['user_id']
#     #     message: Dict = {}
#     #     debug = ''
#     #     user_exist = User(cursor).get_by_id(user_id)
#     #     debug = 'user exists'
#     #     if not user_exist:
#     #         created = True
#     #         debug = 'user not exists'
#     #         user_exist = User(cursor).create(user_id)

#     #     if user_exist:
#     #         token_creation = AccessToken(cursor).add(access_token, user_id, duration, token_type)

#     # message = {
#     #         'success': user_exist and token_creation,
#     #         'token_created': token_creation,
#     #         'access_token': check_token,
#     #         'server_created': created,
#     #         'debug': debug,
#     #         'data': data,
#     #         'json': JSON
#     #     }
        
#     # return message