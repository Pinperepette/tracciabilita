#!/usr/bin/env python

from flask import Blueprint, render_template, request, redirect, url_for
import sqlite3

clienti_bp = Blueprint('clienti', __name__, template_folder='../templates/clienti')

# Connessione al database
def get_db_connection():
    conn = sqlite3.connect('database/tracabilita.db')
    conn.row_factory = sqlite3.Row
    return conn

# Route per visualizzare la lista dei clienti
@clienti_bp.route('/clienti')
def index():
    conn = get_db_connection()
    clienti = conn.execute('SELECT c.*, l.nome AS listino_nome FROM clienti c LEFT JOIN listini l ON c.listino_id = l.id').fetchall()
    conn.close()
    return render_template('clienti.html', clienti=clienti)

# Route per aggiungere un nuovo cliente
@clienti_bp.route('/aggiungi_cliente', methods=('GET', 'POST'))
def aggiungi_cliente():
    conn = get_db_connection()
    listini = conn.execute('SELECT * FROM listini').fetchall()

    if request.method == 'POST':
        ragione_sociale = request.form['ragione_sociale']
        partita_iva = request.form['partita_iva']
        pec = request.form['pec']
        sdi = request.form['sdi']
        indirizzo = request.form['indirizzo']
        listino_id = request.form['listino_id']

        conn.execute('INSERT INTO clienti (ragione_sociale, partita_iva, pec, sdi, indirizzo, listino_id) VALUES (?, ?, ?, ?, ?, ?)',
                     (ragione_sociale, partita_iva, pec, sdi, indirizzo, listino_id))
        conn.commit()
        conn.close()
        return redirect(url_for('clienti.index'))
    
    return render_template('aggiungi_cliente.html', listini=listini)

# Route per aggiungere una destinazione per il cliente
@clienti_bp.route('/aggiungi_destinazione/<int:cliente_id>', methods=('GET', 'POST'))
def aggiungi_destinazione(cliente_id):
    if request.method == 'POST':
        destinazione = request.form['destinazione']
        indirizzo = request.form['indirizzo']

        conn = get_db_connection()
        conn.execute('INSERT INTO destinazioni_clienti (cliente_id, destinazione, indirizzo) VALUES (?, ?, ?)',
                     (cliente_id, destinazione, indirizzo))
        conn.commit()
        conn.close()
        return redirect(url_for('clienti.index'))
    
    return render_template('aggiungi_destinazione.html', cliente_id=cliente_id)

# Route per eliminare un cliente
@clienti_bp.route('/elimina_cliente/<int:cliente_id>', methods=['POST'])
def elimina_cliente(cliente_id):
    conn = get_db_connection()

    # Prima di eliminare il cliente, eliminiamo le destinazioni associate
    conn.execute('DELETE FROM destinazioni_clienti WHERE cliente_id = ?', (cliente_id,))

    # Poi eliminiamo il cliente
    conn.execute('DELETE FROM clienti WHERE id = ?', (cliente_id,))
    conn.commit()
    conn.close()
    
    return redirect(url_for('clienti.index'))
