"""Agent hotel_search — recherche d'hébergements via Google Search + géocodage."""

import os

from google.adk import Agent
from google.adk.tools import google_search

from . import prompt

MODEL = os.getenv("GOOGLE_MODEL", "gemini-2.5-pro")

hotel_search_agent = Agent(
    model=MODEL,
    name="hotel_search_agent",
    instruction=prompt.HOTEL_SEARCH_PROMPT,
    output_key="hotel_search_output",
    tools=[
        google_search,       # Recherche des hôtels (prix officiels, sites de réservation)
    ],
)
