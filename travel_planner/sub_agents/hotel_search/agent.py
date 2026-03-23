"""Agent hotel_search — recherche d'hébergements via Google Search + géocodage."""

import os

from google.adk import Agent

from travel_planner.tools.places import get_hotel_image_url
from travel_planner.tools.web_search import web_search

from . import prompt

MODEL = os.getenv("GOOGLE_MODEL", "gemini-2.5-flash")

hotel_search_agent = Agent(
    model=MODEL,
    name="hotel_search_agent",
    instruction=prompt.HOTEL_SEARCH_PROMPT,
    output_key="hotel_search_output",
    tools=[
        web_search,          # Alternative Python à google_search pour éviter l'erreur 400
        get_hotel_image_url, # Récupération de la *véritable* photo de l'hôtel
    ],
)
