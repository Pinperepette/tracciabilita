

# Sistema di Tracciabilità - Gestione Produzione e Logistica

![Dashboard](./image.png)

## Descrizione

Il Sistema di Tracciabilità è una soluzione completa per la gestione di materie prime, fornitori, prodotti, clienti, magazzino e operazioni logistiche. Sviluppato utilizzando **Flask** e **SQLite**, permette di monitorare l'intero ciclo produttivo e la gestione delle merci in entrata e in uscita. Con un'interfaccia intuitiva basata su **Bootstrap**, l'applicazione è altamente accessibile e personalizzabile.

### Funzionalità Principali

- **Inserimenti Base**
  - Gestione di **materie prime**, fornitori, rappresentanti, prodotti e listini.
  - Aggiunta e modifica delle destinazioni dei clienti.
  - Possibilità di associare listini ai clienti.

- **Operazioni**
  - **Arrivo merci**: tracciamento dei controlli di qualità, verifica documentale, ispezione visiva e altri controlli specifici.
  - **Produzione**: gestione dei lotti di produzione, con possibilità di visualizzare le materie prime utilizzate e i relativi valori nutrizionali.
  - **Merce in uscita**: generazione e gestione di documenti di spedizione, come DDT e fatture.

- **Ricerca Avanzata**
  - **Tracciabilità delle materie prime**: ricerca per lotto per individuare i prodotti creati con una specifica materia prima e i relativi dettagli di spedizione.
  - **Magazzino**: monitoraggio delle materie prime in uso, meno quelle già utilizzate nella produzione.

- **Gestione Valori Nutrizionali**
  - Calcolo dei valori nutrizionali per i prodotti in base alle materie prime utilizzate.
  - Visualizzazione e stampa delle schede di prodotto complete di ingredienti e valori nutrizionali.

- **Controlli di Arrivo Merci**
  - Gestione e registrazione dei controlli di arrivo merci: verifica imballaggi, temperatura, igiene del trasporto e non conformità.

- **Schede Dettagliate**
  - Generazione di schede dettagliate per arrivo merci e produzione con la possibilità di stampa.

### Tecnologie Utilizzate

- **Python** e **Flask** per il backend.
- **SQLite** per la gestione del database relazionale.
- **Bootstrap** per un'interfaccia utente reattiva e moderna.
- **Jinja2** per il templating e la visualizzazione dinamica dei dati.

### Installazione

1. Clona il repository:
   ```bash
   git clone https://github.com/tuo-repository.git
   ```

2. Installa le dipendenze:
   ```bash
   pip install -r requirements.txt
   ```

3. Esegui l'applicazione:
   ```bash
   python app.py
   ```

4. Accedi all'applicazione tramite il browser all'indirizzo `http://localhost:5000`.

### Struttura del Progetto

```bash
├── app.py
├── blueprints
│   ├── __pycache__
│   │   ├── arrivo_merci.cpython-310.pyc
│   │   ├── clienti.cpython-310.pyc
│   │   ├── ditta.cpython-310.pyc
│   │   ├── fornitori.cpython-310.pyc
│   │   ├── listino.cpython-310.pyc
│   │   ├── materie_prime.cpython-310.pyc
│   │   ├── merce_in_uscita.cpython-310.pyc
│   │   ├── merci.cpython-310.pyc
│   │   ├── prodotti.cpython-310.pyc
│   │   ├── produzione.cpython-310.pyc
│   │   ├── rappresentanti.cpython-310.pyc
│   │   └── ricerca.cpython-310.pyc
│   ├── arrivo_merci.py
│   ├── clienti.py
│   ├── ditta.py
│   ├── fornitori.py
│   ├── listino.py
│   ├── materie_prime.py
│   ├── merce_in_uscita.py
│   ├── merci.py
│   ├── prodotti.py
│   ├── produzione.py
│   ├── rappresentanti.py
│   └── ricerca.py
├── create_db.py
├── database
│   └── tracabilita.db
├── jupyter.ipynb
├── static
│   ├── css
│   │   └── style.css
│   ├── documenti
│   └── schede_tecniche_materie_prime
└── templates
    ├── arrivo_merci
    │   ├── aggiungi_arrivo.html
    │   ├── aggiungi_controllo.html
    │   ├── arrivo_merci.html
    │   └── scheda_arrivo.html
    ├── base.html
    ├── clienti
    │   ├── aggiungi_cliente.html
    │   ├── aggiungi_destinazione.html
    │   └── clienti.html
    ├── ditta
    │   └── gestione_ditta.html
    ├── fornitori
    │   ├── aggiungi_fornitore.html
    │   └── fornitori.html
    ├── index.html
    ├── listino
    │   ├── aggiungi_listino.html
    │   ├── dettagli_listino.html
    │   └── listini.html
    ├── materie_prime
    │   ├── aggiungi_materia.html
    │   └── materie_prime.html
    ├── merce_in_uscita
    │   ├── aggiungi_dettagli_merce_in_uscita.html
    │   ├── aggiungi_merce_in_uscita.html
    │   ├── documento.html
    │   ├── merce_in_uscita.html
    │   └── modifica_merce_in_uscita.html
    ├── merci
    │   ├── aggiungi_merce.html
    │   ├── merci.html
    │   └── modifica_merce.html
    ├── prodotti
    │   ├── aggiungi_prodotto.html
    │   ├── modifica_ricetta.html
    │   ├── prodotti.html
    │   └── scheda_prodotto.html
    ├── produzione
    │   ├── aggiungi_produzione.html
    │   ├── modifica_produzione.html
    │   ├── produzione.html
    │   └── scheda_produzione.html
    ├── rappresentanti
    │   ├── aggiungi_rappresentante.html
    │   └── rappresentanti.html
    └── ricerca
        ├── magazzino.html
        ├── matpri.html
        └── matpri_risultati.html
```

### Licenza

Questo progetto è rilasciato sotto la licenza MIT.
