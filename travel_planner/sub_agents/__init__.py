"""
Package des sous-agents du Travel Planner.

Expose les quatre agents spécialisés utilisés par le travel_coordinator :
- transport_search_agent : recherche de vols, trains et bus
- hotel_search_agent     : recherche d'hébergements
- activity_search_agent  : suggestions d'activités et restaurants
- itinerary_planner_agent: génération d'itinéraire jour par jour
"""

from .transport_search import transport_search_agent
from .hotel_search import hotel_search_agent
from .activity_search import activity_search_agent
from .itinerary_planner import itinerary_planner_agent

__all__ = [
    "transport_search_agent",
    "hotel_search_agent",
    "activity_search_agent",
    "itinerary_planner_agent",
]
