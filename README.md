# DriveIsland – Piattaforma di Noleggio Auto Online

**DriveIsland** è un'applicazione web per la gestione e il noleggio online di automobili. Sviluppata con Django e
deployata su Render, offre un'esperienza completa sia per clienti che per amministratori, con funzionalità di
prenotazione, pagamento, gestione flotte e assistenza integrata.

🔗 **Link**: [https://driveisland.onrender.com/](https://driveisland.onrender.com/)

---

## 📦 Funzionalità principali

### 👤 Clienti

Gli utenti registrati appartenenti al gruppo "clienti" possono accedere alle seguenti funzionalità:

- **Registrazione con conferma email**:
    - Al momento della registrazione, viene inviata automaticamente un'email con un link di attivazione per convalidare
      l’account.

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
    - Le prenotazioni attive, future o passate sono visibili in una dashboard personale, con dettagli completi e stato
      aggiornato.

- **Ricerca avanzata delle auto**:
    - Funzionalità di ricerca e filtro per categoria, disponibilità, caratteristiche (carburante, cambio, aria
      condizionata, ecc.).

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

Gli amministratori hanno **tutti i permessi dei clienti**, con funzionalità avanzate per la gestione completa della
piattaforma:

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

| App        | Descrizione                                    |
|------------|------------------------------------------------|
| `users`    | Gestione utenti, registrazione, profilo, login |
| `cars`     | Catalogo e gestione veicoli                    |
| `bookings` | Prenotazioni e gestione pagamenti              |
| `contact`  | Modulo assistenza e sistema messaggistica      |
| `pages`    | Homepage, pagine informative e navigazione     |

**User Model** esteso e personalizzato.

---

## 🔐 Gruppi e permessi

- `Clienti`: assegnati automaticamente alla registrazione
- `Amministratori`: accesso avanzato al backend e gestione

---

## ⚙️ Setup locale

Questi sono i passaggi per configurare l'ambiente locale e avviare il progetto **DriveIsland**.

### 1. Clona il repository:

Per prima cosa, clona il repository del progetto sul tuo computer:

  ```bash
      git clone https://github.com/tuo-utente/driveisland.git
      cd driveisland
  ```
### 2. Crea ambiente virtuale e installa le dipendenze:

Crea un ambiente virtuale e installa le dipendenze necessarie:

```bash
    python -m venv venv
    source venv\Scripts\activate
    pip install -r requirements.txt
```
  
### 3. Configura variabili in `.env.local`
Crea il file .env.local nella radice del progetto.
All'interno di questo file, aggiungi le seguenti variabili:

```bash
  echo DEBUG=True > .env.local
  
  echo ALLOWED_HOSTS=127.0.0.1,localhost >> .env.local
  echo SITE_DOMAIN=127.0.0.1:8000 >> .env.local
  
  echo DATABASE_URL=sqlite:///db.sqlite3 >> .env.local
```

 **Django Secret Key**: Puoi generare una nuova chiave segreta per Django eseguendo il seguente comando:

```bash
  python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```
Copia la chiave segreta generata e inseriscila manualmente nel file .env.local:

```
DJANGO_SECRET_KEY=la_tua_chiave_segreta
```
Aggiungi manualmente anche le altre variabili necessarie per la configurazione del progetto nel file .env.local.
```
EMAIL_HOST_USER=la_tua_email@gmail.com >> .env.local
EMAIL_HOST_PASSWORD=password_fornita_da gmail (diversa dalla password personale) >> .env.local

STRIPE_SECRET_KEY=
STRIPE_PUBLIC_KEY=

CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET
```
Reperibili registrandosi rispettivamente sui siti ufficiali di Gmail, Stripe e Cloudinary.
### 4. Esegui il server:

```bash
  python manage.py runserver
```

Il progetto sarà accessibile all'indirizzo: http://127.0.0.1:8000/.

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

## 📌 Nota
Il file .env.local sarà fornito direttamente al professore simone ricci via email, in data 10/07/2025

---

## 📄 Licenza

Questo progetto è stato realizzato per l’esercitazione PPM 2025 (Università di Firenze).