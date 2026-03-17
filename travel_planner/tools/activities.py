"""
Tools de recherche d'activités et restaurants basés sur Overpass API (OpenStreetMap).
Complètement gratuit, sans inscription, sans clé API requise.
"""

import requests

OVERPASS_URL = "https://overpass-api.de/api/interpreter"
HEADERS = {"User-Agent": "TravelPlannerAgent/1.0"}

# Mapping des centres d'intérêts vers des tags OpenStreetMap
INTEREST_TO_TAGS = {
    "culture": [
        '["tourism"="museum"]',
        '["historic"]',
        '["tourism"="gallery"]',
    ],
    "gastronomie": [
        '["amenity"="restaurant"]',
        '["amenity"="cafe"]',
        '["amenity"="bar"]',
    ],
    "aventure": [
        '["leisure"="sports_centre"]',
        '["sport"]',
        '["tourism"="adventure"]',
    ],
    "nature": [
        '["leisure"="park"]',
        '["natural"="beach"]',
        '["tourism"="viewpoint"]',
    ],
    "détente": [
        '["leisure"="spa"]',
        '["amenity"="spa"]',
        '["tourism"="hotel"]',
    ],
    "art": [
        '["tourism"="gallery"]',
        '["tourism"="museum"]',
    ],
    "shopping": [
        '["shop"="mall"]',
        '["shop"="market"]',
    ],
    "architecture": [
        '["historic"="monument"]',
        '["historic"="building"]',
        '["tourism"="attraction"]',
    ],
    "default": [
        '["tourism"="attraction"]',
        '["tourism"="museum"]',
        '["historic"]',
    ],
}


def _build_overpass_query(latitude: float, longitude: float, radius_m: int, tags: list, limit: int) -> str:
    """Construit une requête Overpass QL pour chercher des lieux par tags."""
    node_queries = "\n".join(
        f'  node{tag}(around:{radius_m},{latitude},{longitude});'
        for tag in tags
    )
    way_queries = "\n".join(
        f'  way{tag}(around:{radius_m},{latitude},{longitude});'
        for tag in tags
    )
    return f"""
[out:json][timeout:25];
(
{node_queries}
{way_queries}
);
out center {limit};
"""


def search_attractions(
    latitude: float,
    longitude: float,
    radius_km: int = 10,
    interests: str = "culture",
    limit: int = 15,
) -> dict:
    """
    Recherche des attractions touristiques, monuments et points d'intérêt
    autour d'une position géographique via OpenStreetMap (Overpass API).
    Entièrement gratuit, aucune clé API requise.

    Args:
        latitude: Latitude du centre de recherche (ex: 48.8566 pour Paris).
        longitude: Longitude du centre de recherche (ex: 2.3522 pour Paris).
        radius_km: Rayon de recherche en kilomètres (défaut: 10 km).
        interests: Type d'intérêts séparés par des virgules
                   (ex: "culture,art", "nature,aventure", "gastronomie").
                   Valeurs possibles: culture, gastronomie, aventure, nature, détente, art, shopping, architecture.
        limit: Nombre maximum de résultats à retourner (défaut: 15).

    Returns:
        Un dictionnaire contenant une liste d'attractions avec nom, catégorie
        et coordonnées, ou un message d'erreur.
    """
    try:
        # Collecter les tags correspondant aux intérêts
        tags = []
        for interest in interests.lower().split(","):
            interest = interest.strip()
            tags.extend(INTEREST_TO_TAGS.get(interest, INTEREST_TO_TAGS["default"]))
        # Dédupliquer
        tags = list(dict.fromkeys(tags))[:6]  # Max 6 types pour éviter timeout

        query = _build_overpass_query(latitude, longitude, radius_km * 1000, tags, limit)
        response = requests.post(
            OVERPASS_URL,
            data={"data": query},
            headers=HEADERS,
            timeout=30,
        )
        response.raise_for_status()
        elements = response.json().get("elements", [])

        attractions = []
        for el in elements:
            tags_el = el.get("tags", {})
            name = tags_el.get("name") or tags_el.get("name:fr") or tags_el.get("name:en")
            if not name:
                continue
            lat = el.get("lat") or el.get("center", {}).get("lat")
            lon = el.get("lon") or el.get("center", {}).get("lon")
            category = (
                tags_el.get("tourism")
                or tags_el.get("historic")
                or tags_el.get("leisure")
                or tags_el.get("amenity")
                or "attraction"
            )
            attractions.append({
                "name": name,
                "category": category,
                "latitude": lat,
                "longitude": lon,
                "website": tags_el.get("website", ""),
                "opening_hours": tags_el.get("opening_hours", ""),
                "description": tags_el.get("description", ""),
            })

        return {
            "attractions": attractions[:limit],
            "total_found": len(attractions),
            "search_radius_km": radius_km,
            "interests": interests,
            "source": "OpenStreetMap via Overpass API (gratuit, sans clé)",
        }

    except requests.RequestException as e:
        return {"error": f"Erreur Overpass API : {str(e)}"}


def search_restaurants(
    latitude: float,
    longitude: float,
    radius_km: int = 3,
    cuisine: str = "",
    limit: int = 15,
) -> dict:
    """
    Recherche des restaurants, cafés et lieux de restauration autour d'une position
    géographique via OpenStreetMap (Overpass API).
    Entièrement gratuit, aucune clé API requise.

    Args:
        latitude: Latitude du centre de recherche.
        longitude: Longitude du centre de recherche.
        radius_km: Rayon de recherche en kilomètres (défaut: 3 km).
        cuisine: Type de cuisine souhaité (ex: "french", "italian", "japanese").
                 Laisser vide pour tous les types de cuisine.
        limit: Nombre maximum de restaurants à retourner (défaut: 15).

    Returns:
        Un dictionnaire contenant une liste de restaurants avec nom, type de cuisine,
        coordonnées et horaires, ou un message d'erreur.
    """
    try:
        cuisine_filter = f'["cuisine"="{cuisine}"]' if cuisine else ""
        tags = [
            f'["amenity"="restaurant"]{cuisine_filter}',
            '["amenity"="cafe"]',
            '["amenity"="fast_food"]',
            '["amenity"="bar"]',
        ]
        query = _build_overpass_query(latitude, longitude, radius_km * 1000, tags, limit)
        response = requests.post(
            OVERPASS_URL,
            data={"data": query},
            headers=HEADERS,
            timeout=30,
        )
        response.raise_for_status()
        elements = response.json().get("elements", [])

        restaurants = []
        for el in elements:
            tags_el = el.get("tags", {})
            name = tags_el.get("name") or tags_el.get("name:fr") or tags_el.get("name:en")
            if not name:
                continue
            restaurants.append({
                "name": name,
                "type": tags_el.get("amenity", "restaurant"),
                "cuisine": tags_el.get("cuisine", "non précisé"),
                "opening_hours": tags_el.get("opening_hours", ""),
                "website": tags_el.get("website", ""),
                "phone": tags_el.get("phone", ""),
            })

        return {
            "restaurants": restaurants[:limit],
            "total_found": len(restaurants),
            "search_radius_km": radius_km,
            "source": "OpenStreetMap via Overpass API (gratuit, sans clé)",
        }

    except requests.RequestException as e:
        return {"error": f"Erreur Overpass API : {str(e)}"}
