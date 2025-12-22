import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Clés secrètes
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev_secret_key'

    # Spotify
    CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
    CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')
    REDIRECT_URI = os.environ.get('SPOTIFY_REDIRECT_URI')

    # Scopes (Droits demandés)
    SCOPE = "user-library-read user-top-read playlist-read-private playlist-read-collaborative"

    # Frontend
    FRONTEND_URL = "http://127.0.0.1:4200"