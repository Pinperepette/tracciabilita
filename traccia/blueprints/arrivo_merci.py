#!/usr/bin/env python

from flask import Blueprint, render_template, request, redirect, url_for
import sqlite3
import os

# Definizione del blueprint
arrivo_merci_bp = Blueprint('arrivo_merci', __name__, template_folder='../templates/arrivo_merci')

# Cartella per salvare i PDF dei documenti
UPLOAD_FOLDER = 'static/documenti'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Connessione al database
def get_db_connection():
    conn = sqlite3.connect('database/tracabilita.db')
    conn.row_factory = sqlite3.Row
    return conn

# Route per visualizzare gli arrivi delle merci
@arrivo_merci_bp.route('/arrivo_merci')
def index():
    conn = get_db_connection()
    arrivi = conn.execute('''
        SELECT arrivo_merci.id, merci.nome_merce, arrivo_merci.data_arrivo, arrivo_merci.kg_pezzi, arrivo_merci.lotto,
               arrivo_merci.scadenza, arrivo_merci.numero_documento, arrivo_merci.in_uso, arrivo_merci.usato
        FROM arrivo_merci
        JOIN merci ON arrivo_merci.merce_id = merci.id
    ''').fetchall()
    conn.close()
    return render_template('arrivo_merci.html', arrivi=arrivi)

# Route per aggiungere un nuovo arrivo
@arrivo_merci_bp.route('/aggiungi_arrivo', methods=('GET', 'POST'))
def aggiungi_arrivo():
    conn = get_db_connection()
    merci = conn.execute('SELECT * FROM merci').fetchall()

    if request.method == 'POST':
        merce_id = request.form['merce_id']
        data_arrivo = request.form['data_arrivo']
        kg_pezzi = request.form['kg_pezzi']
        lotto = request.form['lotto']
        scadenza = request.form['scadenza']
        numero_documento = request.form['numero_documento']
        note = request.form['note']
        in_uso = request.form.get('in_uso') == 'on'
        usato = request.form.get('usato') == 'on'

        # Gestione del caricamento del PDF
        documento = request.files['documento']
        if documento:
            documento_filename = documento.filename
            documento_path = os.path.join(UPLOAD_FOLDER, documento_filename)
            documento.save(documento_path)
        else:
            documento_path = None

        # Inserimento nel database
        conn.execute('''
            INSERT INTO arrivo_merci (merce_id, data_arrivo, kg_pezzi, lotto, scadenza, numero_documento, documento_pdf, note, in_uso, usato)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (merce_id, data_arrivo, kg_pezzi, lotto, scadenza, numero_documento, documento_path, note, in_uso, usato))
        conn.commit()
        conn.close()
        return redirect(url_for('arrivo_merci.index'))

    return render_template('aggiungi_arrivo.html', merci=merci)

@arrivo_merci_bp.route('/aggiungi_controllo/<int:arrivo_merce_id>', methods=['GET', 'POST'])
def aggiungi_controllo(arrivo_merce_id):
    conn = get_db_connection()

    if request.method == 'POST':
        verifica_documenti = request.form.get('verifica_documenti') == 'on'
        imballaggi_integri = request.form.get('imballaggi_integri') == 'on'
        temperatura = request.form['temperatura']
        igiene_mezzo = request.form.get('igiene_mezzo') == 'on'
        ispezione_visiva = request.form.get('ispezione_visiva') == 'on'
        verifica_scadenza = request.form.get('verifica_scadenza') == 'on'
        non_conformita = request.form['non_conformita']
        note_controllo = request.form['note_controllo']

        conn.execute('''
            INSERT INTO controlli_arrivo_merci 
            (arrivo_merce_id, verifica_documenti, imballaggi_integri, temperatura, igiene_mezzo, ispezione_visiva, verifica_scadenza, non_conformita, note_controllo)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (arrivo_merce_id, verifica_documenti, imballaggi_integri, temperatura, igiene_mezzo, ispezione_visiva, verifica_scadenza, non_conformita, note_controllo))

        conn.commit()
        conn.close()
        return redirect(url_for('arrivo_merci.index'))

    conn.close()
    return render_template('aggiungi_controllo.html', arrivo_merce_id=arrivo_merce_id)

@arrivo_merci_bp.route('/mostra_scheda/<int:arrivo_merce_id>')
def mostra_scheda_arrivo(arrivo_merce_id):
    conn = get_db_connection()

    # Ottenere i dettagli dell'arrivo merce
    arrivo_merce = conn.execute('''
        SELECT am.*, m.nome_merce 
        FROM arrivo_merci am 
        JOIN merci m ON am.merce_id = m.id 
        WHERE am.id = ?
    ''', (arrivo_merce_id,)).fetchone()

    # Ottenere i controlli associati all'arrivo merce
    controlli = conn.execute('''
        SELECT *
        FROM controlli_arrivo_merci
        WHERE arrivo_merce_id = ?
    ''', (arrivo_merce_id,)).fetchall()

    conn.close()

    return render_template('scheda_arrivo.html', arrivo_merce=arrivo_merce, controlli=controlli)

@arrivo_merci_bp.route('/elimina_arrivo/<int:id>', methods=['POST'])
def elimina_arrivo(id):
    conn = get_db_connection()
    
    # Prima eliminiamo i controlli associati a questo arrivo di merce
    conn.execute('DELETE FROM controlli_arrivo_merci WHERE arrivo_merce_id = ?', (id,))
    
    # Poi eliminiamo l'arrivo di merce stesso
    conn.execute('DELETE FROM arrivo_merci WHERE id = ?', (id,))
    
    conn.commit()
    conn.close()
    return redirect(url_for('arrivo_merci.index'))
