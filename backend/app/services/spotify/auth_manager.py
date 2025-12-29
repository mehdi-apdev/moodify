import spotipy
from spotipy.oauth2 import SpotifyOAuth
from app.config import Config


class SpotifyAuthManager:
    def __init__(self):
        self.oauth = SpotifyOAuth(
            client_id=Config.CLIENT_ID,
            client_secret=Config.CLIENT_SECRET,
            redirect_uri=Config.REDIRECT_URI,
            scope=Config.SCOPE
        )

    def get_authorize_url(self):
        return self.oauth.get_authorize_url()


    def get_auth_url(self):
        return self.get_authorize_url()

    def get_token_from_code(self, code):
        return self.oauth.get_access_token(code)

    def get_token(self, code):
        return self.get_token_from_code(code)

    def get_client(self, token):
        """Retourne une instance de l'API Spotify déjà authentifiée"""
        return spotipy.Spotify(auth=token)
