"""
Configuration centralisée du Travel Planner.

Ce module regroupe toutes les constantes de configuration partagées
par les agents et sous-agents, évitant la duplication de code.
"""

import os

# Modèle principal (utilisé pour les agents nécessitant un raisonnement approfondi)
MODEL = os.getenv("GOOGLE_MODEL", "gemini-2.5-pro")

# Modèle rapide (utilisé pour les agents de recherche simple, plus économique)
MODEL_FAST = os.getenv("GOOGLE_MODEL_FAST", "gemini-2.5-flash")
