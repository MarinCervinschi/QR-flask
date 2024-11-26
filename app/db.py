from flask_mysqldb import MySQL
from flask import current_app, g
import click
import os

mysql = MySQL()

def get_db():
    """Get a database connection, initializing it if not already set in the app context."""
    if 'db' not in g:
        try:
            g.db = mysql.connection

        except Exception as e:
            current_app.logger.error(f"Failed to connect to the database: {e}")
            raise
    return g.db

def close_db(e=None):
    """Close the database connection if it exists."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    """Initialize the database by executing the schema."""
    db = get_db()
    cursor = db.cursor()

    schema_path = os.path.join(current_app.root_path, 'schema.sql')
    if not os.path.exists(schema_path):
        current_app.logger.error(f"Schema file not found: {schema_path}")
        raise FileNotFoundError(f"Schema file not found: {schema_path}")

    try:
        with open(schema_path, 'r') as f:
            schema = f.read()
        cursor.execute(schema)
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
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)