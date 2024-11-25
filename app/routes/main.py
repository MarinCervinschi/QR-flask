from flask import Blueprint, render_template, jsonify
from app import mysql

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return "Hello, World!"

@bp.route('/db')
def db():
    try:
        # Creazione del cursore
        cur = mysql.connection.cursor()
        
        # Esecuzione della query
        cur.execute("SELECT * FROM users")
        
        # Recupero dei nomi delle colonne
        columns = [column[0] for column in cur.description]
        
        # Conversione dei risultati in una lista di dizionari
        results = [dict(zip(columns, row)) for row in cur.fetchall()]
        
        # Chiusura del cursore
        cur.close()
        
        # Restituzione come JSON
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500