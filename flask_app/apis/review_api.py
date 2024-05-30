from flask import Blueprint, request, jsonify
from sql_db.conn import ConnectSQL
import os
from dotenv import load_dotenv
from sql_db.review import Review
from usecases.get_review import GetReviewByJob, GetReviewByUser, GetReviewByJobRegister, GetReviewByJobRegisterAndUser

review_bp = Blueprint('review', __name__, url_prefix='/review')

def extract_review_request(request):
    review_id = request.json.get('id')
    job_register_id = request.json.get('job_register_id')
    job_id = request.json.get('job_id')
    user_id = request.json.get('user_id')
    link = request.json.get('link')
    review_type = request.json.get('type')
    return review_id, job_register_id, job_id, user_id, link, review_type

@review_bp.route('/', methods=['PUT'])
def upate_review():
    review_id, job_register_id, job_id, user_id, link, review_type = extract_review_request(request)

    connection = ConnectSQL().get_connection()
    cursor = connection.cursor()
    updated: bool = False
    message: str = ''

    try:
        review = Review(cursor)
        updated = review.update(review_id, job_register_id, job_id, user_id, link, review_type)
        if updated:
            connection.commit()
            review_id = cursor.lastrowid
            message = 'review updated'
        else:
            message = 'review not updated'
            
        result = {
            'success': updated,
            'review_id': review_id,
            'message': message
        }

        return jsonify(result)
    finally:
        connection.close()

@review_bp.route('/', methods=['POST'])
def create_review():
    _, job_register_id, job_id, user_id, link, review_type = extract_review_request(request)

    connection = ConnectSQL().get_connection()
    cursor = connection.cursor()
    created: bool = False
    review_id = None
    message: str = ''

    try:
        review = Review(cursor)
        created = review.create(job_register_id, job_id, user_id, link, review_type)
        if created:
            connection.commit()
            review_id = cursor.lastrowid
            message = 'review created'
        else:
            message = 'review not created'
            
        result = {
            'success': created,
            'review_id': review_id,
            'message': message
        }

        return jsonify(result)
    finally:
        connection.close()

@review_bp.route('/', methods=['GET'])
def get_review_by_id():
    review_id = request.json.get('review_id')
    connection = ConnectSQL().get_connection()
    cursor = connection.cursor()
    try:
        review = Review(cursor)
        data = review.get_by_id(review_id)
        return jsonify(data)
    finally:
        connection.close()

@review_bp.route('/job', methods=['GET'])
def get_by_job():
    job_id = request.json.get('job_id')
    data = GetReviewByJob().execute(job_id)
    return jsonify(data)

@review_bp.route('/job_register', methods=['GET'])
def get_by_job_register():
    job_register_id = request.json.get('job_register_id')
    data = GetReviewByJobRegister().execute(job_register_id)
    return jsonify(data)

@review_bp.route('/user', methods=['GET'])
def get_by_user():
    user_id = request.json.get('user_id')
    data = GetReviewByUser().execute(user_id)
    return jsonify(data)

@review_bp.route('/job_register_and_user', methods=['GET'])
def get_by_job_register_user():
    job_register_id = request.json.get('job_register_id')
    user_id = request.json.get('user_id')
    data = GetReviewByJobRegisterAndUser().execute(job_register_id, user_id)
    return jsonify(data)