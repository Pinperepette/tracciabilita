#!/usr/bin/env python

from flask import Blueprint, render_template, request, redirect, url_for
import sqlite3

# Definizione del blueprint
fornitori_bp = Blueprint('fornitori', __name__, template_folder='../templates/fornitori')

# Connessione al database
def get_db_connection():
    conn = sqlite3.connect('database/tracabilita.db')
    conn.row_factory = sqlite3.Row
    return conn

# Route per visualizzare i fornitori
@fornitori_bp.route('/fornitori')
def index():
    conn = get_db_connection()
    fornitori = conn.execute('SELECT * FROM fornitori').fetchall()
    conn.close()
    return render_template('fornitori.html', fornitori=fornitori)

# Route per aggiungere un nuovo fornitore
@fornitori_bp.route('/aggiungi_fornitore', methods=('GET', 'POST'))
def aggiungi_fornitore():
    if request.method == 'POST':
        ragione_sociale = request.form['ragione_sociale']
        indirizzo = request.form['indirizzo']
        email = request.form['email']
        telefono = request.form['telefono']
        descrizione = request.form['descrizione']
        
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO fornitori (ragione_sociale, indirizzo, email, telefono, descrizione)
            VALUES (?, ?, ?, ?, ?)
        ''', (ragione_sociale, indirizzo, email, telefono, descrizione))
        conn.commit()
        conn.close()
        return redirect(url_for('fornitori.index'))
    return render_template('aggiungi_fornitore.html')

# Route per eliminare un fornitore
@fornitori_bp.route('/elimina_fornitore/<int:id>')
def elimina_fornitore(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM fornitori WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('fornitori.index'))
