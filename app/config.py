from dotenv import load_dotenv
from datetime import timedelta as time
import os

def load_env_file(file_path):
    if os.path.exists(file_path):
        load_dotenv(dotenv_path=file_path)
    else:
        print(f"Warning: {file_path} not found.")

load_env_file('.flask.env')

APP_URL = os.getenv('APP_URL', 'http://127.0.0.1:5000/')
SECRET_KEY = os.getenv('SECRET_KEY', 'dev')
minutes = int(os.getenv('PERMANENT_SESSION_LIFETIME', 120))
PERMANENT_SESSION_LIFETIME = time(minutes=minutes)

load_env_file('.mysql.env')

MYSQL_HOST = os.getenv('MYSQL_HOST', '127.0.0.1')
MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
MYSQL_USER = os.getenv('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'root')
MYSQL_DB = os.getenv('MYSQL_DB', 'test_db')