from flask import Blueprint, render_template, redirect, flash

from ..db import get_db
from .auth import json_data

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/<string>', methods=['GET'])
def custom_route(string):
    try:
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT * FROM dynamic_links WHERE internal = %s", (string,))
        description = cur.description
        check = cur.fetchone()
    except Exception as e:
        flash(f"An error occurred nh: {e}")
        check = None
    finally:
        cur.close()

    if check is not None:
        external_link = json_data(description, [check])[0]['external']
        print(external_link)
        return redirect(f'http://{external_link}') 

    return render_template('error.html', error="404")

@bp.app_errorhandler(404)
def page_not_found(error):
    return render_template('error.html', error="404"), 404