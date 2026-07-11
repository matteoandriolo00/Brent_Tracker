# Brent Tracker

Brent Tracker è un progetto semplice per monitorare il prezzo del petrolio Brent tramite un’API FastAPI. L’idea è dividere chiaramente le responsabilità tra:

- API: riceve le richieste HTTP
- servizi: contiene la logica di business
- repository: gestisce i dati
- modelli: descrive le tabelle del database
- database: gestisce la connessione SQLite

## Struttura del progetto

```text
app/
├── api/              # endpoint FastAPI
├── core/             # connessione al database e utility condivise
├── models/           # classi ORM che rappresentano le tabelle
├── repositories/     # accesso ai dati
├── schemas/          # modelli di input/output Pydantic
├── services/         # logica applicativa
main.py              # punto di ingresso dell’applicazione
``` 

## Come è organizzato il flusso dei dati

Il flusso principale è questo:

1. Un client chiama un endpoint in [app/api](app/api)
2. L’endpoint usa un servizio in [app/services](app/services)
3. Il servizio usa il repository in [app/repositories](app/repositories)
4. Il repository legge o scrive nel database tramite [app/core/database.py](app/core/database.py)
5. Il risultato torna indietro fino all’API e quindi al client

## Componenti principali

### 1. Entry point: main.py
Il file [main.py](main.py) crea l’app FastAPI, registra i router e prepara il database.

Funzionamento:
- crea l’istanza di FastAPI
- include i router di prezzi, autenticazione e alert
- crea le tabelle del database all’avvio

### 2. API
La cartella [app/api](app/api) contiene gli endpoint HTTP.

#### [app/api/prices.py](app/api/prices.py)
Gestisce le richieste sui prezzi Brent:
- GET /prices/current: recupera il prezzo corrente dal provider esterno, lo salva e lo restituisce
- GET /prices/history: restituisce lo storico dei prezzi salvati

#### [app/api/auth.py](app/api/auth.py)
Gestisce autenticazione e registrazione:
- POST /auth/register: registra un nuovo utente
- POST /auth/login: controlla email e password e restituisce un token fittizio

#### [app/api/alert.py](app/api/alert.py)
Gestisce gli alert:
- POST /alerts/: crea un nuovo alert
- GET /alerts/{user_id}: visualizza gli alert di un utente
- PATCH /alerts/{alert_id}/status: cambia stato dell’alert
- DELETE /alerts/{alert_id}: elimina un alert

### 3. Servizi
I servizi contengono la logica di business.

#### [app/services/price_service.py](app/services/price_service.py)
Questa classe coordina il flusso dei prezzi.

Metodi:
- update_and_get_price():
  - chiama BrentService per recuperare il prezzo corrente
  - salva il valore nel database tramite il repository
  - controlla gli alert tramite check_and_trigger_alerts
  - restituisce il record salvato
- get_price_history():
  - richiede lo storico dei prezzi al repository

#### [app/services/brent_service.py](app/services/brent_service.py)
Questa classe si occupa solo della comunicazione con l’API esterna di Yahoo Finance.

Funzione:
- fetch_current_price(): fa una richiesta HTTP e restituisce il prezzo corrente

#### [app/services/auth_service.py](app/services/auth_service.py)
Questa classe gestisce la registrazione e il login degli utenti.

Metodi:
- get_password_hash(): genera l’hash bcrypt della password
- verify_password(): verifica una password in chiaro contro l’hash
- register_user(): controlla che l’email non esista, crea l’hash e salva l’utente
- authenticate_user(): verifica email e password per il login

#### [app/services/alert_service.py](app/services/alert_service.py)
Questa funzione aggiorna lo stato degli alert quando il prezzo raggiunge una soglia.

Logica:
- se l’alert è di tipo BELOW e il prezzo corrente è minore o uguale alla soglia, lo imposta a TRIGGERED
- se l’alert è di tipo ABOVE e il prezzo corrente è maggiore o uguale alla soglia, lo imposta a TRIGGERED

### 4. Repository
I repository separano la logica di accesso ai dati dall’applicazione.

#### [app/repositories/price_repo.py](app/repositories/price_repo.py)
Gestisce il salvataggio e la lettura dello storico dei prezzi:
- save_price(): salva un nuovo prezzo nel DB
- get_history(): recupera tutti i prezzi ordinati dal più recente al più vecchio

#### [app/repositories/user_repo.py](app/repositories/user_repo.py)
Gestisce gli utenti:
- get_user_by_email(): cerca un utente per email
- get_user_by_username(): cerca un utente per username
- create_user(): salva un nuovo utente

### 5. Modelli
I modelli rappresentano le tabelle del database.

#### [app/models/brent.py](app/models/brent.py)
Rappresenta la tabella brent_values:
- id
- value
- timestamp

#### [app/models/user.py](app/models/user.py)
Rappresenta la tabella users:
- id
- username
- email
- password

#### [app/models/alert.py](app/models/alert.py)
Rappresenta la tabella alerts:
- id
- user_id
- target_price
- direction
- status

### 6. Database
Il cuore della persistenza è [app/core/database.py](app/core/database.py).

Qui avviene:
- connessione a SQLite tramite SQLAlchemy
- creazione della sessione per ogni richiesta
- chiusura della sessione alla fine

## Percorsi principali dei dati

### Registrazione utente
```text
Client -> /auth/register -> AuthService -> UserRepository -> SQLite
```

### Login
```text
Client -> /auth/login -> AuthService -> UserRepository -> SQLite
```

### Recupero prezzo corrente
```text
Client -> /prices/current -> PriceService -> BrentService -> Yahoo Finance
                                      \-> PriceRepository -> SQLite
                                      \-> AlertService -> SQLite
```

### Storico prezzi
```text
Client -> /prices/history -> PriceService -> PriceRepository -> SQLite
```

### Gestione alert
```text
Client -> /alerts/... -> API alert -> SQLite
```

## Mini mappa delle dipendenze

```text
Client
  │
  ▼
FastAPI routes (app/api)
  │
  ├── prices.py ──> PriceService ──> BrentService
  │                          │
  │                          ├── PriceRepository ──> BrentValue (DB)
  │                          └── check_and_trigger_alerts ──> Alert (DB)
  │
  ├── auth.py ─────> AuthService ──> UserRepository ──> User (DB)
  │
  └── alert.py ─────> Alert model / DB queries

Database
  ├── users
  ├── brent_values
  └── alerts
```

## Nota di progettazione

La struttura è pensata per separare bene i compiti:
- l’API riceve richieste
- i servizi contengono la logica
- i repository gestiscono il database
- i modelli descrivono i dati

Questa separazione rende il codice più ordinato, più facile da estendere e più semplice da testare.
