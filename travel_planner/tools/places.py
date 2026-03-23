"""
Tool Google Places API pour la récupération de photos.
La clé API est configurée dans GOOGLE_API_KEY.
"""

import os
import requests

PLACES_API_URL = "https://maps.googleapis.com/maps/api/place"

def get_hotel_image_url(hotel_name: str, city_name: str) -> str:
    """
    Recherche la photo officielle de façade ou de présentation d'un hôtel via Google Places API.
    Cet outil est extrêmement utile pour fournir une "VRAIE URL d'image" pour le Markdown d'hébergement.

    Args:
        hotel_name: Le nom précis de l'hôtel (ex: "Hôtel Ritz").
        city_name: La ville où se trouve l'hôtel (ex: "Paris").

    Returns:
        Une chaîne de caractères contenant l'URL directe de l'image (haute résolution) 
        qui peut être intégrée dans un tag Markdown ![Nom](URL).
        Retourne un message d'erreur si l'hôtel n'a pas de photo ou si la recherche échoue.
    """
    api_key = os.getenv("GOOGLE_API_KEY", "")
    if not api_key:
        return "Erreur : La clé GOOGLE_API_KEY est introuvable."

    try:
        # Étape 1 : Text Search pour trouver le place_id et photo_reference
        search_params = {
            "query": f"{hotel_name} {city_name} hotel",
            "key": api_key,
        }
        search_response = requests.get(f"{PLACES_API_URL}/textsearch/json", params=search_params, timeout=10)
        search_response.raise_for_status()
        search_data = search_response.json()

        if not search_data.get("results"):
            return f"Erreur : Aucun hôtel trouvé pour '{hotel_name}' à '{city_name}'."

        first_result = search_data["results"][0]
        photos = first_result.get("photos", [])

        if not photos:
            return f"Erreur : L'hôtel '{hotel_name}' n'a pas de photos associées sur Google Maps."

        photo_reference = photos[0].get("photo_reference")
        
        # Étape 2 : Construction de l'URL finale (qui fera une redirection 302 vers l'image JPEG).
        # Le navigateur ou le markdown gère très bien les URL avec redirection 302.
        image_url = f"{PLACES_API_URL}/photo?maxwidth=800&maxheight=600&photo_reference={photo_reference}&key={api_key}"
        
        return image_url

    except requests.RequestException as e:
        return f"Erreur de réseau lors de la communication avec l'API Places : {str(e)}"
    except Exception as e:
        return f"Erreur lors de la récupération de l'image de l'hôtel : {str(e)}"
