from flask import Blueprint, render_template, redirect, flash

from ..db import get_db

def json_data(description, data):
    if data is None or description is None:
        return None

    data = [data] if not isinstance(data[0], tuple) else data

    columns = [column[0] for column in description]
    return [dict(zip(columns, row)) for row in data]

__all__ = ['json_data']

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
        external_link = json_data(cur.description, cur.fetchone())
    except Exception as e:
        flash(f"An error occurred nh: {e}")
        external_link = None
    finally:
        cur.close()

    if external_link is not None:
        return redirect(f'http://{external_link[0]["external"]}') 

    return render_template('error.html', error="404")

@bp.app_errorhandler(404)
def page_not_found(error):
    return render_template('error.html', error="404"), 404