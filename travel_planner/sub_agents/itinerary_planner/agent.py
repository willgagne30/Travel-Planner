"""Agent itinerary_planner — génère un itinéraire structuré avec météo et devises."""

from google.adk import Agent

from . import prompt
from travel_planner.config import MODEL
from travel_planner.tools.weather import get_weather_forecast
from travel_planner.tools.currency import convert_currency, get_exchange_rate
from travel_planner.tools.geocoding import get_country_info



itinerary_planner_agent = Agent(
    model=MODEL,
    name="itinerary_planner_agent",
    instruction=prompt.ITINERARY_PLANNER_PROMPT,
    output_key="itinerary_plan_output",
    tools=[
        get_weather_forecast,  # Météo prévue pour adapter l'itinéraire au temps
        get_exchange_rate,     # Taux de change pour le résumé budgétaire
        convert_currency,      # Convertir le budget total dans la devise locale
        get_country_info,      # Infos pratiques sur le pays (langue, fuseau, etc.)
    ],
)
