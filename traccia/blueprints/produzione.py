#!/usr/bin/env python
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
import sqlite3

produzione_bp = Blueprint('produzione', __name__, template_folder='../templates/produzione')

# Connessione al database
def get_db_connection():
    conn = sqlite3.connect('database/tracabilita.db')
    conn.row_factory = sqlite3.Row
    return conn

# Route per visualizzare la lista di produzioni
@produzione_bp.route('/produzione')
def index():
    conn = get_db_connection()
    produzioni = conn.execute('''
        SELECT produzione.id, prodotti.nome AS prodotto, produzione.data_produzione, produzione.lotto,
               produzione.scadenza, produzione.in_uso, produzione.usato
        FROM produzione
        JOIN prodotti ON produzione.prodotto_id = prodotti.id
    ''').fetchall()
    conn.close()
    return render_template('produzione.html', produzioni=produzioni)

# Route per aggiungere una nuova produzione
@produzione_bp.route('/aggiungi_produzione', methods=('GET', 'POST'))
def aggiungi_produzione():
    conn = get_db_connection()
    prodotti = conn.execute('SELECT * FROM prodotti').fetchall()

    if request.method == 'POST':
        # Step 1: Inserimento produzione principale
        data_produzione = request.form['data_produzione']
        lotto = request.form['lotto']
        prodotto_id = request.form['prodotto_id']
        scadenza = request.form['scadenza']
        in_uso = request.form.get('in_uso') == 'on'
        usato = request.form.get('usato') == 'on'

        # Inserimento nella tabella produzione
        conn.execute('''
            INSERT INTO produzione (data_produzione, lotto, prodotto_id, scadenza, in_uso, usato)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (data_produzione, lotto, prodotto_id, scadenza, in_uso, usato))
        produzione_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]

        # Step 2: Inserimento dettagli produzione (materie prime utilizzate)
        materie_id = request.form.getlist('materia_id')  # Usa materia_id invece di merce_id
        kg_utilizzati = request.form.getlist('kg_utilizzati')
        for i in range(len(materie_id)):
            conn.execute('''
                INSERT INTO dettagli_produzione (produzione_id, materia_id, kg_utilizzati)
                VALUES (?, ?, ?)
            ''', (produzione_id, materie_id[i], kg_utilizzati[i]))  # Inseriamo materia_id
        conn.commit()
        conn.close()
        return redirect(url_for('produzione.index'))

    return render_template('aggiungi_produzione.html', prodotti=prodotti)

# API per caricare materie prime (merci) in uso per un dato prodotto
@produzione_bp.route('/api/materie_prime_in_uso/<int:prodotto_id>')
def materie_prime_in_uso(prodotto_id):
    conn = get_db_connection()
    query = '''
        SELECT merci.materia_id, merci.nome_merce, arrivo_merci.kg_pezzi, arrivo_merci.lotto
        FROM merci
        JOIN arrivo_merci ON merci.id = arrivo_merci.merce_id
        WHERE merci.materia_id IN (SELECT materia_id FROM ricetta WHERE prodotto_id = ?) AND arrivo_merci.in_uso = 1
    '''
    materie_prime_in_uso = conn.execute(query, (prodotto_id,)).fetchall()
    conn.close()

    materie_prime_list = [{'materia_id': m['materia_id'], 'nome_merce': m['nome_merce'], 'kg_pezzi': m['kg_pezzi'], 'lotto': m['lotto']} for m in materie_prime_in_uso]
    return jsonify(materie_prime_list)

# Rotta per eliminare una produzione e i relativi dettagli
@produzione_bp.route('/elimina_produzione/<int:id>', methods=('POST',))
def elimina_produzione(id):
    conn = get_db_connection()
    try:
        # Elimina i dettagli associati alla produzione
        conn.execute('DELETE FROM dettagli_produzione WHERE produzione_id = ?', (id,))
        # Elimina la produzione stessa
        conn.execute('DELETE FROM produzione WHERE id = ?', (id,))
        conn.commit()
    finally:
        conn.close()
    return redirect(url_for('produzione.index'))

# Rotta per modificare una produzione
@produzione_bp.route('/modifica_produzione/<int:id>', methods=('GET', 'POST'))
def modifica_produzione(id):
    conn = get_db_connection()
    produzione = conn.execute('SELECT * FROM produzione WHERE id = ?', (id,)).fetchone()
    prodotti = conn.execute('SELECT * FROM prodotti').fetchall()

    if request.method == 'POST':
        # Step 1: Modifica produzione principale
        data_produzione = request.form['data_produzione']
        lotto = request.form['lotto']
        prodotto_id = request.form['prodotto_id']
        scadenza = request.form['scadenza']
        in_uso = request.form.get('in_uso') == 'on'
        usato = request.form.get('usato') == 'on'

        # Aggiorna la produzione
        conn.execute('''
            UPDATE produzione SET data_produzione = ?, lotto = ?, prodotto_id = ?, scadenza = ?, in_uso = ?, usato = ?
            WHERE id = ?
        ''', (data_produzione, lotto, prodotto_id, scadenza, in_uso, usato, id))

        # Step 2: Aggiorna dettagli della produzione (elimina e riaggiunge)
        conn.execute('DELETE FROM dettagli_produzione WHERE produzione_id = ?', (id,))
        materie_id = request.form.getlist('materia_id')
        kg_utilizzati = request.form.getlist('kg_utilizzati')
        for i in range(len(materie_id)):
            conn.execute('''
                INSERT INTO dettagli_produzione (produzione_id, materia_id, kg_utilizzati)
                VALUES (?, ?, ?)
            ''', (id, materie_id[i], kg_utilizzati[i]))
        conn.commit()
        conn.close()
        return redirect(url_for('produzione.index'))

    # Recuperiamo i dettagli della produzione
    dettagli_produzione = conn.execute('''
        SELECT dp.materia_id, mp.nome AS nome_materia, dp.kg_utilizzati
        FROM dettagli_produzione dp
        JOIN materie_prime mp ON dp.materia_id = mp.id
        WHERE dp.produzione_id = ?
    ''', (id,)).fetchall()

    conn.close()
    return render_template('modifica_produzione.html', produzione=produzione, prodotti=prodotti, dettagli=dettagli_produzione)


@produzione_bp.route('/scheda/<int:produzione_id>')
def scheda_produzione(produzione_id):
    conn = get_db_connection()

    # Ottenere i dettagli della produzione
    produzione = conn.execute('SELECT * FROM produzione WHERE id = ?', (produzione_id,)).fetchone()

    if produzione is None:
        return "Produzione non trovata", 404

    # Ottenere il prodotto associato alla produzione
    prodotto = conn.execute('SELECT * FROM prodotti WHERE id = ?', (produzione['prodotto_id'],)).fetchone()

    # Ottenere i dettagli delle materie prime utilizzate nella produzione e i valori nutrizionali dalle merci
    materie_prime = conn.execute('''
    SELECT dp.kg_utilizzati, m.nome_merce, am.lotto, m.proteine, m.carboidrati, m.grassi, m.zuccheri, m.grassi_saturi, m.fibre_alimentari
    FROM dettagli_produzione dp
    JOIN merci m ON dp.materia_id = m.id
    JOIN arrivo_merci am ON am.merce_id = m.id
    WHERE dp.produzione_id = ?
    ''', (produzione_id,)).fetchall()

    # Calcolo dei valori nutrizionali totali della produzione
    valori_nutrizionali = {
        'proteine': 0,
        'carboidrati': 0,
        'grassi': 0,
        'zuccheri': 0,
        'grassi_saturi': 0,
        'fibre_alimentari': 0
    }

    for materia in materie_prime:
        valori_nutrizionali['proteine'] += materia['proteine'] * materia['kg_utilizzati']
        valori_nutrizionali['carboidrati'] += materia['carboidrati'] * materia['kg_utilizzati']
        valori_nutrizionali['grassi'] += materia['grassi'] * materia['kg_utilizzati']
        valori_nutrizionali['zuccheri'] += materia['zuccheri'] * materia['kg_utilizzati']
        valori_nutrizionali['grassi_saturi'] += materia['grassi_saturi'] * materia['kg_utilizzati']
        valori_nutrizionali['fibre_alimentari'] += materia['fibre_alimentari'] * materia['kg_utilizzati']

    conn.close()

    return render_template('produzione/scheda_produzione.html', produzione=produzione, prodotto=prodotto, materie_prime=materie_prime, valori_nutrizionali=valori_nutrizionali)
