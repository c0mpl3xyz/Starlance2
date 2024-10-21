# app.py
import logging
import os
from flask import Flask, request, jsonify
from instagram.login import get_manual_link
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler

from content_updater import ContentUpdater
from apis.user_api import user_bp
from apis.token_api import token_bp
from apis.job_api import job_bp
from apis.job_register_api import job_register_bp
from apis.content_api import content_bp
from apis.review_api import review_bp
from apis.collect_api import collect_bp
from logging.handlers import RotatingFileHandler
load_dotenv()

test = os.getenv('TEST')

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s',
                    handlers=[logging.StreamHandler()])

APP_ID = os.getenv('APP_ID')
APP_SECRET = os.getenv('APP_SECRET')
URL = os.getenv('URL')
REDIRECT_URL = URL + 'exchange_token/'
API_VERSION = os.getenv('API_VERSION')
API_PREFIX = os.getenv('API_PREFIX')
URL_PREFIX = f'{API_PREFIX}/{API_VERSION}'


logging.info(f'{URL=}')
logging.info(f'{API_VERSION=}')
logging.info(f'{APP_ID=}')
logging.info(f'{API_PREFIX=}')
logging.info(f'{URL_PREFIX=}')

def create_app():
    app = Flask(__name__)
    app.register_blueprint(user_bp)
    app.register_blueprint(token_bp)
    app.register_blueprint(job_bp)
    app.register_blueprint(job_register_bp)
    app.register_blueprint(content_bp)
    app.register_blueprint(review_bp)
    app.register_blueprint(collect_bp)
    app.config['THREADED'] = True

    try:
        log_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
        log_file_path = os.path.abspath('../../app.log')
        file_handler = RotatingFileHandler(log_file_path, maxBytes=10240, backupCount=3)
        file_handler.setFormatter(log_formatter)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
    except Exception:
        return app
    
    return app

scheduler = None

if test:
    scheduler = BlockingScheduler()
else:
    scheduler = BackgroundScheduler()

scheduler.add_job(ContentUpdater().content_updater, 'interval', minutes=1)
app = create_app()
first = True

@app.before_request
def firstRun():
    global first
    if first:
        logging.info('Test-----------------------------------------')
        first = False
        scheduler.start()

@app.route('/')
def hello_world():
    return 'hello world'

@app.route('/ig_login', methods=['GET'])
def ig_login():
    username = request.json.get('username')
    user_id = request.json.get('user_id')
    link = get_manual_link(user_id, username)
    data = {'link': link}
    return jsonify(data)

if __name__ == '__main__':
    app.run(    
        host='0.0.0.0', 
        port=80,
        ssl_context=('key/cert.pem', 'key/key.pem'), 
        # ssl_context='adhoc',
        threaded=True
    )