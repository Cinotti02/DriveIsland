# DriveIsland – Piattaforma di Noleggio Auto Online

**DriveIsland** è un'applicazione web per la gestione e il noleggio online di automobili. Sviluppata con Django e deployata su Render, offre un'esperienza completa sia per clienti che per amministratori, con funzionalità di prenotazione, pagamento, gestione flotte e assistenza integrata.

🔗 **Live demo**: [https://driveisland.onrender.com/](https://driveisland.onrender.com/)

---

## 📦 Funzionalità principali

### 👤 Clienti

Gli utenti registrati appartenenti al gruppo "clienti" possono accedere alle seguenti funzionalità:

- **Registrazione con conferma email**:
  - Al momento della registrazione, viene inviata automaticamente un'email con un link di attivazione per convalidare l’account.

- **Prenotazione auto con pagamento online**:
  - Possibilità di prenotare un’auto disponibile specificando data, ora e luogo di ritiro/riconsegna.
  - Il pagamento avviene in modo sicuro tramite Stripe (in modalità test con carta).

- **Recupero password dimenticata**:
  - Se l’utente dimentica la password, può utilizzare il link "Password dimenticata?" nel form di login.
  - Verrà inviata un’email contenente un link sicuro per reimpostare la password.

- **Annullamento delle prenotazioni**:
  - I clienti possono annullare autonomamente una prenotazione tramite la dashboard.
  - L’annullamento comporta la disattivazione della prenotazione e un'email di conferma viene inviata automaticamente.

- **Gestione del profilo**:
  - Accesso a un'area personale per modificare i propri dati (nome, email, telefono, data di nascita).
  - Possibilità di eliminare definitivamente il proprio account.

- **Visualizzazione prenotazioni personali**:
  - Le prenotazioni attive, future o passate sono visibili in una dashboard personale, con dettagli completi e stato aggiornato.

- **Ricerca avanzata delle auto**:
  - Funzionalità di ricerca e filtro per categoria, disponibilità, caratteristiche (carburante, cambio, aria condizionata, ecc.).

- **Richiesta di assistenza**:
  - Modulo "Contattaci" per inviare richieste di supporto.
  - Le risposte vengono inviate via email direttamente dall’amministratore.

💳 Test pagamento (Stripe):
```
Carta: 4242 4242 4242 4242
Scadenza: qualsiasi data futura
CVV: qualsiasi
```

---

### 🛠️ Amministratori

Gli amministratori hanno **tutti i permessi dei clienti**, con funzionalità avanzate per la gestione completa della piattaforma:

- **Gestione prenotazioni**:
  - Visualizzazione dell’elenco completo di tutte le prenotazioni
  - Filtraggio per cliente, data e stato (completate, in corso, future)
  - Cancellazione delle prenotazioni con:
    - Form dedicato per inserire una motivazione
    - Notifica automatica via email al cliente

- **Gestione richieste di assistenza**:
  - Accesso a tutte le richieste inviate tramite il modulo "Contattaci"
  - Filtraggio per stato (risposte/non risposte) e data
  - Risposta diretta tramite form, con invio automatico via email

- **Gestione auto (CRUD completo)**:
  - Aggiunta di nuove auto tramite form
  - Modifica delle informazioni esistenti (modello, prezzo, disponibilità, ecc.)
  - Eliminazione di auto dal sistema
  - Visualizzazione dettagliata di ogni auto

- **Gestione attributi delle auto**:
  - Modello
  - Categoria
  - Colore
  - Aria condizionata
  - Immagini
  - Sconti (creazione, modifica, eliminazione; le auto scontate appaiono evidenziate nella homepage)
---

## 🗂️ Architettura

Il progetto è suddiviso in **5 app Django**:

| App         | Descrizione                                      |
|-------------|--------------------------------------------------|
| `users`     | Gestione utenti, registrazione, profilo, login   |
| `cars`      | Catalogo e gestione veicoli                      |
| `bookings`  | Prenotazioni e gestione pagamenti                |
| `contact`   | Modulo assistenza e sistema messaggistica        |
| `pages`     | Homepage, pagine informative e navigazione       |

**User Model** esteso e personalizzato.

---

## 🔐 Gruppi e permessi
- `Clienti`: assegnati automaticamente alla registrazione
- `Amministratori`: accesso avanzato al backend e gestione

---

## ⚙️ Setup locale

1. Clona il repository:
```bash
    git clone https://github.com/tuo-utente/driveisland.git
    cd driveisland
```

2. Crea ambiente virtuale e installa le dipendenze:
```bash
    python -m venv env
    source env/bin/activate
    pip install -r requirements.txt
```

3. Configura variabili in `.env.local` 

4. Esegui il server:

```bash
   python manage.py runserver
```

---

## 📁 Struttura del progetto

```
DriveIsland/
├── cars/
├── bookings/
├── users/
├── contact/
├── pages/
├── templates/
├── static/
├── media/
├── logs/
├── manage.py
├── .env
├── .env.local
└── requirements.txt
```

---

## 🔐 Accesso amministratore

Per accedere come amministratore, usa le seguenti credenziali effettuando il login normalmente nel sito

```
Username: amministratore
Password: ciao1234
```
---

## 📄 Licenza

Questo progetto è stato realizzato per l’esercitazione PPM 2025 (Università di Firenze).