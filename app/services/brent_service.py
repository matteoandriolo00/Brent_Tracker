import requests

class BrentService:
    """
    Gestisce esclusivamente la comunicazione di rete con l'API esterna.
    Utilizza l'API pubblica di Yahoo Finance per ottenere in tempo reale
    la quotazione del petrolio Brent (Ticker: BZ=F).
    """
    
    def __init__(self):
        """
        Inizializza il servizio configurando l'URL dell'API di Yahoo Finance.
        Viene impostato un header 'User-Agent' simulato per evitare che 
        i sistemi anti-bot del provider blocchino la connessione.
        """
        self.api_url = "https://query1.finance.yahoo.com/v8/finance/chart/BZ=F"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, come Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def fetch_current_price(self) -> float:
        """
        Effettua una richiesta HTTP GET all'API esterna, naviga la struttura
        della risposta JSON per estrarre il prezzo di mercato corrente 
        e lo restituisce come numero decimale (float).
        """
        try:
            response = requests.get(self.api_url, headers=self.headers)
            response.raise_for_status()  # Lancia un'eccezione se la risposta HTTP non è 200 (OK)
            
            data = response.json()
            
            # Estraiamo il prezzo specifico navigando i dizionari annidati restituiti da Yahoo
            current_price = data['chart']['result'][0]['meta']['regularMarketPrice']
            
            return float(current_price)
            
        except requests.RequestException as e:
            # RNF5: Affidabilità. Gestiamo la mancata connessione.
            print(f"Errore di comunicazione con l'API esterna: {e}")
            raise Exception("Impossibile recuperare il prezzo del Brent: errore di rete.")
            
        except (KeyError, IndexError, TypeError) as e:
            # Gestiamo il caso in cui Yahoo modifichi la struttura della sua API
            print(f"Errore durante l'estrazione dei dati JSON: {e}")
            raise Exception("Impossibile leggere i dati forniti dal provider esterno.")