# app.py
import os
from flask import Flask
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from content_updater import content_updater
from apis.user_api import user_bp
from apis.token_api import token_bp
from apis.job_api import job_bp
from apis.job_register_api import job_register_bp
from apis.content_api import content_bp
from apis.review_api import review_bp
from apis.collect_api import collect_bp

load_dotenv()

APP_ID = os.getenv('APP_ID')
APP_SECRET = os.getenv('APP_SECRET')
URL = os.getenv('URL')
REDIRECT_URL = URL + 'exchange_token/'
API_VERSION = os.getenv('API_VERSION')
API_PREFIX = os.getenv('API_PREFIX')
URL_PREFIX = f'{API_PREFIX}/{API_VERSION}'

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
    
    # scheduler = BackgroundScheduler()
    # scheduler.add_job(content_updater, 'interval', seconds=10)  # Adjust the interval as needed
    # scheduler.start()

    return app

app = create_app()

@app.route('/')
def hello_world():
    return 'hello world'

if __name__ == '__main__':
    app.run(    
        # host='0.0.0.0', 
        port=9000, 
        # ssl_context=('key/cert.pem', 'key/key.pem'), 
        threaded=True
    )