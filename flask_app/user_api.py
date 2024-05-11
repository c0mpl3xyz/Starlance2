from flask import Blueprint, request, jsonify
from sql_db.user import User
from sql_db.conn import ConnectSQL
import os
from dotenv import load_dotenv
load_dotenv()

host = os.getenv('SQL_HOST')
user = os.getenv('SQL_USER')
password = os.getenv('SQL_PASSWORD')
database = os.getenv('SQL_DATABASE')

cursor = ConnectSQL(host, user, password, database).get_cursor()
user_bp = Blueprint('user_api', __name__)
user = User(cursor)

@user_bp.route('/user', methods=['POST'])
def create():
    discord_id = request.args.get('discord_id')
    fb_id = request.args.get('fb_id')
    ig_id = request.args.get('ig_id')
    tiktok_id = request.args.get('tiktok_id')
    youtube_id = request.args.get('youtube_id')
    result = user.create(discord_id, fb_id, ig_id, tiktok_id, youtube_id)
    
    return jsonify({'result': result})

@user_bp.route('/user', methods=['DELETE'])
def delete():
    discord_id = request.args.get('discord_id')
    result = user.delete(discord_id)
    return jsonify({'result': result})

@user_bp.route('/user', methods=['PUT'])
def edit():
    discord_id = request.args.get('discord_id')
    fb_id = request.args.get('fb_id')
    ig_id = request.args.get('ig_id')
    tiktok_id = request.args.get('tiktok_id')
    youtube_id = request.args.get('youtube_id')
    
    result = user.edit(discord_id, fb_id, ig_id, tiktok_id, youtube_id)
    return jsonify({'result': result})

@user_bp.route('/user', methods=['GET'])
def get():
    discord_id = request.args.get('discord_id')
    result = user.get(discord_id)
    return jsonify({'result': result})