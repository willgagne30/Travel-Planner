"""Agent itinerary_planner pour générer un itinéraire de voyage structuré"""

import os

from google.adk import Agent

from . import prompt

MODEL = os.getenv("GOOGLE_MODEL", "gemini-2.5-pro")

itinerary_planner_agent = Agent(
    model=MODEL,
    name="itinerary_planner_agent",
    instruction=prompt.ITINERARY_PLANNER_PROMPT,
    output_key="itinerary_plan_output",
)
