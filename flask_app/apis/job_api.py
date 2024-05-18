from flask import Blueprint, request, jsonify
from sql_db.conn import ConnectSQL
import os
from dotenv import load_dotenv
from sql_db.job import Job

job_bp = Blueprint('job', __name__, url_prefix='/job')

def extract_job_request(request):
    discord_server_id = request.json.get('discord_server_id')
    name = request.json.get('name')
    start_date = request.json.get('start_date')
    end_date = request.json.get('end_date')
    participation_date = request.json.get('participation_date')
    duration = request.json.get('duration')
    description = request.json.get('description')
    upload_link = request.json.get('upload_link')
    requirements = request.json.get('requirements')

    return discord_server_id, name, start_date, end_date, participation_date, duration, description, upload_link, requirements

@job_bp.route('/', methods=['POST'])
def bank_registration():
    discord_server_id, name, roles, start_date, end_date, participation_date, duration, description, upload_link, requirements = extract_job_request(request)

    connection = ConnectSQL().get_connection()
    cursor = connection.cursor()
    updated: bool = False

    try:
        job = Job(cursor)
        job_exist = job.get_by_id(discord_server_id)
        
        if not job_exist:
            updated = job.create(name, roles, start_date, duration, end_date, participation_date, description, upload_link, requirements)
        
        else:
            updated = job.update(name, roles, start_date, duration, end_date, participation_date, description, upload_link, requirements)

        if updated:
            connection.commit()

        result = {
            'success': updated
        }

        return jsonify(result)
    finally:
        connection.close()