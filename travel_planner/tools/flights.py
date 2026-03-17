"""
Tool de recherche de vols réels basé sur l'API Amadeus for Developers (gratuit).
Nécessite le package 'amadeus' et les clés API dans AMADEUS_API_KEY et AMADEUS_API_SECRET.
"""

import os
from amadeus import Client, ResponseError

def get_amadeus_client():
    """Initialise le client Amadeus avec les clés du .env"""
    api_key = os.getenv("AMADEUS_API_KEY", "")
    api_secret = os.getenv("AMADEUS_API_SECRET", "")
    
    if not api_key or not api_secret:
        return None
        
    return Client(
        client_id=api_key,
        client_secret=api_secret,
        hostname='test' # Utilise l'environnement de test gratuit d'Amadeus
    )

def search_real_flights(
    origin_iata: str,
    destination_iata: str,
    departure_date: str,
    return_date: str = None,
    adults: int = 1,
    max_results: int = 5
) -> dict:
    """
    Recherche de vrais vols avec horaires et prix en utilisant l'API Amadeus.
    
    Args:
        origin_iata: Code IATA de l'aéroport de départ (ex: "CDG", "JFK", "YUL").
        destination_iata: Code IATA de l'aéroport d'arrivée (ex: "HND", "LHR", "FCO").
        departure_date: Date de départ au format YYYY-MM-DD (ex: "2024-11-15").
        return_date: (Optionnel) Date de retour au format YYYY-MM-DD. Si None, recherche un aller-simple.
        adults: Nombre de passagers adultes (défaut: 1).
        max_results: Nombre maximal d'itinéraires à retourner (défaut: 5).

    Returns:
        Un dictionnaire contenant les meilleures offres de vols trouvées (prix, compagnies, horaires),
        ou un message d'erreur clair.
    """
    client = get_amadeus_client()
    if not client:
        return {
            "error": "Clés API Amadeus manquantes. L'utilisateur doit configurer AMADEUS_API_KEY et AMADEUS_API_SECRET."
        }

    try:
        # Construction des paramètres de recherche
        params = {
            'originLocationCode': origin_iata.upper(),
            'destinationLocationCode': destination_iata.upper(),
            'departureDate': departure_date,
            'adults': adults,
            'max': min(max_results, 10),
            'currencyCode': 'EUR'
        }
        
        if return_date:
            params['returnDate'] = return_date

        # Appel à l'API Amadeus Flight Offers Search
        response = client.shopping.flight_offers_search.get(**params)
        offers = response.data

        if not offers:
            return {
                "message": f"Aucun vol trouvé entre {origin_iata} et {destination_iata} "
                           f"pour le(s) date(s) indiquée(s).",
                "flights": []
            }

        parsed_flights = []
        for offer in offers:
            # Prix total
            price = offer.get("price", {}).get("total", "N/A")
            currency = offer.get("price", {}).get("currency", "")
            
            # Parcours des séquences de vol (Aller, puis Retour)
            itineraries = []
            for itinerary in offer.get("itineraries", []):
                segments = itinerary.get("segments", [])
                
                # Récupérer les infos du premier et dernier segment pour avoir l'horaire global
                first_segment = segments[0]
                last_segment = segments[-1]
                
                departure_time = first_segment.get("departure", {}).get("at", "")
                arrival_time = last_segment.get("arrival", {}).get("at", "")
                
                # Liste des compagnies aériennes (codes)
                carriers = [seg.get("carrierCode", "") for seg in segments]
                carriers = list(dict.fromkeys(carriers)) # Dédupliquer
                
                stops = len(segments) - 1
                
                itineraries.append({
                    "duration": itinerary.get("duration", "").replace("PT", ""),
                    "departure": departure_time,
                    "arrival": arrival_time,
                    "stops": stops,
                    "airlines": carriers
                })

            # Format final pour cette offre
            parsed_flights.append({
                "price": f"{price} {currency}",
                "outbound_flight": itineraries[0] if len(itineraries) > 0 else None,
                "return_flight": itineraries[1] if len(itineraries) > 1 else None,
                "bookable_seats": offer.get("numberOfBookableSeats", "N/A")
            })

        return {
            "source": "Amadeus Flight API (Temps réel)",
            "origin": origin_iata,
            "destination": destination_iata,
            "passengers": adults,
            "flights": parsed_flights
        }

    except ResponseError as error:
        return {"error": f"Erreur de recherche Amadeus: {str(error)}"}
    except Exception as e:
        return {"error": f"Erreur inattendue: {str(e)}"}
