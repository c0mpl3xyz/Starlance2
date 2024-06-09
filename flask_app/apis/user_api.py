from flask import Blueprint, request, jsonify
from sql_db.user import User
from sql_db.conn import ConnectSQL
import os
from dotenv import load_dotenv
from sql_db.user import User

load_dotenv()

SQL_DICT = {
    'host': os.getenv('SQL_HOST'),
    'user': os.getenv('SQL_USER'),
    'password': os.getenv('SQL_PASSWORD'),
    'database': os.getenv('SQL_DATABASE')
}

user_bp = Blueprint('user_api', __name__, url_prefix='/user')

def extract_user_request(request):
    user_id = request.json.get('user_id')
    total_points = request.json.get('total_points')
    points = request.json.get('points')
    bank_name = request.json.get('bank_name')
    bank_number = request.json.get('bank_number')
    register = request.json.get('register')

    return user_id, total_points, points, bank_name, bank_number, register

@user_bp.route('/bank_register', methods=['POST'])
def bank_registration():
    user_id, _, _, bank_name, bank_number, register = extract_user_request(request)

    connection = ConnectSQL().get_connection()
    updated: bool = False

    try:
        user = User(connection.cursor())
        user_exist = user.get_by_id(user_id)
        debug = ''
        if not user_exist:
            updated = user.create(user_id, bank_name=bank_name, bank_number=bank_number, register=register)
            debug = f'updated {updated}'
        
        else:
            updated = user.update(user_id, bank_name=bank_name, bank_number=bank_number, register=register)
            debug = f'updated {updated}'

        if updated:
            connection.commit()

        result = {
            'success': updated,
            'debug': debug,
        }

        return jsonify(result)
    finally:
        connection.close()

@user_bp.route('/', methods=['GET'])
def get_user():
    user_id = request.args.get('user_id')

    connection = ConnectSQL().get_connection()
    user = User(connection.cursor())

    data = user.get_by_id(user_id)
    return jsonify(data)

@user_bp.route('/status', methods=['GET'])
def user_status():
    user_id, total_points, points, bank_name, bank_number, register = extract_user_request(request)

    connection = ConnectSQL().get_connection()
    updated: bool = False

    try:
        user = User(connection.cursor())
        user_exist = user.get_by_id(user_id)
        # debug = ''
        # if not user_exist:
        #     updated = user.create(user_id, bank_name=bank_name, bank_number=bank_number, register=register)
        #     debug = f'updated {updated}'
        
        # else:
        #     updated = user.update(user_id, bank_name=bank_name, bank_number=bank_number, register=register)
        #     debug = f'updated {updated}'

        # if updated:
        #     connection.commit()

        # result = {
        #     'success': updated,
        #     'debug': debug,
        # }

        return jsonify(user_exist)
    finally:
        connection.close()