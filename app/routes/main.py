from flask import Blueprint, render_template, redirect, flash

from ..db import query_db

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/<string>', methods=['GET'])
def custom_route(string):
    try:
        query = "SELECT * FROM dynamic_links WHERE internal = %s"
        external_link = query_db(query, (string,), one=True)
    except Exception as e:
        flash(f"An error occurred nh: {e}")
        external_link = None

    if external_link is not None:
        return redirect(f'http://{external_link["external"]}') 

    return render_template('error.html', error="404"), 404

@bp.app_errorhandler(404)
def page_not_found(error):
    return render_template('error.html', error="404"), 404