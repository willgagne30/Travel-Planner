"""
Serveur web intégré pour l'interface Planificateur de Voyage.
Charge l'application ADK en local et lui ajoute le middleware CORS
pour autoriser les requêtes web directement, tout en servant chat.html.
Lance avec: uv run python server.py
"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from google.adk.cli.fast_api import get_fast_api_app
from pathlib import Path
import os
import uvicorn

# Forcer le bon backend et app pour ADK
os.environ["ADK_APP_NAME"] = "travel_planner"
os.environ["ADK_PACKAGE_NAME"] = "travel_planner"

print("Initialisation du moteur ADK...")
# 1. Creer l'application FastAPI de l'ADK
adk_app = get_fast_api_app(agents_dir=".", web=False)

# 2. Ajouter CORS a l'application ADK
adk_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Creer une application principale qui sert aussi le HTML
app = FastAPI(title="Travel Agent UI")

# Monter l'ADK sur /api (ou à la racine si on veut simplifier)
app.mount("/api", adk_app)

@app.get("/", response_class=HTMLResponse)
@app.get("/chat.html", response_class=HTMLResponse)
async def serve_chat():
    html = Path("chat.html").read_text(encoding="utf-8")
    return HTMLResponse(content=html)

if __name__ == "__main__":
    print("\n" + "="*50)
    print("  Planificateur de Voyage - Interface Web")
    print("  Ouvrez: http://localhost:8080")
    print("="*50 + "\n")
    uvicorn.run(app, host="127.0.0.1", port=8080)
