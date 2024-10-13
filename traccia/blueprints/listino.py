#!/usr/bin/env python

from flask import Blueprint, render_template, request, redirect, url_for
import sqlite3

listino_bp = Blueprint('listino', __name__, template_folder='../templates/listino')

# Connessione al database
def get_db_connection():
    conn = sqlite3.connect('database/tracabilita.db')
    conn.row_factory = sqlite3.Row
    return conn

# Route per visualizzare la lista dei listini
@listino_bp.route('/listini')
def index():
    conn = get_db_connection()
    listini = conn.execute('SELECT * FROM listini').fetchall()
    conn.close()
    return render_template('listini.html', listini=listini)

# Route per aggiungere un nuovo listino
@listino_bp.route('/aggiungi_listino', methods=('GET', 'POST'))
def aggiungi_listino():
    if request.method == 'POST':
        nome = request.form['nome']
        descrizione = request.form['descrizione']

        conn = get_db_connection()
        conn.execute('INSERT INTO listini (nome, descrizione) VALUES (?, ?)', (nome, descrizione))
        conn.commit()
        conn.close()
        return redirect(url_for('listino.index'))
    
    return render_template('aggiungi_listino.html')

# Route per gestire i dettagli di un listino specifico
@listino_bp.route('/dettagli_listino/<int:listino_id>', methods=('GET', 'POST'))
def dettagli_listino(listino_id):
    conn = get_db_connection()

    # Recupera il listino e i prodotti disponibili
    listino = conn.execute('SELECT * FROM listini WHERE id = ?', (listino_id,)).fetchone()
    prodotti = conn.execute('SELECT * FROM prodotti').fetchall()

    if request.method == 'POST':
        prodotto_id = request.form['prodotto_id']
        formato = request.form['formato']
        prezzo = request.form['prezzo']

        # Inserisci i dettagli del listino
        conn.execute('INSERT INTO dettagli_listino (listino_id, prodotto_id, formato, prezzo) VALUES (?, ?, ?, ?)',
                     (listino_id, prodotto_id, formato, prezzo))
        conn.commit()
        conn.close()
        return redirect(url_for('listino.dettagli_listino', listino_id=listino_id))

    # Recupera i dettagli del listino
    dettagli = conn.execute('''
        SELECT dl.id, p.nome AS prodotto, dl.formato, dl.prezzo
        FROM dettagli_listino dl
        JOIN prodotti p ON dl.prodotto_id = p.id
        WHERE dl.listino_id = ?
    ''', (listino_id,)).fetchall()

    conn.close()
    return render_template('dettagli_listino.html', listino=listino, prodotti=prodotti, dettagli=dettagli)
