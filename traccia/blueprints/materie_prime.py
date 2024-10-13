#!/usr/bin/env python

from flask import Blueprint, render_template, request, redirect, url_for
import sqlite3

# Definizione del blueprint
materie_prime_bp = Blueprint('materie_prime', __name__, template_folder='../templates/materie_prime')

# Connessione al database
def get_db_connection():
    conn = sqlite3.connect('database/tracabilita.db')
    conn.row_factory = sqlite3.Row
    return conn

# Route per visualizzare le materie prime
@materie_prime_bp.route('/materie_prime')
def index():
    conn = get_db_connection()
    materie = conn.execute('SELECT * FROM materie_prime').fetchall()
    conn.close()
    return render_template('materie_prime.html', materie=materie)

# Route per aggiungere una nuova materia prima
@materie_prime_bp.route('/aggiungi_materia', methods=('GET', 'POST'))
def aggiungi_materia():
    if request.method == 'POST':
        nome = request.form['nome']
        if nome:
            conn = get_db_connection()
            conn.execute('INSERT INTO materie_prime (nome) VALUES (?)', (nome,))
            conn.commit()
            conn.close()
            return redirect(url_for('materie_prime.index'))
    return render_template('aggiungi_materia.html')

# Route per eliminare una materia prima
@materie_prime_bp.route('/elimina_materia/<int:id>')
def elimina_materia(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM materie_prime WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('materie_prime.index'))
