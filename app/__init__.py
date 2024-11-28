from flask import Flask
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY', 'dev'), # Default value if not set
        MYSQL_HOST=os.getenv('MYSQL_HOST', '127.0.0.1'),
        MYSQL_PORT=int(os.getenv('MYSQL_PORT', 3306)),
        MYSQL_USER=os.getenv('MYSQL_USER', 'root'),
        MYSQL_PASSWORD=os.getenv('MYSQL_PASSWORD', 'root'),
        MYSQL_DB=os.getenv('MYSQL_DB', 'qr_db'),
        APP_URL=os.getenv('APP_URL', 'http://127.0.0.1:5000/')
    )

    from . import db
    db.init_app(app)

    from .routes import main
    app.register_blueprint(main.bp)

    from .routes import auth
    app.register_blueprint(auth.bp)
    return app