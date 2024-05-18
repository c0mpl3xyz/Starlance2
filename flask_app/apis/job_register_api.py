from flask import Blueprint, request, jsonify
from sql_db.conn import ConnectSQL
import os
from dotenv import load_dotenv
from sql_db.job import Job
from sql_db.user import User
from sql_db.job_register import JobRegister
from sql_db.job import Job

job_register_bp = Blueprint('job_register', __name__, url_prefix='/job_register')

@job_register_bp.route('/', methods=['POST'])
def job_register():
    user_id = request.json.get('user_id')
    job_id = request.json.get('job_id')
    message: str = ''
    success: bool = False
    connection = ConnectSQL().get_connection()

    job_register = JobRegister(connection.cursor())
    success = job_register.create(user_id, job_id)

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

@job_register_bp.route('/user', methods=['GET'])
def get_user_jobs():
    user_id = request.json.get('user_id')
    connection = ConnectSQL().get_connection()
    job_register = JobRegister(connection.cursor())
    data = job_register.get_by_user_id(31321)
    return jsonify(data)

@job_register_bp.route('/job', methods=['GET'])
def get_job_users():
    job_id = request.json.get('job_id')
    connection = ConnectSQL().get_connection()
    job_register = JobRegister(connection.cursor())
    data = job_register.get_by_job_id(job_id)
    return jsonify(data)