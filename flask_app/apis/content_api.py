from flask import Blueprint, request, jsonify
from sql_db.conn import ConnectSQL
from sql_db.user import User
import os, requests
from dotenv import load_dotenv
from sql_db.content import Content
from usecases.get_content import *
from apis.utils import get_ig_ids


content_bp = Blueprint('content', __name__, url_prefix='/content')

def get_status(user_id, link):
    connection = ConnectSQL().get_connection()
    user = User(connection.cursor())
    try:
        if user.exists(user_id):
            access_token = user.get_access_token(user_id)
            if access_token is not None:
                IG_TOKEN = access_token[0]
                return get_ig_ids(IG_TOKEN, link)

        return None, None
    finally:
        connection.close()

def extract_content_status(request):
    content_id = request.json.get('content_id')
    initial_plays = request.json.get('initial_plays')
    total_plays = request.json.get('total_plays')
    likes = request.json.get('likes')
    replays = request.json.get('replays')
    saves = request.json.get('saves')
    shares = request.json.get('shares')
    comments = request.json.get('comments')
    account_reach = request.json.get('account_reach')
    total_interactions = request.json.get('total_interactions')
    points = request.json.get('points')
    engagement = request.json.get('engagement')
    engagement_rate = request.json.get('engagement_rate')
    active = request.json.get('active')

    return content_id, initial_plays, total_plays, likes, replays, saves, shares, comments, account_reach, total_interactions, points, engagement, engagement_rate, active

def extract_content_request(request):
    content_id = request.json.get('id')
    job_register_id = request.json.get('job_register_id')
    job_id = request.json.get('job_id')
    review_id = request.json.get('review_id')
    user_id = request.json.get('user_id')
    server_id = request.json.get('server_id')
    content_type = request.json.get('type')
    link = request.json.get('link')
    point = request.json.get('point')
    active = request.json.get('active')
    test = request.json.get('test')

    return content_id, job_register_id, job_id, user_id, review_id, server_id, content_type, link, point, active, test

@content_bp.route('/link_by_review', methods=['PUT'])
def upate_content_link():
    content_id, job_register_id, job_id, user_id, review_id, server_id, content_type, link, point, active = extract_content_request(request)

    connection = ConnectSQL().get_connection()
    cursor = connection.cursor()
    updated: bool = False
    message: str = ''

    try:
        content = Content(cursor)
        content_id = 0
        updated = content.update_link(review_id, link)
        if updated:
            connection.commit()
            
            result = content.get_by_review_id(review_id)
            
            if len(result):
                content_id = result[0][0]
            message = 'Content updated'
        else:
            message = 'Content not updated'
            
        result = {
            'success': updated,
            'content_id': content_id,
            'message': message
        }

        return jsonify(result)
    finally:
        connection.close()

@content_bp.route('/', methods=['PUT'])
def upate_content():
    content_id, job_register_id, job_id, user_id, review_id, server_id, content_type, link, point, active = extract_content_request(request)

    connection = ConnectSQL().get_connection()
    cursor = connection.cursor()
    updated: bool = False
    message: str = ''

    try:
        content = Content(cursor)
        updated = content.update_by_id(content_id, job_register_id, job_id, user_id, review_id, server_id, content_type, link, point, active)
        if updated:
            connection.commit()
            content_id = cursor.lastrowid
            message = 'Content updated'
        else:
            message = 'Content not updated'
            
        result = {
            'success': updated,
            'content_id': content_id,
            'message': message
        }

        return jsonify(result)
    finally:
        connection.close()

@content_bp.route('/status', methods=['PUT'])
def update_content_status():
    content_id, initial_plays, total_plays, likes, replays, saves, shares, comments, account_reach, total_interactions, points, engagement, engagement_rate, active = extract_content_status(request)

    connection = ConnectSQL().get_connection()
    cursor = connection.cursor()
    updated: bool = False
    message: str = ''

    try:
        content = Content(cursor)
        updated = content.update_status(content_id, initial_plays, total_plays, likes, replays, saves, shares, comments, account_reach, total_interactions, points, engagement, engagement_rate, active)
        if updated:
            connection.commit()
            content_id = cursor.lastrowid
            message = 'Content updated'
        else:
            message = 'Content not updated'
            
        result = {
            'success': updated,
            'content_id': content_id,
            'message': message
        }

        return jsonify(result)
    finally:
        connection.close()

@content_bp.route('/active', methods=['PUT'])
def update_content_active():
    content_id = request.json.get('content_id')
    active = request.json.get['active']

    connection = ConnectSQL().get_connection()
    cursor = connection.cursor()
    updated: bool = False
    message: str = ''

    try:
        content = Content(cursor)
        updated = content.update_active(content_id, active)
        if updated:
            connection.commit()
            content_id = cursor.lastrowid
            message = 'Content updated'
        else:
            message = 'Content not updated'
            
        result = {
            'success': updated,
            'content_id': content_id,
            'message': message
        }

        return jsonify(result)
    finally:
        connection.close()

@content_bp.route('/', methods=['POST'])
def create_content():
    _, job_register_id, job_id, user_id, review_id, server_id, content_type, link, point, active, test = extract_content_request(request)
    
    ig_id = 'test'
    ig_content_id = 'test'

    # if test and test is not None:
    #     ig_id, ig_content_id = get_status(user_id, link)
        
    #     if ig_id is None and ig_content_id is None:
    #         result = {
    #             'success': False,
    #             'content_id': None,
    #             'message': 'Account not found'
    #         }
            
    #         return jsonify(result)
    
    connection = ConnectSQL().get_connection()
    cursor = connection.cursor()
    created: bool = False
    content_id = None
    message: str = ''

    try:
        content = Content(cursor)
        created = content.create(int(job_register_id), int(job_id), int(user_id), review_id, server_id, content_type, link, ig_id, ig_content_id)
        if created:
            connection.commit()
            content_id = cursor.lastrowid
            message = 'Content created'
        else:
            message = 'Content not created'
            
        result = {
            'success': created,
            'content_id': content_id,
            'message': message
        }

        return jsonify(result)
    finally:
        connection.close()

@content_bp.route('/', methods=['GET'])
def get_content_by_id():
    content_id = request.json.get('content_id')
    connection = ConnectSQL().get_connection()
    cursor = connection.cursor()
    try:
        content = Content(cursor)
        data = content.get_by_id(content_id)
        return jsonify(data)
    finally:
        connection.close()

@content_bp.route('/job', methods=['GET'])
def get_by_job():
    job_id = request.json.get('job_id')
    data = GetContentByJob().execute(job_id)
    return jsonify(data)

@content_bp.route('/job_register', methods=['GET'])
def get_by_job_register():
    job_register_id = request.json.get('job_register_id')
    data = GetContentByJobRegister().execute(job_register_id)
    return jsonify(data)

@content_bp.route('/user', methods=['GET'])
def get_by_user():
    user_id = request.json.get('user_id')
    data = GetContentByUser().execute(user_id)
    return jsonify(data)

@content_bp.route('/user_id', methods=['GET'])
def get_by_user_id():
    user_id = request.args.get('user_id')
    if user_id != 537848640140476436 and user_id != '537848640140476436':
        return jsonify([])
    user_id = 537848640140476436
    data = GetContentByUser().execute(user_id)
    return jsonify(data)

@content_bp.route('/user_and_job', methods=['GET'])
def get_by_user_and_job():
    user_id = request.json.get('user_id')
    job_id = request.json.get('job_id')
    data = GetContentByUserAndJob().execute(user_id, job_id)
    return jsonify(data)

@content_bp.route('/job_register_and_user', methods=['GET'])
def get_by_job_register_user():
    job_register_id = request.json.get('job_register_id')
    user_id = request.json.get('user_id')
    data = GetContentByJobRegisterAndUser().execute(job_register_id, user_id)
    return jsonify(data)

@content_bp.route('/company', methods=['GET'])
def get_by_company():
    server_id = request.json.get('server_id')
    data = GetContentByCompany().execute(server_id)
    return jsonify(data)

@content_bp.route('/server', methods=['GET'])
def get_by_server():
    data = GetContentByServer().execute()
    return jsonify(data)

@content_bp.route('/job_ids', methods=['GET'])
def get_by_job_ids():
    job_ids = request.json.get('job_ids')
    if not len(job_ids):
        return jsonify([])
    data = GetByJobId().execute(job_ids)
    return jsonify(data)