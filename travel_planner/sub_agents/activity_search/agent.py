"""Agent activity_search — suggestions d'activités via OpenTripMap + Google Search."""

from google.adk import Agent
from google.adk.tools import google_search

from . import prompt
from travel_planner.config import MODEL

activity_search_agent = Agent(
    model=MODEL,
    name="activity_search_agent",
    instruction=prompt.ACTIVITY_SEARCH_PROMPT,
    output_key="activity_search_output",
    tools=[
        google_search,       # Recherche des activités, descriptions et tarifications
    ],
)
