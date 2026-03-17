"""
Tool de conversion de devises basé sur ExchangeRate-API (gratuit, sans clé).
Utilise l'endpoint public open.er-api.com.
"""

import requests

EXCHANGE_URL = "https://open.er-api.com/v6/latest"


def get_exchange_rate(base_currency: str, target_currency: str) -> dict:
    """
    Récupère le taux de change actuel entre deux devises.
    Utile pour estimer les coûts d'un voyage dans une devise étrangère.

    Args:
        base_currency: Code ISO 4217 de la devise de départ (ex: "EUR", "USD", "CAD").
        target_currency: Code ISO 4217 de la devise cible (ex: "JPY", "GBP", "THB").

    Returns:
        Un dictionnaire avec le taux de change et la date de mise à jour,
        ou un message d'erreur si les devises sont invalides.
    """
    try:
        response = requests.get(
            f"{EXCHANGE_URL}/{base_currency.upper()}",
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        if data.get("result") != "success":
            return {"error": f"Devise '{base_currency}' invalide ou non supportée."}

        rates = data.get("rates", {})
        target = target_currency.upper()

        if target not in rates:
            return {"error": f"Devise cible '{target_currency}' non supportée."}

        rate = rates[target]
        return {
            "base_currency": base_currency.upper(),
            "target_currency": target,
            "exchange_rate": rate,
            "example": f"1 {base_currency.upper()} = {rate:.4f} {target}",
            "last_updated": data.get("time_last_update_utc", ""),
            "source": "ExchangeRate-API (open.er-api.com)",
        }

    except requests.RequestException as e:
        return {"error": f"Erreur lors de la récupération du taux de change : {str(e)}"}


def convert_currency(amount: float, from_currency: str, to_currency: str) -> dict:
    """
    Convertit un montant d'une devise vers une autre en utilisant les taux de change actuels.

    Args:
        amount: Le montant à convertir (ex: 100.0, 1500.50).
        from_currency: Code ISO 4217 de la devise source (ex: "EUR", "CAD", "USD").
        to_currency: Code ISO 4217 de la devise cible (ex: "JPY", "THB", "GBP").

    Returns:
        Un dictionnaire avec le montant converti et le taux appliqué,
        ou un message d'erreur si la conversion échoue.
    """
    rate_result = get_exchange_rate(from_currency, to_currency)

    if "error" in rate_result:
        return rate_result

    rate = rate_result["exchange_rate"]
    converted = amount * rate

    return {
        "original_amount": amount,
        "from_currency": from_currency.upper(),
        "to_currency": to_currency.upper(),
        "converted_amount": round(converted, 2),
        "exchange_rate": rate,
        "summary": f"{amount} {from_currency.upper()} = {converted:.2f} {to_currency.upper()}",
        "last_updated": rate_result.get("last_updated", ""),
    }
