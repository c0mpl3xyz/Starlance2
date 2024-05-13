import os
from user_api import user_bp
from token_api import token_bp
from flask import Flask
from dotenv import load_dotenv
load_dotenv()

APP_ID = os.getenv('APP_ID')
APP_SECRET = os.getenv('APP_SECRET')
REDIRECT_URL = os.getenv('REDIRECT_URL')
API_VERSION = os.getenv('API_VERSION')
API_PREFIX = os.getenv('API_PREFIX')
URL_PREFIX = f'{API_PREFIX}/{API_VERSION}'

app = Flask(__name__)
app.logger.info(REDIRECT_URL)
app.register_blueprint(user_bp)
app.register_blueprint(token_bp)

if __name__ == '__main__':
    app.run(ssl_context=('key/cert.pem', 'key/key.pem'), debug=True, host='0.0.0.0', port=9000, threaded=True)