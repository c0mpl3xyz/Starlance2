from flask import Blueprint, request, jsonify, send_file
from sql_db.conn import ConnectSQL
import os
from dotenv import load_dotenv
from sql_db.job import Job
from sql_db.user import User
from sql_db.job_register import JobRegister
from usecases.get_all_company_jobs import GetCompanyJobs, GetServerJobs, GetUserJobs
from usecases.get_job_report import GetJobReportById

job_bp = Blueprint('job', __name__, url_prefix='/job')

def extract_job_request(request):
    job_id = request.json.get('discord_server_id')
    discord_server_id = request.json.get('discord_server_id')
    server_name = request.json.get('server_name')
    roles = request.json.get('roles')
    budget = request.json.get('budget')
    name = request.json.get('name')
    start_date = request.json.get('start_date')
    end_date = request.json.get('end_date')
    participation_date = request.json.get('participation_date')
    duration = request.json.get('duration')
    description = request.json.get('description')
    upload_link = request.json.get('upload_link')
    requirements = request.json.get('requirements')
    job_type = request.json.get('type')
    user_count = request.json.get('user_count')
    point = request.json.get('point')

    return job_id, discord_server_id, server_name, name, roles, budget, start_date, end_date, participation_date, duration, description, upload_link, requirements, job_type, user_count, point

@job_bp.route('/status', methods=['PUT'])
def upate_status():
    job_id = request.json.get('job_id')
    job_type = request.json.get('type')
    connection = ConnectSQL().get_connection()
    cursor = connection.cursor()
    updated: bool = False
    message: str = ''

    try:
        job = Job(cursor)
        updated = job.update_status(job_id, job_type)

        if updated:
            connection.commit()
            job_id = cursor.lastrowid
            message = 'Job updated'
        else:
            message = 'Job not updated'
            
        result = {
            'success': updated,
            'job_id': job_id,
            'message': message
        }

        return jsonify(result)
    finally:
        connection.close()
@job_bp.route('/', methods=['PUT'])
def upate_job():
    job_id, discord_id, server_name, name, roles, budget, start_date, end_date, participation_date, duration, description, upload_link, requirements, job_type, user_count, point = extract_job_request(request)

    connection = ConnectSQL().get_connection()
    cursor = connection.cursor()
    updated: bool = False
    job_id = None
    message: str = ''

    data = {
            'discord_id': discord_id,
            'name': name,
            'server_name': server_name,
            'roles': roles,
            'budget': budget,
            'start_date': start_date,
            'end_date': end_date,
            'duration': duration,
            'participation_date': participation_date,
            'description': description,
            'upload_link': upload_link,
            'requirements': requirements,
            'job_type': job_type,
            'user_count': user_count,
            'point': point
        }
    try:
        job = Job(cursor)
        updated = job.update(job_id, data)
        if updated:
            connection.commit()
            job_id = cursor.lastrowid
            message = 'Job updated'
        else:
            message = 'Job not updated'
            
        result = {
            'success': updated,
            'job_id': job_id,
            'message': message
        }

        return jsonify(result)
    finally:
        connection.close()

@job_bp.route('/', methods=['POST'])
def create_job():
    _, discord_id, server_name, name, roles, budget, start_date, end_date, participation_date, duration, description, upload_link, requirements, job_type, user_count, point = extract_job_request(request)

    connection = ConnectSQL().get_connection()
    cursor = connection.cursor()
    created: bool = False
    job_id = None
    message: str = ''

    try:
        job = Job(cursor)
        data = {
            'discord_id': discord_id,
            'name': name,
            'server_name': server_name,
            'roles': roles,
            'budget': budget,
            'start_date': start_date,
            'end_date': end_date,
            'duration': duration,
            'participation_date': participation_date,
            'description': description,
            'upload_link': upload_link,
            'requirements': requirements,
            'job_type': job_type,
            'user_count': user_count,
            'point': point
        }
        
        created = job.create(data)
        if created:
            connection.commit()
            job_id = cursor.lastrowid
            message = 'Job created'
        else:
            message = 'Job not created'
            
        result = {
            'success': created,
            'job_id': job_id,
            'message': message
        }

        return jsonify(result)
    finally:
        connection.close()

@job_bp.route('/', methods=['GET'])
def get_job_by_id():
    job_id = request.json.get('job_id')
    connection = ConnectSQL().get_connection()
    cursor = connection.cursor()
    try:
        job = Job(cursor)
        data = job.get_by_id(job_id)
        return jsonify(data)
    finally:
        connection.close()

@job_bp.route('/company', methods=['GET'])
def get_company_jobs():
    company_id = request.json.get('company_id')
    data = GetCompanyJobs().execute(company_id)
    return jsonify(data)

@job_bp.route('/user', methods=['GET'])
def get_user_jobs():
    user_id = request.json.get('user_id')
    data = GetUserJobs().execute(user_id)
    return jsonify(data)

@job_bp.route('/server', methods=['GET'])
def get_server_jobs():
    data = GetServerJobs().execute()
    return jsonify(data)

@job_bp.route('/open_jobs', methods=['GET'])
def get_open_jobs():
    connection = ConnectSQL().get_connection()
    cursor = connection.cursor()
    try:
        job = Job(cursor)
        data = job.get_all_open_job()
        return jsonify(data)
    finally:
        connection.close()

@job_bp.route('/', methods=['DELETE'])
def delete_job():
    job_id = request.json.get('job_id')
    connection = ConnectSQL().get_connection()
    cursor = connection.cursor()
    try:
        job = Job(cursor)
        success = job.delete(job_id)
        connection.commit()
        return jsonify({'success': success})
    finally:
        connection.close()

@job_bp.route('/report', methods=['GET'])
def report():
    job_id = request.json.get('job_id')
    success, file_path = GetJobReportById().execute(job_id)

    try:
        if success:
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({'error': 'Report not found or could not be generated'}), 404
    finally:
        os.remove(file_path)