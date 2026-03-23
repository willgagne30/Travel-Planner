"""Agent activity_search — suggestions d'activités via OpenTripMap + Google Search."""

import os

from google.adk import Agent
from google.adk.tools import google_search

from . import prompt

MODEL = os.getenv("GOOGLE_MODEL", "gemini-2.5-pro")

activity_search_agent = Agent(
    model=MODEL,
    name="activity_search_agent",
    instruction=prompt.ACTIVITY_SEARCH_PROMPT,
    output_key="activity_search_output",
    tools=[
        google_search,       # Recherche des activités, descriptions et tarifications
    ],
)
