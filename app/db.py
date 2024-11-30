from flask_mysqldb import MySQL
from flask import current_app
import click
import os

mysql = MySQL()

def get_db():
    """Get a database connection."""
    try:
        db = mysql.connection
    except Exception as e:
        current_app.logger.error(f"Failed to connect to the database: {e}")
        raise
    return db

def json_data(description, data):
    if not data or not description:
        return None

    data = [data] if not isinstance(data[0], tuple) else data

    columns = [column[0] for column in description]
    return [dict(zip(columns, row)) for row in data]

def query_db(query, args=(), one=False, commit=False):
    try:
        cur = get_db().cursor()
        cur.execute(query, args)
        results = json_data(cur.description, cur.fetchall())
        if commit:
            get_db().commit()
    except Exception as e:
        current_app.logger.error(f"Query failed: {e}")
        if commit:
            get_db().rollback()
            return
        raise
    finally:
        cur.close()

    if commit:
        return

    return (results[0] if results else None) if one else results

def init_db():
    """Initialize the database by executing the schema."""
    db = get_db()
    cursor = db.cursor()

    schema_path = os.path.join(current_app.root_path, '../schema.sql')
    if not os.path.exists(schema_path):
        current_app.logger.error(f"Schema file not found: {schema_path}")
        raise FileNotFoundError(f"Schema file not found: {schema_path}")

    try:
        with open(schema_path, 'r') as f:
            schema = f.read()

        for command in schema.split(';'):
            if command.strip():
                cursor.execute(command)

        db.commit()
    except Exception as e:
        db.rollback()
        current_app.logger.error(f"Failed to initialize the database: {e}")
        raise
    finally:
        cursor.close()

@click.command('init-db')
def init_db_command():
    """Command-line command to initialize the database."""
    try:
        init_db()
        click.echo('Initialized the database.')
    except Exception as e:
        click.echo(f'Failed to initialize the database: {e}')

def init_app(app):
    """Register database functions with the Flask app."""
    mysql.init_app(app)
    app.cli.add_command(init_db_command)