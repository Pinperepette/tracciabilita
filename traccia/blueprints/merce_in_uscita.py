#!/usr/bin/env python

from flask import Blueprint, render_template, request, redirect, url_for, flash
import sqlite3

merce_in_uscita_bp = Blueprint('merce_in_uscita', __name__, template_folder='../templates/merce_in_uscita')

# Connessione al database
def get_db_connection():
    conn = sqlite3.connect('database/tracabilita.db')
    conn.row_factory = sqlite3.Row
    return conn

# Route per visualizzare la lista delle merci in uscita
@merce_in_uscita_bp.route('/merce_in_uscita')
def index():
    conn = get_db_connection()
    merce_in_uscita = conn.execute('SELECT mu.*, c.ragione_sociale FROM merce_in_uscita mu JOIN clienti c ON mu.cliente_id = c.id').fetchall()
    conn.close()
    return render_template('merce_in_uscita.html', merce_in_uscita=merce_in_uscita)

# Route per aggiungere una nuova merce in uscita
@merce_in_uscita_bp.route('/aggiungi_merce_in_uscita', methods=('GET', 'POST'))
def aggiungi_merce_in_uscita():
    conn = get_db_connection()
    clienti = conn.execute('SELECT * FROM clienti').fetchall()

    if request.method == 'POST':
        data = request.form['data']
        tipo_documento = request.form['tipo_documento']
        numero_documento = request.form['numero_documento']
        cliente_id = request.form['cliente_id']
        destinazione = request.form['destinazione']
        aspetto_esteriore = request.form['aspetto_esteriore']
        note = request.form['note']

        conn.execute('INSERT INTO merce_in_uscita (data, tipo_documento, numero_documento, cliente_id, destinazione, aspetto_esteriore, note) VALUES (?, ?, ?, ?, ?, ?, ?)',
                     (data, tipo_documento, numero_documento, cliente_id, destinazione, aspetto_esteriore, note))
        conn.commit()
        conn.close()
        return redirect(url_for('merce_in_uscita.index'))
    
    return render_template('aggiungi_merce_in_uscita.html', clienti=clienti)

# Route per modificare una merce in uscita
@merce_in_uscita_bp.route('/modifica_merce_in_uscita/<int:merce_in_uscita_id>', methods=('GET', 'POST'))
def modifica_merce_in_uscita(merce_in_uscita_id):
    conn = get_db_connection()
    merce = conn.execute('SELECT * FROM merce_in_uscita WHERE id = ?', (merce_in_uscita_id,)).fetchone()
    clienti = conn.execute('SELECT * FROM clienti').fetchall()

    if request.method == 'POST':
        data = request.form['data']
        tipo_documento = request.form['tipo_documento']
        numero_documento = request.form['numero_documento']
        cliente_id = request.form['cliente_id']
        destinazione = request.form['destinazione']
        aspetto_esteriore = request.form['aspetto_esteriore']
        note = request.form['note']

        conn.execute('UPDATE merce_in_uscita SET data = ?, tipo_documento = ?, numero_documento = ?, cliente_id = ?, destinazione = ?, aspetto_esteriore = ?, note = ? WHERE id = ?',
                     (data, tipo_documento, numero_documento, cliente_id, destinazione, aspetto_esteriore, note, merce_in_uscita_id))
        conn.commit()
        conn.close()
        flash('Merce in uscita aggiornata con successo!')
        return redirect(url_for('merce_in_uscita.index'))

    conn.close()
    return render_template('modifica_merce_in_uscita.html', merce=merce, clienti=clienti)

# Route per eliminare una merce in uscita
@merce_in_uscita_bp.route('/elimina_merce_in_uscita/<int:merce_in_uscita_id>', methods=('POST',))
def elimina_merce_in_uscita(merce_in_uscita_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM merce_in_uscita WHERE id = ?', (merce_in_uscita_id,))
    conn.execute('DELETE FROM dettagli_merce_in_uscita WHERE merce_in_uscita_id = ?', (merce_in_uscita_id,))  # Elimina i dettagli collegati
    conn.commit()
    conn.close()
    flash('Merce in uscita eliminata con successo!')
    return redirect(url_for('merce_in_uscita.index'))

# Route per mostrare il documento (fattura)
@merce_in_uscita_bp.route('/mostra_documento/<int:merce_in_uscita_id>')
def mostra_documento(merce_in_uscita_id):
    conn = get_db_connection()

    # Query per ottenere i dati della merce in uscita e del cliente associato
    merce = conn.execute('SELECT mu.*, c.ragione_sociale, c.partita_iva, c.indirizzo, c.pec, c.sdi FROM merce_in_uscita mu JOIN clienti c ON mu.cliente_id = c.id WHERE mu.id = ?', (merce_in_uscita_id,)).fetchone()

    # Query per ottenere i dettagli della merce in uscita, incluso il prezzo dal listino e il nome del prodotto
    dettagli = conn.execute('''
        SELECT dmu.*, prod.nome AS nome_prodotto, prod.iva, dl.prezzo
        FROM dettagli_merce_in_uscita dmu
        JOIN produzione p ON dmu.produzione_id = p.id
        JOIN prodotti prod ON prod.id = p.prodotto_id
        JOIN dettagli_listino dl ON dl.prodotto_id = prod.id
        WHERE dmu.merce_in_uscita_id = ?
    ''', (merce_in_uscita_id,)).fetchall()

    # Query per ottenere i dati della ditta
    ditta = conn.execute('SELECT * FROM ditta LIMIT 1').fetchone()

    conn.close()

    # Calcoliamo il totale fattura nel backend
    totale_fattura = 0.0
    for dettaglio in dettagli:
        prezzo_totale = dettaglio['prezzo'] * dettaglio['quantita']
        sconto = prezzo_totale * (dettaglio['sconto'] / 100)
        prezzo_scontato = prezzo_totale - sconto
        iva = prezzo_scontato * (dettaglio['iva'] / 100)
        totale_con_iva = prezzo_scontato + iva
        totale_fattura += totale_con_iva

    # Passiamo il totale calcolato al template insieme ai dati della ditta
    return render_template('documento.html', merce=merce, dettagli=dettagli, totale_fattura=round(totale_fattura, 2), ditta=ditta)




# Route per aggiungere dettagli della merce in uscita
@merce_in_uscita_bp.route('/aggiungi_dettagli_merce_in_uscita/<int:merce_in_uscita_id>', methods=('GET', 'POST'))
def aggiungi_dettagli_merce_in_uscita(merce_in_uscita_id):
    conn = get_db_connection()
    produzioni = conn.execute('SELECT * FROM produzione WHERE in_uso = 1').fetchall()

    if request.method == 'POST':
        produzione_id = request.form['produzione_id']
        quantita = request.form['quantita']
        sconto = request.form['sconto']

        conn.execute('INSERT INTO dettagli_merce_in_uscita (merce_in_uscita_id, produzione_id, quantita, sconto) VALUES (?, ?, ?, ?)',
                     (merce_in_uscita_id, produzione_id, quantita, sconto))
        conn.commit()
        conn.close()
        return redirect(url_for('merce_in_uscita.index'))
    
    return render_template('aggiungi_dettagli_merce_in_uscita.html', merce_in_uscita_id=merce_in_uscita_id, produzioni=produzioni)
