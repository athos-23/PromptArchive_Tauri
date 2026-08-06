"""
Entry point usato per impacchettare il backend FastAPI con PyInstaller
e farlo eseguire da Tauri come processo "sidecar".

Va lanciato/compilato dalla RADICE del repo (stesso livello di backend/ e
frontend/), esattamente come si fa oggi con:

    uvicorn backend.main:app --port 8000

così l'import `backend.main` (e i suoi import relativi interni, es.
`from . import models, database`) funzionano esattamente come in sviluppo.

Legge le variabili d'ambiente impostate da src-tauri/src/main.rs:
- PROMPTARCHIVE_DATA_DIR: cartella scrivibile dove salvare database.sqlite
  e le immagini (letta da backend/deps.py e backend/database.py).
- PROMPTARCHIVE_HOST / PROMPTARCHIVE_PORT: dove far ascoltare il server
  (default 127.0.0.1:8000, identico allo sviluppo).
"""

import os
import uvicorn

from backend.main import app

if __name__ == "__main__":
    host = os.environ.get("PROMPTARCHIVE_HOST", "127.0.0.1")
    port = int(os.environ.get("PROMPTARCHIVE_PORT", "8000"))
    uvicorn.run(app, host=host, port=port, log_level="info")
