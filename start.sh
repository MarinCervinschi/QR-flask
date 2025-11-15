#!/bin/bash
#File start.bash

# .flask.env config
if [ ! -f .flask.env ]; then
    cat <<EOT >> .flask.env
    FLASK_APP=app  # The app name
    FLASK_RUN_PORT=5000  # Port for the app
    FLASK_RUN_HOST=0.0.0.0  # App host (0.0.0.0 for Docker)
    APP_URL=http://localhost:8000  # URL for the app and QR code
    SECRET_KEY=your_secret_key  # Secret key for Flask
    PERMANENT_SESSION_LIFETIME=30  # Session lifetime in minutes
EOT
fi

# .mysql.env config
if [ ! -f .mysql.env ]; then
    cat <<EOT >> .mysql.env
    MYSQL_ROOT_PASSWORD=gYeH97kPb4viZp2
    MYSQL_HOST=qr-db
    MYSQL_PORT=3306
    MYSQL_PASSWORD=gYeH97kPb4viZp2
    MYSQL_DB=qr_db
EOT
fi

# OS specific commands
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Running on macOS"
    # macOS specific command
    docker compose up --build -d
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Running on Linux"
    # Linux specific command
    docker-compose up --build -d
else
    echo "Unsupported OS"
fi
