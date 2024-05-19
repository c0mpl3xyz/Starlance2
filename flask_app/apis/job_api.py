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
    discord_server_id = request.json.get('discord_server_id')
    roles = request.json.get('roles')
    name = request.json.get('name')
    start_date = request.json.get('start_date')
    end_date = request.json.get('end_date')
    participation_date = request.json.get('participation_date')
    duration = request.json.get('duration')
    description = request.json.get('description')
    upload_link = request.json.get('upload_link')
    requirements = request.json.get('requirements')

    return discord_server_id, name, roles, start_date, end_date, participation_date, duration, description, upload_link, requirements

@job_bp.route('/', methods=['POST'])
def create_job():
    discord_id, name, roles, start_date, end_date, participation_date, duration, description, upload_link, requirements = extract_job_request(request)

    connection = ConnectSQL().get_connection()
    cursor = connection.cursor()
    created: bool = False
    job_id = None
    message: str = ''

    try:
        job = Job(cursor)
        created = job.create(discord_id, name, roles, start_date, end_date, duration, participation_date, description, upload_link, requirements)
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

@job_bp.route('/company', methods=['GET'])
def get_company_jobs():
    company_id = request.json.get('company_id')
    data = GetCompanyJobs().execute(company_id)
    return jsonify(data)