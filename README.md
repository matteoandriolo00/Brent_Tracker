# Brent Tracker

Backend REST per il il monitoraggio del prezzo del petrolio Brent.

Il progetto espone API REST e può essere testato direttamente tramite **Swagger UI**.
**Non è presente un frontend dedicato.**

## Requisiti

* [Docker](https://www.docker.com/)

## Avvio dell'applicazione

Per avviare il backend, eseguire il seguente comando da terminale:

```bash
docker run -p 8000:8000 matteoandriolo00/brent-tracker:latest
```

Il container avvierà l'applicazione sulla porta `8000`.

## Utilizzo tramite Swagger

Una volta avviato il backend, aprire il seguente indirizzo nel browser:

http://127.0.0.1:8000/docs

Si aprirà **Swagger UI**, attraverso cui è possibile visualizzare e provare direttamente tutti gli endpoint disponibili.

## Funzionalità principali

Il backend permette di:

* registrare nuovi utenti;
* effettuare il login;
* ottenere l'ultimo prezzo disponibile del Brent;
* consultare lo storico dei prezzi del Brent.

Tutte le funzionalità possono essere testate tramite le API documentate in Swagger.
