# DriveIsland – Piattaforma di Noleggio Auto Online

**DriveIsland** è un'applicazione web per la gestione e il noleggio online di automobili. Sviluppata con Django e deployata su Render, offre un'esperienza completa sia per clienti che per amministratori, con funzionalità di prenotazione, pagamento, gestione flotte e assistenza integrata.

🔗 **Live demo**: [https://driveisland.onrender.com/](https://driveisland.onrender.com/)

---

## 📦 Funzionalità principali

### 👤 Clienti
- Registrazione con conferma email automatica
- Prenotazione auto con pagamento online (Stripe)
- Annullamento prenotazioni
- Gestione del profilo (modifica/cancellazione)
- Visualizzazione prenotazioni personali nella dashboard
- Ricerca avanzata delle auto per categoria, disponibilità, ecc.
- Richiesta assistenza tramite modulo + risposta via email

💳 Test pagamento (Stripe):
```
Carta: 4242 4242 4242 4242
Scadenza: qualsiasi data futura
CVV: qualsiasi
```

---

### 🛠️ Amministratori
Tutti i permessi cliente, **più**:
- Gestione completa prenotazioni (visualizza, filtra, cancella con notifica via email)
- Gestione richieste di assistenza (filtri, risposta via email)
- CRUD completo delle auto: aggiunta, modifica, eliminazione
- Gestione attributi: modello, categoria, colore, aria condizionata, immagini, sconti

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

3. Configura variabili in `.env` oppure `.env.local` (già presenti)

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

## 📫 Credenziali demo

Puoi effettuare il login come amministratore demo con le credenziali fornite separatamente dal docente o dal repository protetto.

---

## ✅ Requisiti soddisfatti

✔️ 5 app Django  
✔️ 2+ relazioni tra modelli  
✔️ Class-Based Views  
✔️ Permessi separati per gruppi  
✔️ User esteso e personalizzato  
✔️ Deploy su Render

---

## 📄 Licenza

Questo progetto è stato realizzato per l’esercitazione PPM 2025 (Università di Firenze).

Contatto docente: **simone.ricci@unifi.it**