"""
Tools de recherche d'activités et restaurants basés sur OpenTripMap et Overpass API.
OpenTripMap offre un niveau gratuit généreux (5000 requêtes/jour).
La clé API est configurée dans la variable d'environnement OPENTRIPMAP_API_KEY.
"""

import os
import requests

OPENTRIPMAP_URL = "https://api.opentripmap.com/0.1/en/places"
HEADERS = {"User-Agent": "TravelPlannerAgent/1.0"}

# Mapping des catégories d'intérêts vers les catégories OpenTripMap
INTEREST_TO_KINDS = {
    "culture": "cultural,museums,historic",
    "gastronomie": "foods,restaurants",
    "aventure": "sport,outdoor,natural",
    "nature": "natural,parks,forests",
    "détente": "spas,accomodations",
    "art": "museums,art_galleries",
    "shopping": "shops",
    "architecture": "architecture,historic",
    "default": "interesting_places,cultural,natural",
}


def search_attractions(
    latitude: float,
    longitude: float,
    radius_km: int = 10,
    interests: str = "culture",
    limit: int = 10,
) -> dict:
    """
    Recherche des attractions touristiques, monuments et points d'intérêt
    autour d'une position géographique via OpenTripMap.

    Args:
        latitude: Latitude du centre de recherche (ex: 48.8566 pour Paris).
        longitude: Longitude du centre de recherche (ex: 2.3522 pour Paris).
        radius_km: Rayon de recherche en kilomètres (défaut: 10 km).
        interests: Type d'intérêts séparés par des virgules
                   (ex: "culture,art", "nature,aventure", "gastronomie").
                   Valeurs possibles: culture, gastronomie, aventure, nature, détente, art, shopping, architecture.
        limit: Nombre maximum de résultats à retourner (défaut: 10, max: 20).

    Returns:
        Un dictionnaire contenant une liste d'attractions avec nom, catégorie,
        description et coordonnées, ou un message d'erreur.
    """
    api_key = os.getenv("OPENTRIPMAP_API_KEY", "")
    if not api_key:
        return {
            "error": "Clé API OpenTripMap manquante. Ajoutez OPENTRIPMAP_API_KEY dans le fichier .env. "
                     "Inscription gratuite sur https://opentripmap.io/product"
        }

    # Construire les kinds à partir des intérêts
    kinds_parts = []
    for interest in interests.lower().split(","):
        interest = interest.strip()
        kinds_parts.append(INTEREST_TO_KINDS.get(interest, INTEREST_TO_KINDS["default"]))
    kinds = ",".join(set(",".join(kinds_parts).split(",")))

    try:
        params = {
            "apikey": api_key,
            "radius": radius_km * 1000,  # Conversion en mètres
            "lon": longitude,
            "lat": latitude,
            "kinds": kinds,
            "limit": min(limit, 20),
            "format": "json",
            "rate": 2,  # Filtrer les lieux avec une note minimum de 2
        }
        response = requests.get(
            f"{OPENTRIPMAP_URL}/radius",
            params=params,
            headers=HEADERS,
            timeout=15,
        )
        response.raise_for_status()
        places = response.json()

        if not places:
            return {
                "attractions": [],
                "message": f"Aucune attraction trouvée pour les intérêts '{interests}' dans un rayon de {radius_km} km.",
            }

        attractions = []
        for place in places:
            attractions.append({
                "name": place.get("name", "Sans nom"),
                "categories": place.get("kinds", "").replace(",", ", "),
                "distance_km": round(place.get("dist", 0) / 1000, 2),
                "latitude": place.get("point", {}).get("lat"),
                "longitude": place.get("point", {}).get("lon"),
                "opentripmap_id": place.get("xid", ""),
            })

        return {
            "attractions": attractions,
            "total_found": len(attractions),
            "search_radius_km": radius_km,
            "interests": interests,
        }

    except requests.RequestException as e:
        return {"error": f"Erreur lors de la recherche d'attractions : {str(e)}"}


def search_restaurants(
    latitude: float,
    longitude: float,
    radius_km: int = 3,
    limit: int = 10,
) -> dict:
    """
    Recherche des restaurants et lieux de restauration autour d'une position
    géographique via OpenTripMap.

    Args:
        latitude: Latitude du centre de recherche.
        longitude: Longitude du centre de recherche.
        radius_km: Rayon de recherche en kilomètres (défaut: 3 km).
        limit: Nombre maximum de restaurants à retourner (défaut: 10).

    Returns:
        Un dictionnaire contenant une liste de restaurants avec nom et coordonnées,
        ou un message d'erreur.
    """
    api_key = os.getenv("OPENTRIPMAP_API_KEY", "")
    if not api_key:
        return {
            "error": "Clé API OpenTripMap manquante. Ajoutez OPENTRIPMAP_API_KEY dans le fichier .env."
        }

    try:
        params = {
            "apikey": api_key,
            "radius": radius_km * 1000,
            "lon": longitude,
            "lat": latitude,
            "kinds": "foods,restaurants,fast_food,cafes",
            "limit": min(limit, 20),
            "format": "json",
        }
        response = requests.get(
            f"{OPENTRIPMAP_URL}/radius",
            params=params,
            headers=HEADERS,
            timeout=15,
        )
        response.raise_for_status()
        places = response.json()

        restaurants = [
            {
                "name": p.get("name", "Sans nom"),
                "categories": p.get("kinds", "").replace(",", ", "),
                "distance_km": round(p.get("dist", 0) / 1000, 2),
            }
            for p in places
            if p.get("name")
        ]

        return {
            "restaurants": restaurants,
            "total_found": len(restaurants),
            "search_radius_km": radius_km,
        }

    except requests.RequestException as e:
        return {"error": f"Erreur lors de la recherche de restaurants : {str(e)}"}
