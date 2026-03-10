"""Coordinateur de voyage : planifier des voyages complets et personnalisés."""

import os

from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

from . import prompt
from .sub_agents.flight_search import flight_search_agent
from .sub_agents.hotel_search import hotel_search_agent
from .sub_agents.activity_search import activity_search_agent
from .sub_agents.itinerary_planner import itinerary_planner_agent

MODEL = os.getenv("GOOGLE_MODEL", "gemini-2.5-pro")


travel_coordinator = LlmAgent(
    name="travel_coordinator",
    model=MODEL,
    description=(
        "guider les utilisateurs à travers un processus structuré pour planifier "
        "un voyage complet en orchestrant une série de sous-agents experts. les aider à "
        "rechercher des vols, trouver des hébergements, découvrir des activités, "
        "et générer un itinéraire jour par jour personnalisé."
    ),
    instruction=prompt.TRAVEL_COORDINATOR_PROMPT,
    output_key="travel_coordinator_output",
    tools=[
        AgentTool(agent=flight_search_agent),
        AgentTool(agent=hotel_search_agent),
        AgentTool(agent=activity_search_agent),
        AgentTool(agent=itinerary_planner_agent),
    ],
)

root_agent = travel_coordinator
