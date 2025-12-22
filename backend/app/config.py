import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # On utilise os.getenv avec une valeur par défaut pour éviter les crashs si .env est vide
    CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
    CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
    REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev_key') # Clé par défaut pour le dev
    FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://127.0.0.1:4200')
    SCOPE = 'user-library-read'