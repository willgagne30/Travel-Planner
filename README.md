# Assistant de Planification de Voyage IA - Agent Google ADK

## C'est quoi un Agent ?

Un **agent** est un programme qui utilise un LLM (Large Language Model) pour :
1. Comprendre une demande en langage naturel
2. Decider quelles actions effectuer (appeler des outils, deleguer a des sous-agents)
3. Repondre de maniere structuree

## Architecture de cet agent

```
                    ┌─────────────────────────┐
                    │   travel_coordinator     │  <- Agent principal
                    │   (orchestrateur)        │
                    └──────────┬──────────────┘
                               │
            ┌──────────┬───────┴───────┬──────────┐
            │          │               │          │
     ┌──────▼──┐ ┌─────▼─────┐ ┌──────▼────┐ ┌───▼──────┐
     │ flight  │ │  hotel    │ │ activity  │ │itinerary │
     │ search  │ │  search   │ │  search   │ │ planner  │
     └─────────┘ └───────────┘ └───────────┘ └──────────┘
     Google Search Google Search Google Search   (LLM)
```

### Flux de travail (etape par etape)

1. **flight_search** : Recherche des options de vols via Google Search
2. **hotel_search** : Trouve des hebergements adaptes via Google Search
3. **activity_search** : Suggere des activites et experiences via Google Search
4. **itinerary_planner** : Genere un itineraire jour par jour structure

## Fichiers cles

```
travel_planner/
├── __init__.py       # Point d'entree, charge la config
├── agent.py          # Agent coordinateur + liens vers sous-agents
├── prompt.py         # Instructions du coordinateur
└── sub_agents/
    ├── flight_search/
    │   ├── agent.py  # Agent + outil google_search
    │   └── prompt.py # Instructions specifiques
    ├── hotel_search/
    │   ├── agent.py  # Agent + outil google_search
    │   └── prompt.py # Instructions specifiques
    ├── activity_search/
    │   ├── agent.py  # Agent + outil google_search
    │   └── prompt.py # Instructions specifiques
    └── itinerary_planner/
        ├── agent.py  # Agent LLM uniquement
        └── prompt.py # Instructions specifiques
```

## Installation et lancement

### 1. Prerequis
- Python 3.10 a 3.12
- Une cle API Gemini (https://aistudio.google.com/apikey)

### 2. Configurer le fichier .env
```
GOOGLE_GENAI_USE_VERTEXAI=0
GOOGLE_API_KEY=votre_cle_api_ici
GOOGLE_MODEL=gemini-3.1-flash-lite-preview
```

### 3. Installer et lancer
```bash
uv sync
uv run adk web
```

Puis ouvrir le navigateur a l'adresse affichee et selectionner `travel_planner`.

## Exemple d'interaction

> **Vous** : Je veux voyager a Tokyo du 15 au 22 avril avec un budget de 2000€

> **Agent** : Lance le flight_search pour trouver les meilleurs vols...

> **Vous** : Je prefere un hotel en centre-ville, j'aime la gastronomie et la culture

> **Agent** : Le hotel_search trouve des hebergements, l'activity_search propose des activites,
> puis l'itinerary_planner genere un itineraire complet jour par jour.

## Concepts cles a retenir

| Concept | Description |
|---|---|
| **Agent** | Programme autonome qui utilise un LLM pour raisonner et agir |
| **Sub-agent** | Agent specialise delegue par l'agent principal |
| **Tool** | Outil externe que l'agent peut appeler (ex: Google Search) |
| **Prompt** | Instructions qui definissent le comportement de l'agent |
| **Orchestration** | L'agent principal coordonne les sous-agents en sequence |
| **output_key** | Permet de passer des resultats d'un sous-agent a l'autre via l'etat partage |
