# Travel Agent API

Progetto didattico in Python con FastAPI e LangChain per creare un semplice assistente di viaggio.

## Struttura

- `app/main.py`: endpoint FastAPI;
- `app/agent.py`: modello, prompt e agente LangChain;
- `app/tools.py`: tool di viaggio;
- `app/schemas.py`: validazione delle richieste;
- `.env`: configurazione locale, esclusa da Git.

## Avvio da Visual Studio Code

Aprire questa cartella in VS Code:

```text
C:\Users\utente\hack187\Python\Progetti\travel-agent-api
```

Nel terminale PowerShell di VS Code eseguire:

```powershell
.\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload
```

Aprire `http://127.0.0.1:8000/docs`.

## Endpoint disponibili

`GET /health` verifica che il server sia attivo.

`POST /chat` riceve una domanda nel formato:

```json
{"question": "Qual è il periodo migliore per visitare Roma?"}
```

## Tracing

Il progetto usa messaggi `print` con prefisso `[TRACE]` per rendere visibili ricezione della richiesta, creazione dell'agente e chiamata dei tool.

## Nota di sicurezza

Non pubblicare mai `.env` su GitHub. Il repository deve contenere solo `.env.example`; le chiavi reali restano nella macchina locale.

## Tool `flights_finder`

Il tool usa SerpApi con il motore `google_flights`. I parametri obbligatori sono `departure_airport`, `arrival_airport` e `outbound_date`; `return_date` è opzionale. Se manca `return_date`, viene cercata una tratta di sola andata. I codici aeroporto devono essere IATA di tre lettere e la data deve essere nel formato `YYYY-MM-DD`.

Esempio di domanda per l'agente:

```text
Trova un volo da FCO a JFK per il 15 dicembre 2026.
```

Se SerpApi restituisce `Invalid API key`, il codice e i parametri sono corretti ma la variabile `SERPAPI_API_KEY` nel file `.env` deve essere sostituita con una chiave SerpApi attiva.

## Test manuali

Per controllare solo la validazione dei parametri:

```powershell
python -c "from app.flights_finder import flights_finder; print(flights_finder.invoke({'departure_airport':'FCO','arrival_airport':'JFK','outbound_date':'2026-12-15'}))"
```

Per controllare l'API completa:

```powershell
python -m uvicorn app.main:app --reload
```

Poi usare la pagina `http://127.0.0.1:8000/docs` e provare prima `GET /health`, quindi `POST /chat`.
