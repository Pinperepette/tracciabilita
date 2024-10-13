#!/usr/bin/env python
import sqlite3
from flask import Blueprint, render_template, request, redirect, url_for

# Definisci la funzione per ottenere la connessione al database
def get_db_connection():
    conn = sqlite3.connect('database/tracabilita.db')
    conn.row_factory = sqlite3.Row
    return conn

ricerca_bp = Blueprint('ricerca', __name__, template_folder='../templates/ricerca')

@ricerca_bp.route('/magazzino')
def magazzino():
    conn = sqlite3.connect('database/tracabilita.db')
    conn.row_factory = sqlite3.Row
    materie_in_uso = conn.execute('''
        SELECT mp.id, mp.nome, SUM(am.kg_pezzi) AS totale_in_arrivo,
        IFNULL(SUM(dp.kg_utilizzati), 0) AS totale_utilizzato,
        (SUM(am.kg_pezzi) - IFNULL(SUM(dp.kg_utilizzati), 0)) AS quantita_disponibile
        FROM materie_prime mp
        JOIN merci m ON m.materia_id = mp.id
        JOIN arrivo_merci am ON am.merce_id = m.id
        LEFT JOIN dettagli_produzione dp ON dp.materia_id = mp.id
        WHERE am.in_uso = 1
        GROUP BY mp.id
    ''').fetchall()
    conn.close()

    return render_template('magazzino.html', materie_in_uso=materie_in_uso)

@ricerca_bp.route('/matpri', methods=['GET', 'POST'])
def matpri():
    conn = get_db_connection()

    if request.method == 'POST':
        lotto = request.form['lotto']

        # Query aggiornata per ottenere le materie prime utilizzate per un dato lotto, i prodotti, il lotto della materia e se sono stati spediti
        materie_prime = conn.execute('''
            SELECT mp.nome AS materia_prima, am.lotto AS lotto_materia, p.nome AS prodotto, dp.kg_utilizzati, 
                   pr.data_produzione, COALESCE(mu.destinazione, 'Non spedito') AS destinazione, 
                   COALESCE(mu.numero_documento, 'N/A') AS numero_documento
            FROM dettagli_produzione dp
            JOIN produzione pr ON dp.produzione_id = pr.id
            JOIN prodotti p ON pr.prodotto_id = p.id
            JOIN materie_prime mp ON dp.materia_id = mp.id
            JOIN arrivo_merci am ON am.merce_id = dp.materia_id
            LEFT JOIN dettagli_merce_in_uscita dmu ON dmu.produzione_id = pr.id
            LEFT JOIN merce_in_uscita mu ON mu.id = dmu.merce_in_uscita_id
            WHERE am.lotto = ? AND am.merce_id = dp.materia_id
        ''', (lotto,)).fetchall()

        conn.close()

        if not materie_prime:
            return render_template('matpri_risultati.html', materie_prime=None, lotto=lotto)

        return render_template('matpri_risultati.html', materie_prime=materie_prime, lotto=lotto)

    conn.close()
    return render_template('matpri.html')


