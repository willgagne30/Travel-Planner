"""
Tool de recherche web généraliste personnalisé (alternative gratuite à google_search).
Utilise DuckDuckGo (version HTML Lite) pour éviter la limitation API de Gemini
(conflit entre built-in tools et custom function calling).
"""

import urllib.parse
import urllib.request
import re

def web_search(query: str, limit: int = 5) -> dict:
    """
    Recherche sur le web des informations en temps réel utiles à la planification
    de voyage (ex: "vols Paris Rome novembre", "avis hôtel X", "prix train Y").
    Cet outil remplace google_search pour éviter les conflits d'API.

    Args:
        query: La requête de recherche (mots-clés pertinents).
        limit: Le nombre de résultats à retourner (défaut: 5, max: 10).

    Returns:
        Un dictionnaire contenant les résultats de recherche (titre, description courte, lien)
        ou un message d'erreur.
    """
    try:
        # DDG Lite: Version allégée sans JS, facile à scrapper légalement pour usage basique
        encoded_query = urllib.parse.quote_plus(query)
        url = f"https://html.duckduckgo.com/html/?q={encoded_query}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode("utf-8")
            
        # Extraction basique avec RegEx adaptées à la structure HTMLLite de DDG
        snippets = re.findall(r'<a class="result__snippet[^>]*?href="([^"]+)"[^>]*?>(.*?)</a>', html, re.IGNORECASE | re.DOTALL)
        titles = re.findall(r'<a class="result__url"[^>]*?href="([^"]+)"[^>]*?>(.*?)</a>', html, re.IGNORECASE | re.DOTALL)

        results = []
        for i in range(min(len(snippets), limit)):
            url, snippet_html = snippets[i]
            # Rechercher un titre correspondant à cette URL
            title_text = "Résultat Web"
            for t_url, t_html in titles:
                if t_url == url:
                    title_text = re.sub(r'<[^>]+>', '', t_html).strip()
                    break
            
            snippet_clean = re.sub(r'<[^>]+>', '', snippet_html).strip()
            
            results.append({
                "title": title_text,
                "snippet": snippet_clean,
                "link": url
            })
        
        if not results:
            return {
                "query": query,
                "message": "Aucun résultat trouvé sur le Web.",
                "results": []
            }
            
        return {
            "query": query,
            "source": "Web Search (DuckDuckGo)",
            "total_returned": len(results),
            "results": results,
            "note_to_agent": "Lis les 'snippets' (descriptions) pour trouver la réponse."
        }
        
    except Exception as e:
        return {"error": f"La recherche Web a échoué: {str(e)}"}
