"""
Tool Google Places API pour la récupération de photos d'hôtels.
La clé API est configurée dans GOOGLE_API_KEY.
Cet outil ne peut PAS être utilisé en même temps que google_search natif (erreur 400).
Il est donc réservé exclusivement à hotel_photo_agent.
"""

import os
import requests

PLACES_API_URL = "https://maps.googleapis.com/maps/api/place"


def get_hotel_image_url(hotel_name: str, city_name: str) -> str:
    """
    Récupère l'URL directe de la photo officielle d'un hôtel via Google Places API.
    Utiliser cet outil pour chaque hôtel du rapport après avoir reçu la liste de hotel_search_agent.

    Args:
        hotel_name: Le nom précis de l'hôtel (ex: "Hôtel Ritz").
        city_name: La ville où se trouve l'hôtel (ex: "Paris").

    Returns:
        Une URL directe vers la photo de l'hôtel, intégrable dans Markdown ![Nom](URL).
        Retourne un message d'erreur si la photo est introuvable.
    """
    api_key = os.getenv("GOOGLE_API_KEY", "")
    if not api_key:
        return "Erreur : La clé GOOGLE_API_KEY est introuvable dans .env."

    try:
        search_params = {
            "query": f"{hotel_name} {city_name} hotel",
            "key": api_key,
        }
        search_response = requests.get(
            f"{PLACES_API_URL}/textsearch/json",
            params=search_params,
            timeout=10
        )
        search_response.raise_for_status()
        search_data = search_response.json()

        if not search_data.get("results"):
            return f"Aucun résultat Places pour '{hotel_name}' à '{city_name}'."

        photos = search_data["results"][0].get("photos", [])

        if not photos:
            return f"Pas de photo disponible sur Google Maps pour '{hotel_name}'."

        photo_reference = photos[0].get("photo_reference")
        image_url = (
            f"{PLACES_API_URL}/photo"
            f"?maxwidth=800&maxheight=600"
            f"&photo_reference={photo_reference}"
            f"&key={api_key}"
        )
        return image_url

    except requests.RequestException as e:
        return f"Erreur réseau Google Places : {str(e)}"
    except Exception as e:
        return f"Erreur inattendue : {str(e)}"
