"""Agent transport_search — recherche de transports via Google Search + géocodage."""

import os

from google.adk import Agent
from google.adk.tools import google_search

from . import prompt
from travel_planner.tools.geocoding import geocode_city, get_country_info

MODEL = os.getenv("GOOGLE_MODEL", "gemini-2.5-flash-lite")

transport_search_agent = Agent(
    model=MODEL,
    name="transport_search_agent",
    instruction=prompt.TRANSPORT_SEARCH_PROMPT,
    output_key="transport_search_output",
    tools=[
        google_search,       # Recherche de vols, trains et bus en temps réel
        geocode_city,        # Coordonnées GPS des villes de départ/arrivée
        get_country_info,    # Infos sur le pays de destination (visa, monnaie, etc.)
    ],
)
