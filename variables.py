import os

# Environment variables
BOT_ID = os.environ.get('BOT_ID')
LISTENING_PORT = os.environ.get('LISTENING_PORT', 2200)
WEB_PORT = os.environ.get('WEB_PORT', 5000)
EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
PROJECT_ID = os.environ.get('PROJECT_ID')
PRIVATE_KEY_ID = os.environ.get('PRIVATE_KEY_ID')
PRIVATE_KEY = os.environ.get('PRIVATE_KEY')
CLIENT_EMAIL = os.environ.get('CLIENT_EMAIL')
CLIENT_ID = os.environ.get('CLIENT_ID')
AUTH_URI = os.environ.get('AUTH_URI')
TOKEN_URI = os.environ.get('TOKEN_URI')
AUTH_PROVIDER_x509_CERT_URL = os.environ.get('AUTH_PROVIDER_CERT_URL')
CLIENT_x509_CERT_URL = os.environ.get('CLIENT_CERT_URL')

# Constants
TYPE = 'service_account'
DEBUG = False
MANUAL_PUSH = False
USE_SPREADSHEET = False
SERVICE_CREDENTIALS = 'client_secret.json'

# Accepted CORS origins
ACCEPTED_ORIGINS = [
    r'(https?:\/\/)?(localhost|127\.0\.0\.1)(:\d+)?',
    r'(https?:\/\/)?(.+)?\.heroku\.com(.+)?',
]
