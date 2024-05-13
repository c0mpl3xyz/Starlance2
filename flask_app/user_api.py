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
    fb_id = request.json.get('fb_id')
    ig_id = request.json.get('ig_id')
    tiktok_id = request.json.get('tiktok_id')
    youtube_id = request.json.get('youtube_id')
    bank_name = request.json.get('bank_name')
    bank_number = request.json.get('bank_number')
    register = request.json.get('register')

    return user_id, fb_id, ig_id, tiktok_id, youtube_id, bank_name, bank_number, register

@user_bp.route('/bank_register', methods=['POST'])
def bank_registration():
    user_id, _, _, _, _, bank_name, bank_number, register = extract_user_request(request)
    user_update = None

    db = ConnectSQL()
    connection = ConnectSQL().get_connection()
    cursor = db.get_cursor()
    user_creation: bool = False

    try:
        user = User(cursor)
        user_exist = user.get_user_by_id(user_id)
        
        if not user_exist:
            user_creation = user.create(user_id, bank_name=bank_name, bank_number=bank_number, register=register)
        
        if user_creation:
            user_update = user.update(user_id, bank_name=bank_name, bank_number=bank_number, register=register)

        if user_update:
            connection.commit()

        result = {'success': user_update is not None}
        return jsonify(result)
    finally:
        connection.close()

# @user_bp.route('/user', methods=['PUT'])
# def edit():
#     user_id, fb_id, ig_id, tiktok_id, youtube_id, bank_name, bank_number, register = extract_user_request(request)

#     result = User
#     return jsonify({'result': result})

# @user_bp.route('/user', methods=['DELETE'])
# def delete():
#     discord_id = request.args.get('discord_id')
#     result = user.delete(discord_id)
#     return jsonify({'result': result})

# @user_bp.route('/user', methods=['GET'])
# def get():
#     discord_id = request.args.get('discord_id')
#     result = user.get(discord_id)
#     return jsonify({'result': result})