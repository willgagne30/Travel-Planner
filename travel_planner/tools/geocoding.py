"""
Tools de géocodage basés sur Nominatim (OpenStreetMap) et RestCountries.
Ces APIs sont entièrement gratuites et sans clé requise.
"""

import requests

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
RESTCOUNTRIES_URL = "https://restcountries.com/v3.1"
HEADERS = {"User-Agent": "TravelPlannerAgent/1.0"}


def geocode_city(city_name: str) -> dict:
    """
    Géocode une ville et retourne ses coordonnées GPS, pays et informations générales.

    Args:
        city_name: Le nom de la ville à géocoder (ex: "Paris", "Tokyo", "New York").

    Returns:
        Un dictionnaire avec les coordonnées et informations de la ville,
        ou un message d'erreur si la ville n'est pas trouvée.
    """
    try:
        params = {
            "q": city_name,
            "format": "json",
            "limit": 1,
            "addressdetails": 1,
        }
        response = requests.get(NOMINATIM_URL, params=params, headers=HEADERS, timeout=10)
        response.raise_for_status()
        results = response.json()

        if not results:
            return {"error": f"Ville '{city_name}' non trouvée.", "city": city_name}

        place = results[0]
        address = place.get("address", {})
        return {
            "city": city_name,
            "display_name": place.get("display_name", ""),
            "latitude": float(place.get("lat", 0)),
            "longitude": float(place.get("lon", 0)),
            "country": address.get("country", ""),
            "country_code": address.get("country_code", "").upper(),
            "state": address.get("state", ""),
        }
    except requests.RequestException as e:
        return {"error": f"Erreur lors du géocodage : {str(e)}", "city": city_name}


def get_country_info(country_code: str) -> dict:
    """
    Récupère des informations générales sur un pays (monnaie, langue, fuseau horaire, etc.)
    utiles pour planifier un voyage.

    Args:
        country_code: Le code ISO 2 lettres du pays (ex: "FR", "JP", "US").

    Returns:
        Un dictionnaire avec les informations du pays (monnaie, langue, visa, etc.),
        ou un message d'erreur si le pays n'est pas trouvé.
    """
    try:
        response = requests.get(
            f"{RESTCOUNTRIES_URL}/alpha/{country_code}",
            headers=HEADERS,
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        if not data:
            return {"error": f"Pays '{country_code}' non trouvé."}

        country = data[0] if isinstance(data, list) else data
        currencies = country.get("currencies", {})
        currency_info = {
            code: {"name": info.get("name", ""), "symbol": info.get("symbol", "")}
            for code, info in currencies.items()
        }
        languages = list(country.get("languages", {}).values())
        timezones = country.get("timezones", [])

        return {
            "country_name": country.get("name", {}).get("common", country_code),
            "capital": country.get("capital", [""])[0] if country.get("capital") else "",
            "currencies": currency_info,
            "languages": languages,
            "timezones": timezones,
            "region": country.get("region", ""),
            "subregion": country.get("subregion", ""),
            "population": country.get("population", 0),
        }
    except requests.RequestException as e:
        return {"error": f"Erreur lors de la récupération des infos pays : {str(e)}"}
