import os
import time
from flask import Flask, session, request, redirect, url_for, jsonify
from flask_cors import CORS
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# --- CONFIGURATION ---
CLIENT_ID = '76b02dbe17724bdbb566bedfeecd289d'
CLIENT_SECRET = '8eb086bad2bd4f019c6dc51c4b2cab53'
REDIRECT_URI = 'http://127.0.0.1:5000/callback'
SCOPE = 'user-library-read'

app = Flask(__name__)

# 1. CORS CONFIGURÉ SUR 127.0.0.1 (IMPORTANT pour les cookies)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:4200"}}, supports_credentials=True)

app.secret_key = 'une_cle_secrete_fixe_pour_le_dev'
app.config['SESSION_COOKIE_NAME'] = 'Spotify Cookie'


@app.route('/')
def index():
    return "Serveur Flask en ligne ! <a href='/login'>Se connecter</a>"


@app.route('/login')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


@app.route('/callback')
def callback():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info

    # 2. REDIRECTION MODIFIÉE : Vers la racine (Mood Selector)
    # Et on utilise 127.0.0.1 pour matcher le cookie
    return redirect("http://127.0.0.1:4200/")


@app.route('/recommendations')
def get_recommendations():
    token_info = session.get('token_info', None)

    if not token_info:
        return jsonify({'error': 'Non connecté'}), 401

    if is_token_expired(token_info):
        return jsonify({'error': 'Token expiré'}), 401

    try:
        sp = spotipy.Spotify(auth=token_info['access_token'])
        results = sp.current_user_saved_tracks(limit=10)

        tracks_dto = []
        for item in results['items']:
            track = item['track']

            tracks_dto.append({
                'id': track['id'],
                'title': track['name'],
                'artist': track['artists'][0]['name'],
                'album': track['album']['name'],
                'albumCoverUrl': track['album']['images'][0]['url'] if track['album']['images'] else '',
                'previewUrl': track['preview_url']
            })

        return jsonify(tracks_dto)

    except Exception as e:
        print(f"Erreur: {e}")
        return jsonify({'error': 'Erreur serveur'}), 500


def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE
    )


def is_token_expired(token_info):
    now = int(time.time())
    return token_info['expires_at'] - now < 60


if __name__ == '__main__':
    app.run(port=5000, debug=True)