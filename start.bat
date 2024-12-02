@echo off
REM File start.bat

REM .flask.env config
IF NOT EXIST .flask.env (
    echo FLASK_APP=app>> .flask.env
    echo FLASK_RUN_PORT=5000>> .flask.env
    echo FLASK_RUN_HOST=127.0.0.1>> .flask.env
    echo APP_URL=http://127.0.0.1:5000>> .flask.env
    echo SECRET_KEY=your_secret_key>> .flask.env
    echo PERMANENT_SESSION_LIFETIME=30>> .flask.env
)

REM .mysql.env config
IF NOT EXIST .mysql.env (
    echo MYSQL_ROOT_PASSWORD=gYeH97kPb4viZp2>> .mysql.env
    echo MYSQL_HOST=qr-db>> .mysql.env
    echo MYSQL_PORT=3306>> .mysql.env
    echo MYSQL_PASSWORD=gYeH97kPb4viZp2>> .mysql.env
    echo MYSQL_DB=qr_db>> .mysql.env
)

REM OS specific commands
echo Running on Windows
docker compose up --build -d