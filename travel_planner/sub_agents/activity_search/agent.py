"""Agent activity_search — suggestions d'activités via OpenTripMap + Google Search."""

import os

from google.adk import Agent
from google.adk.tools import google_search

from . import prompt
from travel_planner.tools.geocoding import geocode_city
from travel_planner.tools.activities import search_attractions, search_restaurants

MODEL = os.getenv("GOOGLE_MODEL", "gemini-2.5-pro")

activity_search_agent = Agent(
    model=MODEL,
    name="activity_search_agent",
    instruction=prompt.ACTIVITY_SEARCH_PROMPT,
    output_key="activity_search_output",
    tools=[
        search_attractions,  # POI, musées, monuments via OpenTripMap (gratuit)
        search_restaurants,  # Restaurants et cafés à proximité via OpenTripMap
        geocode_city,        # Obtenir les coordonnées GPS de la destination
        google_search,       # Compléter avec des recherches web sur les activités
    ],
)
