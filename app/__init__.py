from flask import Flask

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',  # change this in production
        MYSQL_HOST='127.0.0.1',
        MYSQL_PORT=3306,
        MYSQL_USER='root',
        MYSQL_PASSWORD='root',
        MYSQL_DB='qr_db',
    )

    from . import db
    db.init_app(app)

    from .routes import main
    app.register_blueprint(main.bp)

    from .routes import auth
    app.register_blueprint(auth.bp)
    return app