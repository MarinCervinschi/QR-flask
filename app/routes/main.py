from flask import Blueprint, render_template, jsonify

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return "Hello, World!"
