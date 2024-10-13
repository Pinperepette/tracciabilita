#!/usr/bin/env python

from flask import Blueprint, render_template, request, redirect, url_for
import sqlite3

# Definizione del blueprint
prodotti_bp = Blueprint('prodotti', __name__, template_folder='../templates/prodotti')

# Connessione al database
def get_db_connection():
    conn = sqlite3.connect('database/tracabilita.db')
    conn.row_factory = sqlite3.Row
    return conn

# Route per visualizzare i prodotti
@prodotti_bp.route('/prodotti')
def index():
    conn = get_db_connection()
    prodotti = conn.execute('SELECT * FROM prodotti').fetchall()
    conn.close()
    return render_template('prodotti.html', prodotti=prodotti)

# Route per aggiungere un nuovo prodotto
@prodotti_bp.route('/aggiungi_prodotto', methods=('GET', 'POST'))
def aggiungi_prodotto():
    if request.method == 'POST':
        nome = request.form['nome']
        codice = request.form['codice']
        descrizione = request.form['descrizione']
        iva = request.form['iva']
        unita = request.form['unita']

        conn = get_db_connection()
        conn.execute('INSERT INTO prodotti (nome, codice, descrizione, iva, unita) VALUES (?, ?, ?, ?, ?)',
                     (nome, codice, descrizione, iva, unita))
        conn.commit()
        conn.close()
        return redirect(url_for('prodotti.index'))
    return render_template('aggiungi_prodotto.html')

# Route per eliminare un prodotto
@prodotti_bp.route('/elimina_prodotto/<int:id>', methods=['POST'])
def elimina_prodotto(id):
    conn = get_db_connection()
    # Prima eliminiamo la ricetta associata al prodotto
    conn.execute('DELETE FROM ricetta WHERE prodotto_id = ?', (id,))
    # Poi eliminiamo il prodotto stesso
    conn.execute('DELETE FROM prodotti WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('prodotti.index'))


@prodotti_bp.route('/modifica_ricetta/<int:prodotto_id>', methods=('GET', 'POST'))
def modifica_ricetta(prodotto_id):
    conn = get_db_connection()
    prodotto = conn.execute('SELECT * FROM prodotti WHERE id = ?', (prodotto_id,)).fetchone()
    materie_prime = conn.execute('SELECT * FROM materie_prime').fetchall()
    ricetta = conn.execute('SELECT ricetta.id, materie_prime.nome, ricetta.quantita, ricetta.materia_id FROM ricetta JOIN materie_prime ON ricetta.materia_id = materie_prime.id WHERE prodotto_id = ?', (prodotto_id,)).fetchall()

    if request.method == 'POST':
        materia_id = request.form.getlist('materia_id')
        quantita = request.form.getlist('quantita')
        
        conn.execute('DELETE FROM ricetta WHERE prodotto_id = ?', (prodotto_id,))
        for i in range(len(materia_id)):
            if materia_id[i] and quantita[i]:
                conn.execute('INSERT INTO ricetta (prodotto_id, materia_id, quantita) VALUES (?, ?, ?)', (prodotto_id, materia_id[i], quantita[i]))
        conn.commit()
        conn.close()
        return redirect(url_for('prodotti.index'))

    return render_template('modifica_ricetta.html', prodotto=prodotto, materie_prime=materie_prime, ricetta=ricetta)

