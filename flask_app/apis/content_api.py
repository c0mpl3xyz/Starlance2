from flask import Blueprint, request, jsonify
from sql_db.conn import ConnectSQL
import os
from dotenv import load_dotenv
from sql_db.content import Content
from usecases.get_content import GetContentByJob, GetContentByJobRegister, GetContentByJobRegisterAndUser, GetContentByUser

content_bp = Blueprint('content', __name__, url_prefix='/content')

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

    return content_id, job_register_id, job_id, user_id, review_id, server_id, content_type, link, point, active

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

@content_bp.route('/', methods=['POST'])
def create_content():
    _, job_register_id, job_id, user_id, review_id, server_id, content_type, link, point, active = extract_content_request(request)

    connection = ConnectSQL().get_connection()
    cursor = connection.cursor()
    created: bool = False
    content_id = None
    message: str = ''

    try:
        content = Content(cursor)
        created = content.create(job_register_id, job_id, user_id, review_id, server_id, content_type, link)
        if created:
            connection.commit()
            content_id = cursor.lastrowid
            message = 'Content created'
        else:
            message = 'Content not created'
            
        result = {
            'success': created,
            'job_id': content_id,
            'message': message
        }

        return jsonify(result)
    finally:
        connection.close()

@content_bp.route('/', methods=['GET'])
def get_content_by_id():
    job_register_id = request.json.get('job_register_id')
    connection = ConnectSQL().get_connection()
    cursor = connection.cursor()
    try:
        content = Content(cursor)
        data = content.get_by_id(job_register_id)
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