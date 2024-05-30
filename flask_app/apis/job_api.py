from flask import Blueprint, request, jsonify
from sql_db.conn import ConnectSQL
import os
from dotenv import load_dotenv
from sql_db.job import Job
from sql_db.user import User
from sql_db.job_register import JobRegister
from usecases.get_all_company_jobs import GetCompanyJobs

job_bp = Blueprint('job', __name__, url_prefix='/job')

def extract_job_request(request):
    job_id = request.json.get('discord_server_id')
    discord_server_id = request.json.get('discord_server_id')
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

    return job_id, discord_server_id, name, roles, budget, start_date, end_date, participation_date, duration, description, upload_link, requirements, job_type, user_count

@job_bp.route('/', methods=['PUT'])
def upate_job():
    job_id, discord_id, name, roles, budget, start_date, end_date, participation_date, duration, description, upload_link, requirements, job_type, user_count = extract_job_request(request)

    connection = ConnectSQL().get_connection()
    cursor = connection.cursor()
    updated: bool = False
    job_id = None
    message: str = ''

    try:
        job = Job(cursor)
        updated = job.update(job_id, discord_id, name, roles, budget, start_date, end_date, duration, participation_date, description, upload_link, requirements, job_type, user_count)
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
    _, discord_id, name, roles, budget, start_date, end_date, participation_date, duration, description, upload_link, requirements, job_type, user_count = extract_job_request(request)

    connection = ConnectSQL().get_connection()
    cursor = connection.cursor()
    created: bool = False
    job_id = None
    message: str = ''

    try:
        job = Job(cursor)
        created = job.create(discord_id, name, roles, budget, start_date, end_date, duration, participation_date, description, upload_link, requirements, job_type, user_count)
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