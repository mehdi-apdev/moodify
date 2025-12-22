from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = '76b02dbe17724bdbb566bedfeecd289d'
CLIENT_SECRET = '8eb086bad2bd4f019c6dc51c4b2cab53'
REDIRECT_URI = 'http://127.0.0.1:5000/callback'
SCOPE = 'user-read-private user-read-email user-library-read playlist-modify-private playlist-modify-public playlist-read-private'

sp_oauth = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE,
    show_dialog=True
)