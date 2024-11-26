from flask import (
    Blueprint, g, flash, render_template, request, redirect, url_for, session)

import functools
from ..db import get_db

from werkzeug.security import check_password_hash

bp = Blueprint('auth', __name__, url_prefix='/private')

def json_data(description, data):
    columns = [column[0] for column in description]
    return [dict(zip(columns, row)) for row in data]

def get_user(username):
    try:
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        description = cur.description
        user = cur.fetchone()
    except Exception as e:
        flash(f"An error occurred: {e}")
        user = None
    finally:
        cur.close()

    if user is not None:
        user = json_data(description, [user])

    return user

@bp.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        error = None
        user = get_user(username)

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user[0]['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user[0]['id']
            return redirect(url_for('auth.dashboard.dashboard'))

        flash(error)
    if g.user is not None:
        return redirect(url_for('auth.dashboard.dashboard'))
    return render_template('admin.html')

@bp.before_app_request
def load_logged_in_admin():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        try:
            db = get_db()
            cur = db.cursor()
            cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            description = cur.description
            user = cur.fetchone()
            g.user = json_data(description, [user])[0]
        except Exception as e:
            flash(f"An error occurred: {e}")
            g.user = None
        finally:
            cur.close()

@bp.route('/logout', methods=['POST'])
def logout():
    if request.method == 'POST':
        session.clear()
        return redirect(url_for('auth.admin'))

def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return render_template('status.html', status="401"), 401

        return view(**kwargs)

    return wrapped_view

from . import dashboard
bp.register_blueprint(dashboard.bp)
