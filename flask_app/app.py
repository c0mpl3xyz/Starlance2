import os
from flask_app.apis.user_api import user_bp
from flask_app.apis.token_api import token_bp
from flask_app.apis.job_api import job_bp
from flask_app.apis.job_register_api import job_register_bp
from flask_app.apis.content_api import content_bp

from flask import Flask
from dotenv import load_dotenv
load_dotenv()

APP_ID = os.getenv('APP_ID')
APP_SECRET = os.getenv('APP_SECRET')
URL = os.getenv('URL')
REDIRECT_URL = URL + '/exchange_token/'
API_VERSION = os.getenv('API_VERSION')
API_PREFIX = os.getenv('API_PREFIX')
URL_PREFIX = f'{API_PREFIX}/{API_VERSION}'

app = Flask(__name__)
app.logger.info(REDIRECT_URL)
app.register_blueprint(user_bp)
app.register_blueprint(token_bp)
app.register_blueprint(job_bp)
app.register_blueprint(job_register_bp)
app.register_blueprint(content_bp)

if __name__ == '__main__':
    app.run(ssl_context=('key/cert.pem', 'key/key.pem'), debug=True, host='0.0.0.0', port=9000, threaded=True)