#!/usr/bin/env python
from flask import Blueprint, render_template, request, redirect, url_for
import sqlite3

# Funzione per ottenere la connessione al database
def get_db_connection():
    conn = sqlite3.connect('database/tracabilita.db')
    conn.row_factory = sqlite3.Row
    return conn

# Definizione del blueprint per la ditta
ditta_bp = Blueprint('ditta', __name__, url_prefix='/ditta')

# Gestione della rotta per inserimento/aggiornamento della ditta
@ditta_bp.route('/', methods=['GET', 'POST'])
def gestione_ditta():
    conn = get_db_connection()
    
    # Preleva i dati della ditta se esiste
    ditta = conn.execute('SELECT * FROM ditta LIMIT 1').fetchone()

    if request.method == 'POST':
        ragione_sociale = request.form['ragione_sociale']
        indirizzo = request.form['indirizzo']
        partita_iva = request.form['partita_iva']
        pec = request.form['pec']
        sdi = request.form['sdi']

        if ditta:
            # Aggiorna la ditta esistente
            conn.execute('''
                UPDATE ditta
                SET ragione_sociale = ?, indirizzo = ?, partita_iva = ?, pec = ?, sdi = ?
                WHERE id = ?
            ''', (ragione_sociale, indirizzo, partita_iva, pec, sdi, ditta['id']))
        else:
            # Inserisci una nuova ditta
            conn.execute('''
                INSERT INTO ditta (ragione_sociale, indirizzo, partita_iva, pec, sdi)
                VALUES (?, ?, ?, ?, ?)
            ''', (ragione_sociale, indirizzo, partita_iva, pec, sdi))

        conn.commit()
        return redirect(url_for('ditta.gestione_ditta'))

    conn.close()

    # Ritorna il template per visualizzare o modificare i dati della ditta
    return render_template('ditta/gestione_ditta.html', ditta=ditta)

@ditta_bp.route('/elimina', methods=['POST'])
def elimina_ditta():
    conn = get_db_connection()
    conn.execute('DELETE FROM ditta')
    conn.commit()
    conn.close()
    return redirect(url_for('ditta.gestione_ditta'))
