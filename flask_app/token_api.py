from flask import Blueprint, request
from sql_db.conn import ConnectSQL
from typing import Dict, List, Tuple, Union
import os, ast
import requests
from urllib.parse import urlencode
from flask import Flask, request, jsonify, make_response, render_template
from dotenv import load_dotenv
from sql_db.user  import User
from flask_app.sql_db.access_token import AccessToken
import datetime

load_dotenv()

APP_ID = os.getenv('APP_ID')
APP_SECRET = os.getenv('APP_SECRET')
REDIRECT_URL = os.getenv('REDIRECT_URL')
API_VERSION = os.getenv('API_VERSION')
API_PREFIX = os.getenv('API_PREFIX')
URL_PREFIX = f'{API_PREFIX}/{API_VERSION}'

host = os.getenv('SQL_HOST')
user = os.getenv('SQL_USER')
password = os.getenv('SQL_PASSWORD')
database = os.getenv('SQL_DATABASE')

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

    if check_token:
        access_token = JSON['access_token']
        duration = JSON['expires_in']
        token_type = JSON['token_type']
        user_id = state['user_id']
        message: Dict = {}

        user_exist = User(cursor).get_user_by_id(user_id)
        if not user_exist: 
            created = True
            user_exist = User(cursor).create(user_id)

        if user_exist:
            token_creation = AccessToken(cursor).add(access_token, user_id, duration, token_type)

    message = {
            'success': user_exist and token_creation,
            'token_creation': token_creation,
            'access_token': check_token,
            'created': created,
            'created2': created,
        }
        
    return message

@token_bp.route('/exchange_token/', methods=['GET'])
def exchange_token_test():
    code = request.args.get('code')
    state = ast.literal_eval(request.args.get('state'))

    connection = ConnectSQL(host, user, password, database).get_connection()
    cursor = connection.cursor()
    try:
        result = exchange_code_for_token(cursor, APP_ID, APP_SECRET, REDIRECT_URL, code, state)
        if result['success']:
            connection.commit()
    finally:
        connection.close()
    return jsonify(result)

@token_bp.route('/', methods=['GET'])
def home_page():
    return render_template('index.html') 