"""
Tool météo basé sur OpenWeatherMap API.
Le niveau gratuit offre 1000 appels/jour.
La clé API est configurée dans OPENWEATHERMAP_API_KEY.
"""

import os
import requests
from datetime import datetime

OWM_URL = "https://api.openweathermap.org/data/2.5"


def get_weather_forecast(city_name: str, days: int = 5) -> dict:
    """
    Récupère les prévisions météo pour une ville sur les prochains jours.
    Utile pour planifier les activités en fonction du temps prévu.

    Args:
        city_name: Nom de la ville pour laquelle obtenir la météo (ex: "Paris", "Tokyo").
        days: Nombre de jours de prévision souhaités (entre 1 et 5, défaut: 5).
              Note: L'API gratuite offre jusqu'à 5 jours de prévisions.

    Returns:
        Un dictionnaire contenant les prévisions météo jour par jour avec température,
        conditions et précipitations, ou un message d'erreur.
    """
    api_key = os.getenv("OPENWEATHERMAP_API_KEY", "")
    if not api_key:
        return {
            "error": "Clé API OpenWeatherMap manquante. Ajoutez OPENWEATHERMAP_API_KEY dans .env. "
                     "Inscription gratuite sur https://openweathermap.org/api"
        }

    try:
        # Utiliser l'endpoint forecast (prévisions 5 jours / 3h)
        params = {
            "q": city_name,
            "appid": api_key,
            "units": "metric",
            "lang": "fr",
            "cnt": min(days, 5) * 8,  # 8 créneaux de 3h par jour
        }
        response = requests.get(f"{OWM_URL}/forecast", params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Regrouper les prévisions par jour
        daily_forecasts = {}
        for item in data.get("list", []):
            date_str = item["dt_txt"].split(" ")[0]
            if date_str not in daily_forecasts:
                daily_forecasts[date_str] = {
                    "date": date_str,
                    "temps_min": item["main"]["temp_min"],
                    "temps_max": item["main"]["temp_max"],
                    "conditions": [],
                    "precipitations_mm": 0,
                }
            forecast = daily_forecasts[date_str]
            forecast["temps_min"] = min(forecast["temps_min"], item["main"]["temp_min"])
            forecast["temps_max"] = max(forecast["temps_max"], item["main"]["temp_max"])
            forecast["conditions"].append(item["weather"][0]["description"])
            forecast["precipitations_mm"] += item.get("rain", {}).get("3h", 0)

        # Résumer les conditions de chaque jour
        result_days = []
        for date_str, day in list(daily_forecasts.items())[:days]:
            conditions_set = list(dict.fromkeys(day["conditions"]))  # Dédupliquer
            result_days.append({
                "date": date_str,
                "temperature_min_celsius": round(day["temps_min"], 1),
                "temperature_max_celsius": round(day["temps_max"], 1),
                "conditions": ", ".join(conditions_set[:2]),
                "precipitations_mm": round(day["precipitations_mm"], 1),
            })

        return {
            "city": data.get("city", {}).get("name", city_name),
            "country": data.get("city", {}).get("country", ""),
            "forecasts": result_days,
            "note": "Prévisions météo sur 5 jours maximum (API gratuite OpenWeatherMap).",
        }

    except requests.HTTPError as e:
        if e.response.status_code == 404:
            return {"error": f"Ville '{city_name}' non trouvée dans OpenWeatherMap."}
        return {"error": f"Erreur API météo : {str(e)}"}
    except requests.RequestException as e:
        return {"error": f"Erreur de connexion météo : {str(e)}"}
