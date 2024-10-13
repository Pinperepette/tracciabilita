#!/usr/bin/env python

import sqlite3

def create_dettagli_produzione_table():
    conn = sqlite3.connect('database/tracabilita.db')
    conn.execute('''
    CREATE TABLE IF NOT EXISTS controlli_arrivo_merci (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    arrivo_merce_id INTEGER NOT NULL,
    verifica_documenti BOOLEAN,
    imballaggi_integri BOOLEAN,
    temperatura REAL,
    igiene_mezzo BOOLEAN,
    ispezione_visiva BOOLEAN,
    verifica_scadenza BOOLEAN,
    non_conformita TEXT,
    note_controllo TEXT,
    FOREIGN KEY (arrivo_merce_id) REFERENCES arrivo_merci(id)
);




    ''')
    conn.close()

create_dettagli_produzione_table()
