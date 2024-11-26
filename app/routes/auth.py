from flask import (
    Blueprint, flash, render_template, request, redirect, url_for, session)

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
            session['user'] = user
            return redirect(url_for('auth.dashboard'))

        flash(error)
    
    return render_template('admin.html')


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

    print(links)
    return links

@bp.route('/admin/dashboard')
def dashboard():
    if 'user' in session:
        return render_template('dashboard.html', links=get_links())
    else:
        return redirect(url_for('auth.admin'))
    
