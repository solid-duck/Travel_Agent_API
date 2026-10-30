from langchain_core.tools import tool
from app.flights_finder import flights_finder


DESTINATIONS = {
    'roma': {'country': 'Italia', 'period': 'aprile-giugno e settembre-ottobre'},
    'parigi': {'country': 'Francia', 'period': 'aprile-giugno e settembre-ottobre'},
    'londra': {'country': 'Regno Unito', 'period': 'maggio-settembre'},
}


@tool
def get_destination_info(destination: str) -> str:
    """Restituisce informazioni di base su una destinazione."""
    print(f'[TRACE] get_destination_info: {destination}')
    info = DESTINATIONS.get(destination.strip().lower())
    if info is None:
        return f'Non ho informazioni locali su {destination}.'
    return (
        f"{destination.title()} si trova in {info['country']}. "
        f"Il periodo consigliato è {info['period']}."
    )


@tool
def calculate_trip_budget(days: int, daily_budget: float, travellers: int = 1) -> str:
    """Calcola una stima del budget, esclusi i voli."""
    print(f'[TRACE] calculate_trip_budget: days={days}, budget={daily_budget}, travellers={travellers}')
    if days <= 0 or daily_budget < 0 or travellers <= 0:
        return 'Giorni, viaggiatori e budget devono avere valori validi.'
    total = days * daily_budget * travellers
    return f'Budget stimato: {total:.2f} euro, esclusi i voli.'


TRAVEL_TOOLS = [get_destination_info, calculate_trip_budget, flights_finder]
