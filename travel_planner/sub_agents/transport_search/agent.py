"""Agent transport_search — recherche de transports via Google Search + géocodage."""

from google.adk import Agent
from google.adk.tools import google_search

from . import prompt
from travel_planner.config import MODEL

transport_search_agent = Agent(
    model=MODEL,
    name="transport_search_agent",
    instruction=prompt.TRANSPORT_SEARCH_PROMPT,
    output_key="transport_search_output",
    tools=[
        google_search,       # Recherche de vrais vols/trains/bus (prix officiels)
    ],
)
