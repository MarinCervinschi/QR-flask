from flask import (
    Blueprint, flash, render_template, g)

from ..db import get_db
from .auth import json_data

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@bp.before_request
def check_admin():
    if g.user is None:
        return render_template('status.html', status='401'), 401

def get_links():
    try:
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT * FROM dynamic_links")
        description = cur.description
        links = cur.fetchall()
    except Exception as e:
        flash(f"An error occurred: {e}")
        links = None
    finally:
        cur.close()

    if links is not None:
        links = json_data(description, links)

    return links

@bp.route('/')
def dashboard():
    return render_template('dashboard.html', links=get_links())
    
