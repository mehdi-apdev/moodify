import os
from flask import Flask, session, request, redirect, url_for
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time

# --- CONFIGURATION ---
# Remplacez ces valeurs par celles de votre Spotify Developer Dashboard
CLIENT_ID = '76b02dbe17724bdbb566bedfeecd289d'
CLIENT_SECRET = '8eb086bad2bd4f019c6dc51c4b2cab53'

# Assurez-vous que cette URL est ajoutée dans les "Redirect URIs" du dashboard Spotify
REDIRECT_URI = 'http://127.0.0.1:5000/callback'

# Les permissions demandées (scopes). Ici, on veut lire la librairie de l'utilisateur.
# Liste complète : https://developer.spotify.com/documentation/general/guides/authorization/scopes/
SCOPE = 'user-library-read'

# Configuration de l'application Flask
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Clé pour sécuriser la session cookie
app.config['SESSION_COOKIE_NAME'] = 'Spotify Cookie'


@app.route('/')
def index():
    """
    Page d'accueil.
    Vérifie si l'utilisateur est connecté. Sinon, propose un lien de connexion.
    """
    token_info = session.get('token_info', None)

    if not token_info:
        return "Bienvenue ! <a href='/login'>Se connecter avec Spotify</a>"

    # Vérification si le token est expiré
    if is_token_expired(token_info):
        return redirect(url_for('login'))

    # Si on est connecté, on peut utiliser spotipy
    sp = spotipy.Spotify(auth=token_info['access_token'])

    # Exemple : Récupérer les 5 dernières pistes likées
    results = sp.current_user_saved_tracks(limit=5)
    html = "<h1>Connexion Réussie !</h1><h2>Vos 5 derniers titres likés :</h2><ul>"
    for idx, item in enumerate(results['items']):
        track = item['track']
        html += f"<li>{idx + 1}: {track['artists'][0]['name']} – {track['name']}</li>"
    html += "</ul>"

    return html


@app.route('/login')
def login():
    """
    Crée l'objet d'authentification et redirige l'utilisateur vers la page de login Spotify.
    """
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


@app.route('/callback')
def callback():
    """
    L'utilisateur revient ici après avoir accepté sur Spotify.
    On récupère le 'code' dans l'URL et on l'échange contre un token.
    """
    sp_oauth = create_spotify_oauth()
    session.clear()

    # Récupération du code envoyé par Spotify
    code = request.args.get('code')

    # Échange du code contre le token d'accès
    token_info = sp_oauth.get_access_token(code)

    # Sauvegarde du token dans la session utilisateur
    session['token_info'] = token_info

    return redirect(url_for('index'))


def create_spotify_oauth():
    """
    Helper pour créer l'instance d'authentification avec les bons paramètres.
    """
    return SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE
    )


def is_token_expired(token_info):
    """
    Vérifie si le token actuel est expiré.
    """
    now = int(time.time())
    return token_info['expires_at'] - now < 60


if __name__ == '__main__':
    # Lance le serveur sur le port 5000
    print(f"L'application tourne sur {REDIRECT_URI.split('/callback')[0]}")
    app.run(port=5000, debug=True)