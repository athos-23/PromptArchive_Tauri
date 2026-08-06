import os
from . import database


# Paths
# In sviluppo (uvicorn --reload) usiamo la cartella "data/" del repo come prima.
# Nella build desktop (Tauri), src-tauri/src/main.rs imposta la variabile
# d'ambiente PROMPTARCHIVE_DATA_DIR puntando alla cartella dati dell'utente
# (scrivibile anche quando l'app è installata in Program Files).
DATA_DIR = os.environ.get(
    "PROMPTARCHIVE_DATA_DIR",
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "data"),
)
IMAGES_DIR = os.path.join(DATA_DIR, "images")
os.makedirs(IMAGES_DIR, exist_ok=True)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
