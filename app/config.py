from dotenv import load_dotenv
from datetime import timedelta as time
import os

load_dotenv()

APP_URL = os.getenv('APP_URL', 'http://127.0.0.1:5000/')
minutes = int(os.getenv('PERMANENT_SESSION_LIFETIME', 120))
PERMANENT_SESSION_LIFETIME = time(minutes=minutes)
SECRET_KEY = os.getenv('SECRET_KEY', 'dev')
MYSQL_HOST = os.getenv('MYSQL_HOST', '127.0.0.1')
MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
MYSQL_USER = os.getenv('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'root')
MYSQL_DB = os.getenv('MYSQL_DB', 'qr_db')