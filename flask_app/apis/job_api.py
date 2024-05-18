from flask import Blueprint, request, jsonify
from sql_db.conn import ConnectSQL
import os
from dotenv import load_dotenv
from sql_db.job import Job
from sql_db.user import User
from sql_db.job_register import JobRegister

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
    company_id, name, roles, start_date, end_date, participation_date, duration, description, upload_link, requirements = extract_job_request(request)

    connection = ConnectSQL().get_connection()
    created: bool = False

    try:
        job = Job(connection.cursor())
        created = job.create(company_id, name, roles, start_date, end_date, duration, participation_date, description, upload_link, requirements)
        if created:
            connection.commit()

        result = {
            'success': created
        }

        return jsonify(result)
    finally:
        connection.close()