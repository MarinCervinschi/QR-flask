from flask import (
    Blueprint, flash, render_template, g, request, redirect, url_for, send_file, current_app as app)

from ..db import query_db

import qrcode
import io

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@bp.before_request
def check_admin():
    if g.user is None:
        return render_template('error.html', error='401'), 401

@bp.route('/')
def dashboard():
    return render_template('auth/dashboard.html', links=get_links(), css_file="css/dashboard.css")

def get_links():
    try:
        query = "SELECT * FROM dynamic_links"
        links = query_db(query)
    except Exception as e:
        flash(f"An error occurred: {e}", "error")
        links = None

    return links

def add_link(internal, external):
    external = external.replace("http://", "").replace("https://", "")

    try:
        query = "INSERT INTO dynamic_links (internal, external) VALUES (%s, %s)"
        query_db(query, (internal, external), commit=True)
    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
        raise

def get_internal(internal):
    try:
        query = "SELECT * FROM dynamic_links WHERE internal = %s"
        internal = query_db(query, (internal,), one=True)
    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
        internal = None

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
            flash('Link added successfully!', 'success')
        except Exception as e:
            flash(f"An unexpected error occurred: {e}", "error")
    else:
        flash(error, "error"), 500
        
    return redirect(url_for('auth.dashboard.dashboard'))

@bp.route('/delete', methods=['POST'])
def delete():
    id = request.form['id']
    try:    
        query = "DELETE FROM dynamic_links WHERE id = %s"
        query_db(query, (id,), commit=True)
        flash('Link deleted successfully!', 'success')
    except Exception as e:
        flash(f"An error occurred while deleting: {e}", "error")
        return redirect(url_for('auth.dashboard.dashboard')), 500
    
    return redirect(url_for('auth.dashboard.dashboard'))


@bp.route('/edit', methods=['POST'])
def edit():
    id = request.form.get('id')
    external_value = request.form['external']

    try:
        query = "UPDATE dynamic_links SET external = %s WHERE id = %s"
        query_db(query, (external_value, id), commit=True)
        flash('Link updated successfully!', 'success')
    except Exception as e:
        flash(f"An error occurred while updating the link: {e}", 'error')
        return redirect(url_for('auth.dashboard.dashboard')), 500

    return redirect(url_for('auth.dashboard.dashboard'))

def get_link(id):
    try:
        query = "SELECT * FROM dynamic_links WHERE id = %s"
        link = query_db(query, (id,), one=True)
    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
        link = None

    return link

@bp.route('/qr', methods=['POST'])
def qr():
    id = request.form['id']
    if id is None:
        flash("An error occurred: no id provided", "error")
        return redirect(url_for('auth.dashboard.dashboard')), 500
    
    link = get_link(id)
    if link is None:
        flash("An error occurred: no link found", "error")
        return redirect(url_for('auth.dashboard.dashboard')), 500
    
    url = app.config['APP_URL'] + link['internal']
    print(url)
    filename = f"{link['internal']}_to_{link['external']}.png"

    try:
        img = qrcode.make(url)
        img_io = io.BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)

        return send_file(img_io, mimetype='image/png', as_attachment=True, download_name=filename)
    except Exception as e:
        flash(f"An error occurred while generating the QR code: {e}", "error")
        return redirect(url_for('auth.dashboard.dashboard')), 500
    