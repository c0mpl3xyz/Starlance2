from flask import Blueprint, request, jsonify
from sql_db.conn import ConnectSQL
import os
from dotenv import load_dotenv
from sql_db.job import Job
from sql_db.user import User
from sql_db.job_register import JobRegister
from sql_db.job import Job
from usecases.get_all_jobs_by_user_id import GetAllJobsByUser

job_register_bp = Blueprint('job_register', __name__, url_prefix='/job_register')

@job_register_bp.route('/', methods=['POST'])
def job_register():
    user_id = request.json.get('user_id')
    job_id = request.json.get('job_id')
    job_type = request.json.get('type')

    message: str = ''
    success: bool = False
    connection = ConnectSQL().get_connection()
    job_register = JobRegister(connection.cursor())
    user = User(connection.cursor())
    user_exist = user.exists(user_id)
    if not user_exist:
        user.create(user_id)
        
    success = job_register.create(user_id, job_id, job_type)

    if success:
        connection.commit()
        message = 'Job registered to user'
    else:
        message = 'Job already registered'

    result = {
        'success': success,
        'message': message
    }

    return jsonify(result)

@job_register_bp.route('/', methods=['PUT'])
def job_register_update():
    user_id = request.json.get('user_id')
    job_id = request.json.get('job_id')
    job_type = request.json.get('type')

    message: str = ''
    success: bool = False
    connection = ConnectSQL().get_connection()
    job_register = JobRegister(connection.cursor())
    
    success = job_register.update(user_id, job_id, job_type=job_type)

    if success:
        connection.commit()
        message = 'Job updated to user'

    result = {
        'success': success,
        'message': message
    }

    return jsonify(result)

@job_register_bp.route('/user', methods=['GET'])
def get_user_jobs():
    user_id = request.json.get('user_id')
    data = GetAllJobsByUser().execute(user_id)
    return jsonify(data)

@job_register_bp.route('/roles', methods=['GET'])
def get_job_roles():
    roles = request.json.get('roles')
    user_id = request.json.get('user_id')
    
    connection = ConnectSQL().get_connection()
    job = Job(connection.cursor())

    data = job.get_all_by_roles(user_id, roles)
    return jsonify(data)

@job_register_bp.route('/job', methods=['GET'])
def get_job_users():
    job_id = request.json.get('job_id')
    connection = ConnectSQL().get_connection()
    job_register = JobRegister(connection.cursor())
    data = job_register.get_by_job_id(job_id)
    return jsonify(data)

@job_register_bp.route('/user_job', methods=['GET'])
def get_user_job():
    job_id = request.json.get('job_id')
    user_id = request.json.get('user_id')
    connection = ConnectSQL().get_connection()
    job_register = JobRegister(connection.cursor())
    data = job_register.get_by_user_job_id(user_id, job_id)
    return jsonify(data)

# @job_register_bp.route('/server', methods=['GET'])
# def get_server():
#     connection = ConnectSQL().get_connection()
#     job_ids = [job[0] for job in Job(connection.cursor()).get_all_open_job()]
#     job_register = JobRegister(connection.cursor())
#     data = job_register.get_all_by_job_ids(job_ids)
#     return jsonify(data)