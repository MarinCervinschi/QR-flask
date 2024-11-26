from flask import (
    Blueprint, flash, render_template, request, redirect, url_for, session, abort)

from app import mysql

from werkzeug.security import check_password_hash

bp = Blueprint('auth', __name__, url_prefix='/private')

@bp.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cur.fetchone()
            cur.close()
            
            if user and check_password_hash(user['password'], password):
                session['user'] = user
                return redirect(url_for('auth.dashboard'))
            else:
                flash("Username o password errati")
                abort(401)
        except Exception as e:
            flash(str(e))
            abort(500)
    
    return render_template('admin.html')

@bp.route('/admin/dashboard')
def dashboard():
    if 'user' in session:
        return render_template('dashboard.html')
    else:
        return redirect(url_for('auth.admin'))
    
