#!/bin/bash
#File start.bash

# OS specific commands
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS specific command
    docker compose down -v
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux specific command
    docker-compose down -v
else
    echo "Unsupported OS"
fi