from flask import (
    Blueprint, flash, render_template, g, request, redirect, url_for, send_file)

from ..db import get_db
from .auth import json_data

import qrcode
import io

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@bp.before_request
def check_admin():
    if g.user is None:
        return render_template('error.html', error='401'), 401

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
    return render_template('auth/dashboard.html', links=get_links())

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

@bp.route('/delete', methods=['POST'])
def delete():
    id = request.form['id']
    try:    
        db = get_db() 
        cur = db.cursor()
        cur.execute("DELETE FROM dynamic_links WHERE id = %s", (id,))
        db.commit()
    except Exception as e:
        flash(f"An error occurred while deleting: {e}", "error")
    finally:
        cur.close()
    
    return redirect(url_for('auth.dashboard.dashboard'))


@bp.route('/edit', methods=['POST'])
def edit():
    id = request.form.get('id')
    external_value = request.form['external']

    try:
        db = get_db()
        cur = db.cursor()

        cur.execute("UPDATE dynamic_links SET external = %s WHERE id = %s", (external_value, id,))
        db.commit()

        # flash('Link updated successfully!', 'success')
    except Exception as e:
        db.rollback()
        flash(f"An error occurred while updating the link: {e}", 'error')
    finally:
        cur.close()

    # Reindirizza all'area desiderata dopo l'aggiornamento
    return redirect(url_for('auth.dashboard.dashboard'))


def get_link(id):
    try:
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT * FROM dynamic_links WHERE id = %s", (id,))
        description = cur.description
        link = cur.fetchone()
    except Exception as e:
        flash(f"An error occurred: {e}")
        link = None
    finally:
        cur.close()

    if link is not None:
        link = json_data(description, [link])[0]

    return link

@bp.route('/qr', methods=['POST'])
def qr():
    id = request.form['id']
    if id is None:
        flash("An error occurred: no id provided", "error")
        return redirect(url_for('auth.dashboard.dashboard'))
    
    link = get_link(id)
    if link is None:
        flash("An error occurred: no link found", "error")
        return redirect(url_for('auth.dashboard.dashboard'))
    
    url = 'http://127.0.0.1:5000/' + link['internal']
    print(url)
    filename = f"{link['internal']}_to_l.png"

    try:
        img = qrcode.make(url)
        img_io = io.BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)

        return send_file(img_io, mimetype='image/png', as_attachment=True, download_name=filename)
    except Exception as e:
        flash(f"An error occurred while generating the QR code: {e}", "error")
    
    return redirect(url_for('auth.dashboard.dashboard'))
    