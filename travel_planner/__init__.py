"""Coordinateur de voyage : planifier des voyages complets et personnalisés"""

import os

from dotenv import load_dotenv

load_dotenv()

use_vertex = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "0")

if use_vertex in ("1", "True", "true"):
    try:
        import google.auth

        _, project_id = google.auth.default()
        os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)
        os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
        os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")
    except Exception:
        pass

from . import agent
