"""Agent hotel_photo_agent — enrichit le rapport d'hébergement avec de vraies photos Google Places."""

import os

from google.adk import Agent

from travel_planner.tools.places import get_hotel_image_url

from . import prompt

MODEL = os.getenv("GOOGLE_MODEL", "gemini-2.5-flash")

hotel_photo_agent = Agent(
    model=MODEL,
    name="hotel_photo_agent",
    instruction=prompt.HOTEL_PHOTO_PROMPT,
    output_key="hotel_photo_output",
    tools=[
        get_hotel_image_url,   # SEUL outil autorisé : Google Places (pas de conflit d'API)
    ],
)
