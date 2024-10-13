#!/usr/bin/env python

from flask import Flask, render_template

from blueprints.materie_prime import materie_prime_bp
from blueprints.fornitori import fornitori_bp
from blueprints.merci import merci_bp
from blueprints.rappresentanti import rappresentanti_bp
from blueprints.prodotti import prodotti_bp
from blueprints.arrivo_merci import arrivo_merci_bp
from blueprints.produzione import produzione_bp
from blueprints.listino import listino_bp
from blueprints.clienti import clienti_bp
from blueprints.merce_in_uscita import merce_in_uscita_bp
from blueprints.ditta import ditta_bp
from blueprints.ricerca import ricerca_bp 

import os
import sqlite3

# Funzione per ottenere la connessione al database
def get_db_connection():
    conn = sqlite3.connect('database/tracabilita.db')
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)  
# Registriamo i blueprint
app.register_blueprint(materie_prime_bp)
app.register_blueprint(fornitori_bp)
app.register_blueprint(merci_bp)
app.register_blueprint(rappresentanti_bp)
app.register_blueprint(prodotti_bp)
app.register_blueprint(arrivo_merci_bp)
app.register_blueprint(produzione_bp)
app.register_blueprint(listino_bp)
app.register_blueprint(clienti_bp)
app.register_blueprint(merce_in_uscita_bp)
app.register_blueprint(ditta_bp)
app.register_blueprint(ricerca_bp)

@app.route('/')
def index():
    return render_template('index.html')

@app.context_processor
def inject_ditta():
    conn = get_db_connection()
    ditta = conn.execute('SELECT * FROM ditta LIMIT 1').fetchone()
    conn.close()
    return {'ditta': ditta}

if __name__ == '__main__':
    if not os.path.exists('database/tracabilita.db'):
        # Codice per creare il database se non esiste
        pass
    app.run(debug=True)
