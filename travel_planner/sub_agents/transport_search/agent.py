"""Agent flight_search pour rechercher des vols via Google Search"""

import os

from google.adk import Agent
from google.adk.tools import google_search

from . import prompt

MODEL = os.getenv("GOOGLE_MODEL", "gemini-2.5-flash-lite")

flight_search_agent = Agent(
    model=MODEL,
    name="flight_search_agent",
    instruction=prompt.FLIGHT_SEARCH_PROMPT,
    output_key="flight_search_output",
    tools=[google_search],
)
