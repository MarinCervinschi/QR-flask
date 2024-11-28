from flask import (
    Blueprint, flash, render_template, g, request, redirect, url_for)

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

def add_link(internal, external):
    try:
        db = get_db()
        cur = db.cursor()
        cur.execute("INSERT INTO dynamic_links (internal, external) VALUES (%s, %s)", (internal, external))
        db.commit()
    except Exception as e:
        flash(f"An error occurred while adding the link: {e}", "error")
        db.rollback()
    finally:
        cur.close()

def get_internal(internal):
    try:
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT * FROM dynamic_links WHERE internal = %s", (internal,))
        description = cur.description
        internal = cur.fetchone()
    except Exception as e:
        flash(f"An error occurred nh: {e}")
        internal = None
    finally:
        cur.close()

    if internal is not None:
        internal = json_data(description, [internal])

    return internal

@bp.route('/add', methods=['POST'])
def add():
    # Recupera i dati dal form
    internal = request.form.get('internal')
    external = request.form.get('external')

    error = None
    internal_link = get_internal(internal)
    
    if internal_link is not None:
        error = "This internal path is already available"

    if error is None:
        try:
            add_link(internal, external)
        except Exception as e:
            flash(f"An unexpected error occurred: {e}", "error")
    else:
        flash(error), 500
        
    return redirect(url_for('auth.dashboard.dashboard'))
    

    
