"""
Tool de recherche de vols réels basé sur l'API Aviationstack (gratuit).
Nécessite la clé API dans AVIATIONSTACK_API_KEY.
"""

import os
import requests

AVIATIONSTACK_URL = "http://api.aviationstack.com/v1/flights"

def search_real_flights(
    origin_iata: str,
    destination_iata: str,
    departure_date: str = None,
    limit: int = 10
) -> dict:
    """
    Recherche de vrais vols et horaires en utilisant l'API Aviationstack.
    
    Args:
        origin_iata: Code IATA de l'aéroport de départ (ex: "CDG", "JFK", "YUL").
        destination_iata: Code IATA de l'aéroport d'arrivée (ex: "HND", "LHR", "FCO").
        departure_date: (Optionnel) Date au format YYYY-MM-DD. N'est pas strict pour Aviationstack.
        limit: Nombre maximal de vols à retourner (défaut: 10).

    Returns:
        Un dictionnaire contenant les vols trouvés (compagnies, statuts, horaires),
        ou un message d'erreur clair.
    """
    api_key = os.getenv("AVIATIONSTACK_API_KEY", "")
    if not api_key:
        return {
            "error": "Clé API Aviationstack manquante. L'utilisateur doit configurer AVIATIONSTACK_API_KEY dans le .env."
        }

    try:
        # Construction des paramètres de recherche
        params = {
            'access_key': api_key,
            'dep_iata': origin_iata.upper(),
            'arr_iata': destination_iata.upper(),
            'limit': min(limit, 20)
        }

        # L'API gratuite ne permet pas de filtrer proprement par date future (historique/temps réel).
        # Mais l'agent peut comprendre la structure de la route.
        response = requests.get(AVIATIONSTACK_URL, params=params, timeout=15)
        response.raise_for_status()
        
        data = response.json()
        
        if "error" in data:
            return {"error": f"Erreur API Aviationstack: {data['error'].get('info', 'Erreur inconnue')}"}

        flights = data.get("data", [])

        if not flights:
            return {
                "message": f"Aucun vol direct actif trouvé entre {origin_iata} et {destination_iata}.",
                "flights": []
            }

        parsed_flights = []
        for flight in flights:
            airline = flight.get("airline", {}).get("name", "Inconnue")
            flight_number = flight.get("flight", {}).get("iata", "N/A")
            
            dep = flight.get("departure", {})
            arr = flight.get("arrival", {})
            
            parsed_flights.append({
                "airline": airline,
                "flight_number": flight_number,
                "status": flight.get("flight_status", "scheduled"),
                "departure": {
                    "airport": dep.get("airport"),
                    "terminal": dep.get("terminal", "N/A"),
                    "scheduled_time": dep.get("scheduled", "")
                },
                "arrival": {
                    "airport": arr.get("airport"),
                    "terminal": arr.get("terminal", "N/A"),
                    "scheduled_time": arr.get("scheduled", "")
                }
            })

        return {
            "source": "Aviationstack API",
            "origin": origin_iata,
            "destination": destination_iata,
            "total_found": len(parsed_flights),
            "flights": parsed_flights,
            "note_to_agent": "Utilisez ces vraies compagnies aériennes et routes pour construire l'itinéraire du voyageur."
        }

    except requests.RequestException as e:
        return {"error": f"Erreur de réseau Aviationstack: {str(e)}"}
    except Exception as e:
        return {"error": f"Erreur inattendue: {str(e)}"}
