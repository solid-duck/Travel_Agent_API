import json
import os
from datetime import date
from typing import Optional

from dotenv import load_dotenv
from langchain_core.tools import tool
from pydantic import BaseModel, Field, field_validator
from serpapi import GoogleSearch

load_dotenv()


class FlightsInputSchema(BaseModel):
    departure_airport: str = Field(description='Codice IATA dell aeroporto di partenza, ad esempio FCO.')
    arrival_airport: str = Field(description='Codice IATA dell aeroporto di arrivo, ad esempio JFK.')
    outbound_date: str = Field(description='Data di partenza nel formato YYYY-MM-DD.')
    return_date: Optional[str] = Field(default=None, description='Data di ritorno nel formato YYYY-MM-DD, opzionale.')

    @field_validator('departure_airport', 'arrival_airport')
    @classmethod
    def validate_airport_code(cls, value: str) -> str:
        code = value.strip().upper()
        if len(code) != 3 or not code.isalpha():
            raise ValueError('Il codice aeroporto deve essere di 3 lettere, ad esempio FCO.')
        return code

    @field_validator('outbound_date', 'return_date')
    @classmethod
    def validate_date(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        try:
            date.fromisoformat(value)
        except ValueError as error:
            raise ValueError('La data deve avere il formato YYYY-MM-DD.') from error
        return value


@tool(args_schema=FlightsInputSchema)
def flights_finder(
    departure_airport: str,
    arrival_airport: str,
    outbound_date: str,
    return_date: Optional[str] = None,
) -> str:
    """Cerca voli con Google Flights tramite SerpApi."""
    departure_airport = departure_airport.strip().upper()
    arrival_airport = arrival_airport.strip().upper()
    print(
        f'[TRACE] flights_finder: {departure_airport} -> {arrival_airport}, '
        f'data={outbound_date}, ritorno={return_date or "non indicato"}'
    )

    api_key = os.getenv('SERPAPI_API_KEY')
    if not api_key or api_key.startswith('YOUR_'):
        return 'SERPAPI_API_KEY non configurata nel file .env.'

    params = {
        'engine': 'google_flights',
        'departure_id': departure_airport,
        'arrival_id': arrival_airport,
        'outbound_date': outbound_date,
        'type': 1 if return_date else 2,
        'api_key': api_key,
        'hl': 'it',
        'currency': 'EUR',
    }
    if return_date:
        params['return_date'] = return_date

    try:
        results = GoogleSearch(params).get_dict()
    except Exception as error:
        print(f'[TRACE] Errore SerpApi: {error}')
        return 'Non è stato possibile contattare il servizio di ricerca voli.'

    if results.get('error'):
        print(f"[TRACE] Errore restituito da SerpApi: {results['error']}")
        return 'SerpApi ha restituito un errore durante la ricerca dei voli.'

    best_flights = results.get('best_flights', [])
    if not best_flights:
        return 'Nessun volo trovato per i parametri specificati.'

    print(f'[TRACE] flights_finder: trovate {len(best_flights)} opzioni')
    return json.dumps(best_flights[:3], ensure_ascii=False, indent=2)
