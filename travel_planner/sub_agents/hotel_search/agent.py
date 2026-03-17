"""Agent hotel_search — recherche d'hébergements via Google Search + géocodage."""

import os

from google.adk import Agent
from google.adk.tools import google_search

from . import prompt
from travel_planner.tools.geocoding import geocode_city
from travel_planner.tools.currency import convert_currency, get_exchange_rate

MODEL = os.getenv("GOOGLE_MODEL", "gemini-2.5-pro")

hotel_search_agent = Agent(
    model=MODEL,
    name="hotel_search_agent",
    instruction=prompt.HOTEL_SEARCH_PROMPT,
    output_key="hotel_search_output",
    tools=[
        google_search,       # Recherche d'hôtels et comparaison de prix
        geocode_city,        # Localiser le quartier/la zone souhaitée
        get_exchange_rate,   # Afficher les prix dans la devise de l'utilisateur
        convert_currency,    # Convertir le budget hébergement dans la devise locale
    ],
)
