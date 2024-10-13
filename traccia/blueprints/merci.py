#!/usr/bin/env python

from flask import Blueprint, render_template, request, redirect, url_for
import sqlite3
import os

# Definizione del blueprint
merci_bp = Blueprint('merci', __name__, template_folder='../templates/merci')

# Connessione al database
def get_db_connection():
    conn = sqlite3.connect('database/tracabilita.db')
    conn.row_factory = sqlite3.Row
    return conn

# Cartella per salvare le schede tecniche
UPLOAD_FOLDER = 'static/schede_tecniche_materie_prime'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Route per visualizzare le merci
@merci_bp.route('/merci')
def index():
    conn = get_db_connection()
    merci = conn.execute('''
        SELECT merci.id, merci.nome_merce, materie_prime.nome AS materia, fornitori.ragione_sociale AS fornitore
        FROM merci
        JOIN materie_prime ON merci.materia_id = materie_prime.id
        JOIN fornitori ON merci.fornitore_id = fornitori.id
    ''').fetchall()
    conn.close()
    return render_template('merci.html', merci=merci)

# Route per aggiungere una nuova merce
@merci_bp.route('/aggiungi_merce', methods=('GET', 'POST'))
def aggiungi_merce():
    conn = get_db_connection()
    materie_prime = conn.execute('SELECT * FROM materie_prime').fetchall()
    fornitori = conn.execute('SELECT * FROM fornitori').fetchall()
    
    if request.method == 'POST':
        nome_merce = request.form['nome_merce']
        materia_id = request.form['materia_id']
        fornitore_id = request.form['fornitore_id']
        prezzo_kg = request.form['prezzo_kg']
        ue = request.form['ue']
        proteine = request.form['proteine']
        carboidrati = request.form['carboidrati']
        grassi = request.form['grassi']
        zuccheri = request.form['zuccheri']
        grassi_saturi = request.form['grassi_saturi']
        fibre_alimentari = request.form['fibre_alimentari']
        
        # Gestione della scheda tecnica (file upload)
        scheda = request.files['scheda']
        if scheda:
            scheda_filename = scheda.filename
            scheda_path = os.path.join(UPLOAD_FOLDER, scheda_filename)
            scheda.save(scheda_path)
        else:
            scheda_path = None
        
        # Inserimento nel database
        conn.execute('''
            INSERT INTO merci (nome_merce, materia_id, fornitore_id, prezzo_kg, ue, proteine, carboidrati, grassi, zuccheri, grassi_saturi, fibre_alimentari, scheda_tecnica)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (nome_merce, materia_id, fornitore_id, prezzo_kg, ue, proteine, carboidrati, grassi, zuccheri, grassi_saturi, fibre_alimentari, scheda_path))
        conn.commit()
        conn.close()
        return redirect(url_for('merci.index'))
    
    return render_template('aggiungi_merce.html', materie_prime=materie_prime, fornitori=fornitori)

# Route per eliminare una merce
@merci_bp.route('/elimina_merce/<int:id>', methods=['POST'])
def elimina_merce(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM merci WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('merci.index'))

# Route per modificare una merce esistente
@merci_bp.route('/modifica_merce/<int:id>', methods=('GET', 'POST'))
def modifica_merce(id):
    conn = get_db_connection()
    
    # Ottenere i dettagli della merce corrente
    merce = conn.execute('SELECT * FROM merci WHERE id = ?', (id,)).fetchone()
    materie_prime = conn.execute('SELECT * FROM materie_prime').fetchall()
    fornitori = conn.execute('SELECT * FROM fornitori').fetchall()

    if request.method == 'POST':
        nome_merce = request.form['nome_merce']
        materia_id = request.form['materia_id']
        fornitore_id = request.form['fornitore_id']
        prezzo_kg = request.form['prezzo_kg']
        ue = request.form['ue']
        proteine = request.form['proteine']
        carboidrati = request.form['carboidrati']
        grassi = request.form['grassi']
        zuccheri = request.form['zuccheri']
        grassi_saturi = request.form['grassi_saturi']
        fibre_alimentari = request.form['fibre_alimentari']
        
        # Gestione della scheda tecnica (file upload)
        scheda = request.files['scheda']
        if scheda:
            scheda_filename = scheda.filename
            scheda_path = os.path.join(UPLOAD_FOLDER, scheda_filename)
            scheda.save(scheda_path)
        else:
            scheda_path = merce['scheda_tecnica']  # Mantieni il file esistente se non viene caricato uno nuovo
        
        # Aggiornamento nel database
        conn.execute('''
            UPDATE merci
            SET nome_merce = ?, materia_id = ?, fornitore_id = ?, prezzo_kg = ?, ue = ?, proteine = ?, carboidrati = ?, grassi = ?, zuccheri = ?, grassi_saturi = ?, fibre_alimentari = ?, scheda_tecnica = ?
            WHERE id = ?
        ''', (nome_merce, materia_id, fornitore_id, prezzo_kg, ue, proteine, carboidrati, grassi, zuccheri, grassi_saturi, fibre_alimentari, scheda_path, id))
        conn.commit()
        conn.close()
        return redirect(url_for('merci.index'))
    
    conn.close()
    return render_template('modifica_merce.html', merce=merce, materie_prime=materie_prime, fornitori=fornitori)

