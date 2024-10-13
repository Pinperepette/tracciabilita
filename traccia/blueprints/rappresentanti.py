#!/usr/bin/env python

from flask import Blueprint, render_template, request, redirect, url_for
import sqlite3

# Definizione del blueprint
rappresentanti_bp = Blueprint('rappresentanti', __name__, template_folder='../templates/rappresentanti')

# Connessione al database
def get_db_connection():
    conn = sqlite3.connect('database/tracabilita.db')
    conn.row_factory = sqlite3.Row
    return conn

# Route per visualizzare i rappresentanti
@rappresentanti_bp.route('/rappresentanti')
def index():
    conn = get_db_connection()
    rappresentanti = conn.execute('SELECT * FROM rappresentanti').fetchall()
    conn.close()
    return render_template('rappresentanti.html', rappresentanti=rappresentanti)

# Route per aggiungere un nuovo rappresentante
@rappresentanti_bp.route('/aggiungi_rappresentante', methods=('GET', 'POST'))
def aggiungi_rappresentante():
    if request.method == 'POST':
        nome = request.form['nome']
        telefono = request.form['telefono']
        email = request.form['email']
        note = request.form['note']

        conn = get_db_connection()
        conn.execute('INSERT INTO rappresentanti (nome, telefono, email, note) VALUES (?, ?, ?, ?)',
                     (nome, telefono, email, note))
        conn.commit()
        conn.close()
        return redirect(url_for('rappresentanti.index'))
    return render_template('aggiungi_rappresentante.html')

# Route per eliminare un rappresentante
@rappresentanti_bp.route('/elimina_rappresentante/<int:id>', methods=['POST'])
def elimina_rappresentante(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM rappresentanti WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('rappresentanti.index'))
