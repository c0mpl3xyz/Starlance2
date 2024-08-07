from flask import Blueprint, request, jsonify
from sql_db.conn import ConnectSQL
import os
from dotenv import load_dotenv
from sql_db.collect import Collect
from sql_db.user import User
from usecases.get_collect import GetCollectById, GetCollectByUser, GetAllCollectPending

collect_bp = Blueprint('collect', __name__, url_prefix='/collect')

def extract_collect_request(request):
    collect_id = request.json.get('collect_id')
    user_id = request.json.get('user_id')
    points = request.json.get('points')
    point_100 = request.json.get('point_100')
    collect_type = request.json.get('type')
    return collect_id, user_id, points, point_100, collect_type

@collect_bp.route('/', methods=['DELETE'])
def update():
    collect_id, user_id, points, point_100, collect_type = extract_collect_request(request)

    connection = ConnectSQL().get_connection()
    cursor = connection.cursor()
    updated: bool = False
    message: str = ''

    try:
        collect = Collect(cursor)
        collects = collect.get_by_user_id(user_id)
        if not len(collects):
            message = 'already collected'
        else:
            user = User(cursor)
            user_data = user.get_by_id(user_id)
            user.update(user_id, points=user_data[2] - points)

            updated = collect.delete(collect_id)
            if updated:
                connection.commit()
                message = 'collect updated'
            else:
                message = 'collect not updated'
            
        result = {
            'success': updated,
            'collect_id': collect_id,
            'message': message
        }
        return jsonify(result)
    finally:
        connection.close()

@collect_bp.route('/', methods=['POST'])
def create():
    collect_id, user_id, points, point_100, collect_type = extract_collect_request(request)

    connection = ConnectSQL().get_connection()
    cursor = connection.cursor()
    created: bool = False
    collect_id = None
    message: str = ''
    try:
        collect = Collect(cursor)
        created = collect.create(user_id, points, point_100)
        if created:
            connection.commit()
            collect_id = cursor.lastrowid
            message = 'Collect created'
        else:
            message = 'Collect not created'
            
        result = {
            'success': created,
            'collect_id': collect_id,
            'message': message
        }

        return jsonify(result)
    finally:
        connection.close()

@collect_bp.route('/', methods=['GET'])
def get_by_id():
    collect_id = request.json.get('collect_id')
    data = GetCollectById().execute(collect_id)
    return jsonify(data)

@collect_bp.route('/user', methods=['GET'])
def get_by_user():
    user_id = request.json.get('user_id')
    data = GetCollectByUser().execute(user_id)
    return jsonify(data)

@collect_bp.route('/server', methods=['GET'])
def get_all_by_pending():
    data = GetAllCollectPending().execute()
    return jsonify(data)